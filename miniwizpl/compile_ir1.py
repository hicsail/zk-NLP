import sys
import numpy as np
from dataclasses import dataclass
import os
from .utils import *
from .globals import *
from .expr import *

emp_output_string = ""
witness_map = []
current_wire = 0

def emit(s=''):
    global emp_output_string
    emp_output_string += s + '\n'

int_ops_ir1 = {
    'add': 'add',
    'sub': 'sub',
    'mul': 'mul',
    'div': 'div',
    'mod': 'mod'
}


def print_exp_ir1(e):
    global all_pubvals
    global current_wire
    if isinstance(e, (SecretArray, SecretTensor, SecretInt, SymVar)):
        return '$' + str(witness_map.index(e.name))
    elif isinstance(e, int):
        raise Exception(e)
    elif isinstance(e, Prim):
        if e.op in int_ops_ir1:
            e1, e2 = e.args
            x1 = print_exp_ir1(e1)
            x2 = print_exp_ir1(e2)
            op_sym = int_ops_ir1[e.op]
            r = '$' + str(current_wire)
            current_wire += 1

            emit(f'  {r} <- @{op_sym}({x1}, {x2});')
            return r
        elif e.op == 'assert0':
            assert len(e.args) == 1
            x1 = print_exp_ir1(e.args[0])
            emit(f'  @assert_zero({x1});')
            return None
        else:
            raise Exception(e)
    else:
        raise Exception(e)





def print_defs_ir1(defs):
    for i, d in enumerate(defs):
        name = d.name
        x = d.val()

        if isinstance(d, SecretInt):
            # TODO: deal with big ints
            emit(f'< {x} >;')
            witness_map.append(name)


def print_ir1(filename):
    global all_defs
    global emp_output_string
    global current_wire

    emp_output_string = ""

    emit("""version 1.0.0;
field characteristic 97 degree 1;
short_witness
@begin""")

    print_defs_ir1(all_defs)

    emit("@end")

    with open(filename + '.wit', 'w') as f:
        f.write(emp_output_string)


    emp_output_string = ""

    emit("""version 1.0.0;
field characteristic 97 degree 1;
relation
gate_set: arithmetic;
features: @function, @switch;
@begin""")

    for i in range(len(witness_map)):
        emit(f'  ${i} <- @short_witness;')
    current_wire = i+1

    for a in assertions:
        print_exp_ir1(a)

    emit('@end')

    with open(filename + '.rel', 'w') as f:
        f.write(emp_output_string)

    emp_output_string = ""
