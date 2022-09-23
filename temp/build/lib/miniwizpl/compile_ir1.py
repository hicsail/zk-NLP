import sys
import numpy as np
from dataclasses import dataclass
import os
from .globals import *
from .expr import *
from .data_types import *

emp_output_string = ""
witness_map = []
current_wire = 0

def next_wire():
    global current_wire
    r = current_wire
    current_wire += 1
    return '$' + str(r)

def emit(s=''):
    global emp_output_string
    emp_output_string += s + '\n'

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
        if e.name in witness_map:
            return '$' + str(witness_map.index(e.name))
        else:
            raise Exception(f'Secret value is not part of witness: {e}')
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





def print_defs_ir1(defs):
    for i, d in enumerate(defs):
        name = d.name
        x = d.val

        if isinstance(d, SecretInt):
            # TODO: deal with big ints
            emit(f'< {x} >;')
            witness_map.append(name)


def print_ir1(filename):
    global all_defs
    global emp_output_string

    field = params['arithmetic_field']
    print('field size:', field)

    # WITNESS OUTPUT
    emp_output_string = ""

    emit(f"""version 1.0.0;
field characteristic {field} degree 1;
short_witness
@begin""")

    print_defs_ir1(all_defs)

    emit("@end")

    with open(filename + '.wit', 'w') as f:
        f.write(emp_output_string)

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

    for _ in range(len(witness_map)):
        emit(f'  {next_wire()} <- @short_witness;')

    for a in assertions:
        print_exp_ir1(a)

    emit('@end')

    with open(filename + '.rel', 'w') as f:
        f.write(emp_output_string)

    emp_output_string = ""
