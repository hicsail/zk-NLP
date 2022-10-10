import sys
import numpy as np
from dataclasses import dataclass
import os
from .globals import *
from .expr import *
from .data_types import *
import sys

emp_output_string = ""
current_wire = 0
witness_list = []
IR_MODE = 1

def next_wire():
    global current_wire
    r = current_wire
    current_wire += 1
    return '$' + str(r)

def emit(s=''):
    global emp_output_string
    emp_output_string += s + '\n'

def add_to_witness(obj, comment=None):
    wire_name = str(next_wire())
    witness_list.append(obj)
    if comment:
        emit(f'  {wire_name} <- @short_witness; // {comment}')
    else:
        emit(f'  {wire_name} <- @short_witness;')

    return wire_name

def _extended_gcd(a, b):
   """
   Division in integers modulus p means finding the inverse of the
   denominator modulo p and then multiplying the numerator by this
   inverse (Note: inverse of A is B such that A*B % p == 1) this can
   be computed via extended Euclidean algorithm
   """
   x = 0
   last_x = 1
   y = 1
   last_y = 0
   while b != 0:
       quot = a // b
       a, b = b, a % b
       x, last_x = last_x - quot * x, x
       y, last_y = last_y - quot * y, y
   return last_x, last_y

def modular_inverse(x, p):
   """Compute the inverse of x mod p, i.e. b s.t. x*b mod p = 1"""
   b, _ = _extended_gcd(x, p)
   return b % p

int_ops_ir1 = {
    'add': 'add',
    'mul': 'mul',
    'div': 'div',
    'mod': 'mod'
}

def subst(x, v, e):
    sys.setrecursionlimit(10000)

    assert isinstance(x, SymVar)
    if e is x:
        return v
    elif isinstance(e, (int, float, str, SymVar, SecretInt)):
        return e
    elif isinstance(e, Prim):
        return Prim(e.op, [subst(x, v, a) for a in e.args], e.val)
    else:
        raise RuntimeError('unknown expression type', e)


def print_exp_ir1(e):
    global all_pubvals
    global params

    if isinstance(e, (SecretArray, SecretTensor, SecretInt, SymVar)):
        return add_to_witness(e)

    elif isinstance(e, str):
        # this is a wire name
        return e

    elif isinstance(e, int):
        r = next_wire()
        emit(f'  {r} <- < {e} >;')
        return r
    elif isinstance(e, Prim):
        if e.op in int_ops_ir1:
            e1, e2 = e.args
            x1 = print_exp_ir1(e1)
            x2 = print_exp_ir1(e2)
            op_sym = int_ops_ir1[e.op]
            r = next_wire()

            emit(f'  {r} <- @{op_sym}({x1}, {x2});')
            return r
        elif e.op == 'fold':
            x, body, accum, xs, init = e.args
            assert isinstance(xs, SecretList)

            if IR_MODE == 1:
                for x_val in val_of(xs):
                    r1 = next_wire()
                    emit(f' {r1} <- < {x_val} >;')
                    # TODO Need function name
                    fun_name = '_'
                    rf = next_wire()
                    r1 = rf
                    # TODO I don't think this loop is right
                    for i in range(init, len(val_of(xs))):
                        rf = next_wire()
                        emit(f' {r1}...{rf} <- @for i @first {r1} @last {rf}')
                        emit(f'   $i <- @call({fun_name}, $(i - 1), $(i - 2));')
                        emit(f' @end')

                        # a = init
                        # for x_val in val_of(xs):
                        #     b = subst(accum, a, body)
                        #     a = subst(x, SecretInt(x_val), b)
                        # TODO What do I return?
                        return rf
            elif IR_MODE == 0:
                a_wire = print_exp_ir1(init)
                for x_val in val_of(xs):
                    b = subst(accum, a_wire, body)
                    a = subst(x, SecretInt(x_val), b)
                    a_wire = print_exp_ir1(a)

                return a_wire

            else:
                raise RuntimeError('unknown IR mode:', IR_MODE)
        elif e.op == 'mux':
            e1, e2, e3 = e.args
            x1 = print_exp_ir1(e1)
            x2 = print_exp_ir1(e2)
            x3 = print_exp_ir1(e3)
            c = params['arithmetic_field'] - 1

            r1 = next_wire()
            emit(f'  {r1} <- @mul({x1}, < {x2} >);')
            r2 = next_wire()
            emit(f'  {r2} <- @mulc({x1}, < {c} >);')
            r3 = next_wire()
            emit(f'  {r3} <- @mul({r2}, {x3});')
            r_val = next_wire()
            emit(f'  {r_val} <- @add({r1}, {r3});')
            return r_val
        elif e.op == 'equals':
            e1, e2 = e.args
            x1 = print_exp_ir1(e1)
            x2 = print_exp_ir1(e2)

            diff = e1 - e2
            print('diff is:', diff)
            temp_wire_1 = next_wire()
            wire_name_for_diff = next_wire()
            c = params['arithmetic_field'] - 1

            emit(f'  {temp_wire_1} <- @mulc({x2}, < {c} >);')
            emit(f'  {wire_name_for_diff} <- @add({x1}, {temp_wire_1}); // diff')

            if val_of(diff) != 0:
                res = 1
            else:
                res = val_of(diff)

            wire_name_for_res = add_to_witness(SecretInt(res), 'res')
            temp = next_wire()
            emit(f'  {temp} <- @mulc({wire_name_for_res}, < {c} >);')
            r_res = next_wire()
            emit(f'  {r_res} <- @addc({temp}, < 1 >);')

            diff_inv = SecretInt(modular_inverse(val_of(diff), c + 1))

            wire_name_for_diff_inv = add_to_witness(diff_inv, 'diff_inv')

            temp_wire_1 = next_wire()
            emit(f'  {temp_wire_1} <- @addc({wire_name_for_diff_inv}, < 1 >);')

            temp_wire_2 = next_wire()
            emit(f'  {temp_wire_2} <- @mul({wire_name_for_diff_inv}, {temp_wire_1});')

            temp_wire_1 = next_wire()
            emit(f'  {temp_wire_1} <- @mul({temp_wire_2}, {wire_name_for_res});')

            temp_wire_2 = next_wire()
            emit(f'  {temp_wire_2} <- @mulc({wire_name_for_res}, < {c} >);')
            temp_wire_3 = next_wire()
            emit(f'  {temp_wire_3} <- @add({temp_wire_1}, {temp_wire_2});')

            temp_wire_1 = next_wire()
            emit(f'  {temp_wire_1} <- @mulc({wire_name_for_diff}, < {c} >);')
            temp_wire_3 = next_wire()
            emit(f'  {temp_wire_3} <- @add({temp_wire_2}, {temp_wire_1});')

            emit(f'  @assert_zero({temp_wire_3});')
            return r_res
        elif e.op == 'sub':
            # implementation: multiply x2 by -1
            e1, e2 = e.args
            x1 = print_exp_ir1(e1)
            x2 = print_exp_ir1(e2)
            negated_x2 = next_wire()
            c = params['arithmetic_field'] - 1
            emit(f'  {negated_x2} <- @mulc({x2}, < {c} >);')

            r = next_wire()

            emit(f'  {r} <- @add({x1}, {negated_x2});')
            return r
        elif e.op == 'and':
            e1, e2 = e.args
            x1 = print_exp_ir1(e1)
            x2 = print_exp_ir1(e2)
            r = next_wire()
            emit(f'  {r} <- @mul({x1}, {x2});')
            return r
        elif e.op == 'not':
            e1 = e.args
            x1 = print_exp_ir1(e1)
            negated_x2 = next_wire()
            c = params['arithmetic_field'] - 1
            emit(f'  {negated_x2} <- @mulc({x1}, < {c} >);')
            r = next_wire()
            emit(f'  {r} <- @add({negated_x2}, < {1} >);')
            return r
        elif e.op == 'assert0':
            assert len(e.args) == 1
            x1 = print_exp_ir1(e.args[0])
            emit(f'  @assert_zero({x1});')
            return None
        else:
            raise Exception(f'unknown operator: {e.op}')
    else:
        raise Exception(f'unknown expression type: {e}')

def print_ir0(filename):
    global IR_MODE
    IR_MODE = 0
    print_ir1(filename)
    IR_MODE = 1

def print_ir1(filename):
    global all_defs
    global emp_output_string

    field = params['arithmetic_field']
    print('field size:', field)

    # INSTANCE OUTPUT
    emp_output_string = ""

    emit(f"""version 1.0.0;
field characteristic {field} degree 1;
instance
@begin
@end
""")

    with open(filename + '.ins', 'w') as f:
        f.write(emp_output_string)


    # RELATION OUTPUT
    emp_output_string = ""

    emit(f"""version 1.0.0;
field characteristic {field} degree 1;
relation
gate_set: arithmetic;
features: @function, @switch;
@begin""")

    for a in assertions:
        print_exp_ir1(a)

    emit('@end')

    with open(filename + '.rel', 'w') as f:
        f.write(emp_output_string)

    # WITNESS OUTPUT
    emp_output_string = ""

    emit(f"""version 1.0.0;
field characteristic {field} degree 1;
short_witness
@begin""")

    for x in witness_list:
        emit(f'< {x.val} >;')

    emit("@end")

    with open(filename + '.wit', 'w') as f:
        f.write(emp_output_string)

    emp_output_string = ""

