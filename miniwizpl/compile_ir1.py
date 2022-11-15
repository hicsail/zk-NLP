import sys
import numpy as np
from dataclasses import dataclass
from collections import defaultdict
import os
from .globals import *
from .expr import *
from .data_types import *
import sys

sys.setrecursionlimit(10000)

output_file = None
emp_output_string = ""
current_wire = 0
witness_list = []
IR_MODE = 1
WRITE_TO_WIT = 1
WRITE_TO_REL = 1

@dataclass
class WireVal(AST):
    name: str
    type: type
    val: any

    def __eq__(self, other):
        return Prim('equals', [self, other], val_of(self) == val_of(other))
    def __req__(self, other):
        return Prim('equals', [other, self], val_of(other) == val_of(self))
    def __str__(self):
        return f'WireVal({self.name}, {self.val})'
    __repr__ = __str__


def next_wire():
    global current_wire
    r = current_wire
    current_wire += 1
    return '$' + str(r)

def emit(s=''):
    global output_file
    if WRITE_TO_REL == 1:
        output_file.write(s)
        output_file.write('\n')
    
    # global emp_output_string
    # emp_output_string += s + '\n'

def add_to_witness(obj, comment=None):
    wire_name = str(next_wire())
    if WRITE_TO_WIT == 1:
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


function_unrollings = defaultdict(int)
exp_cache = {}


def print_exp_ir1(e):
    global exp_cache
    if id(e) in exp_cache:
        return exp_cache[id(e)]
    else:
        r = print_exp_ir1_(e)
        exp_cache[id(e)] = r
        return r

def print_exp_ir1_(e):
    global all_pubvals
    global params
    global current_wire
    global WRITE_TO_REL
    global WRITE_TO_WIT

    if isinstance(e, (SecretArray, SecretTensor, SecretInt, SymVar)):
        return add_to_witness(e)

    elif isinstance(e, WireVal):
        # just return the wire name
        return e.name

    elif isinstance(e, np.int64):
        r = next_wire()
        emit(f'  {r} <- < {e} >;')
        return r

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
        elif e.op == 'rec':
            name, bound, args, func = e.args
            if function_unrollings[name] > bound:
                r = next_wire()
                emit(f'  {r} <- < 0 >;')
                return r
            else:
                function_unrollings[name] += 1
                arg_wires = []
                for a in args:
                    w = print_exp_ir1(a)
                    wv = WireVal(w, int, val_of(a))
                    arg_wires.append(wv)

                body = func(*arg_wires)
                r = print_exp_ir1(body)
                return r
        elif e.op == 'fold':
            xs, f, init = e.args
            assert isinstance(xs, SecretList)

            if IR_MODE == 1:
                xs_wires = [print_exp_ir1(SecretInt(x)) for x in val_of(xs)]
                init_wire = next_wire()
                emit(f'  {init_wire} <- < {init} >;')

                r1 = xs_wires[0]
                rf = xs_wires[-1]
                wires = [next_wire() for _ in range(0, len(val_of(xs))+1)]
                x_wire_val = WireVal('$1', int, None)
                a_wire_val = WireVal('$2', int, None)

                # step 1: create the "abstracted" loop body with anonymous function's inputs
                # we want this step to output code to the .rel file
                # we want this step to NOT output anything to the .wit file
                WRITE_TO_REL = 1
                WRITE_TO_WIT = 0
                loop_body = f(a_wire_val, x_wire_val)

                emit(f' {wires[0]}...{wires[-1]} <- @for i @first {0} @last {len(val_of(xs))}')
                emit(f'   $(i+{len(val_of(xs)) + 1}) <- @anon_call($i, $(i + {len(val_of(xs))}), @instance: 0, @short_witness : 0)')
                ocw = current_wire
                current_wire = 3
                output_wire = print_exp_ir1(loop_body)
                current_wire = ocw
                emit(f'   $0 <- {output_wire};')
                emit(f'   @end')
                emit(f' @end')

                # step 2: run the loop "concretely" with actual values instead of abstracted function inputs
                # we want this step to output witness values to the .wit file
                # we want this step to NOT output anything to the .rel file

                WRITE_TO_REL = 0
                WRITE_TO_WIT = 1
                a_val = val_of(init)
                x_wire_vals = [WireVal(n, int, v) for n, v in zip(xs_wires, val_of(xs))]
                for x_val in x_wire_vals:
                    a_val = f(x_val, val_of(a_val))
                    print_exp_ir1(a_val)

                WRITE_TO_REL = 1
                return r1
            elif IR_MODE == 0:
                a_wire_name = print_exp_ir1(init)
                a_wire_val = WireVal(a_wire_name, int, val_of(init))
                for x_val in val_of(xs):
                    new_a_val = f(SecretInt(x_val), a_wire_val)
                    add_to_witness(new_a_val)
                    a_wire_name = print_exp_ir1(new_a_val)
                    a_wire_val = WireVal(a_wire_name, int, val_of(new_a_val))
                return a_wire_name

            else:
                raise RuntimeError('unknown IR mode:', IR_MODE)
        elif e.op == 'mux':
            e1, e2, e3 = e.args
            x1 = print_exp_ir1(e1)
            x2 = print_exp_ir1(e2)
            x3 = print_exp_ir1(e3)
            c = params['arithmetic_field'] - 1
            r1 = next_wire()
            emit(f'  {r1} <- @mul({x1}, {x2});')
            r2 = next_wire()
            emit(f'  {r2} <- @mulc({x1}, < {c} >);')
            r4 = next_wire()
            emit(f'  {r4} <- @addc({r2}, < {1} >);')
            r3 = next_wire()
            emit(f'  {r3} <- @mul({r4}, {x3});')
            r_val = next_wire()
            emit(f'  {r_val} <- @add({r1}, {r3});')
            return r_val
        elif e.op == 'equals':
            e1, e2 = e.args
            x1 = print_exp_ir1(e1)
            x2 = print_exp_ir1(e2)
            diff = e1 - e2
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
            emit(f'  {temp_wire_2} <- @mul({wire_name_for_diff}, {temp_wire_1});')

            temp_wire_1 = next_wire()
            emit(f'  {temp_wire_1} <- @mul({temp_wire_2}, {wire_name_for_res});')

            temp_wire_2 = next_wire()
            emit(f'  {temp_wire_2} <- @mulc({wire_name_for_res}, < {c} >);')
            temp_wire_3 = next_wire()
            emit(f'  {temp_wire_3} <- @add({temp_wire_1}, {temp_wire_2});')

            temp_wire_1 = next_wire()
            emit(f'  {temp_wire_1} <- @mulc({wire_name_for_diff}, < {c} >);')
            temp_wire_4 = next_wire()
            emit(f'  {temp_wire_4} <- @add({temp_wire_3}, {temp_wire_1});')

            emit(f'  @assert_zero({temp_wire_4});')
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
        elif e.op == 'exp_mod':
            a, b, p = e.args
            # TODO: need to check p here
            # we assume p is our current field, so just do a*a b times
            assert isinstance(b, int)
            a_wire = print_exp_ir1(a)
            result_wire = a_wire
            for _ in range(b):
                r = next_wire()
                emit(f'  {r} <- @mul({a_wire}, {result_wire});')
                result_wire = r
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
    global current_wire
    current_wire = 0
    IR_MODE = 0
    print_ir1(filename)
    IR_MODE = 1

def print_ir1(filename):
    global all_defs
    global output_file
    global current_wire
    current_wire = 0

    field = params['arithmetic_field']
    print('field size:', field)

    # INSTANCE OUTPUT
    with open(filename + '.ins', 'w') as f:
        output_file = f

        emit(f"""version 1.0.0;
field characteristic {field} degree 1;
instance
@begin
@end
""")


    # RELATION OUTPUT
    with open(filename + '.rel', 'w') as f:
        output_file = f

        emit(f"""version 1.0.0;
field characteristic {field} degree 1;
relation
gate_set: arithmetic;
features: @function, @for, @switch;
@begin""")

        for a in assertions:
            print_exp_ir1(a)

        emit('@end')

    # WITNESS OUTPUT
    with open(filename + '.wit', 'w') as f:
        output_file = f
        emp_output_string = ""

        emit(f"""version 1.0.0;
field characteristic {field} degree 1;
short_witness
@begin""")

        for x in witness_list:
            emit(f'< {x.val} >;')

        emit("@end")


