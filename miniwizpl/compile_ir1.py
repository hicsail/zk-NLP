import sys
import numpy as np
from dataclasses import dataclass
import os
from .globals import *
from .expr import *
from .data_types import *

emp_output_string = ""
current_wire = 0
witness_list = []

def next_wire():
    global current_wire
    r = current_wire
    current_wire += 1
    return '$' + str(r)

def emit(s=''):
    global emp_output_string
    emp_output_string += s + '\n'

def add_to_witness(obj):
    wire_name = '$' + str(next_wire())
    witness_list.append(obj)
    emit(f'  {wire_name} <- @short_witness;')

    return wire_name

int_ops_ir1 = {
    'add': 'add',
    'mul': 'mul',
    'div': 'div',
    'mod': 'mod'
}


def print_exp_ir1(e):
    global all_pubvals
    global params

    if isinstance(e, (SecretArray, SecretTensor, SecretInt, SymVar)):
        return add_to_witness(e)

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
        elif e.op == 'mux':
            # todo
            pass
        elif e.op == 'equals':
            # todo
            # diff_inv = ???
            # wire_name_for_diff_inv = add_to_witness(diff_inv)
            pass
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
        elif e.op == 'assert0':
            assert len(e.args) == 1
            x1 = print_exp_ir1(e.args[0])
            emit(f'  @assert_zero({x1});')
            return None
        else:
            raise Exception(f'unknown operator: {e.op}')
    else:
        raise Exception(f'unknown expression type: {e}')


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

