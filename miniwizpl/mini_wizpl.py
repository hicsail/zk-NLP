import sys
import numpy as np
from dataclasses import dataclass
import os
from .globals import *
from .expr import *

emp_output_string = ""
bitwidth = 32

def eval(e):
    if isinstance(e, SecretArray):
        return e.arr
    elif isinstance(e, Prim):
        if e.op == 'relu':
            x = eval(e.args[0])
            return x * (x > 0)
        elif e.op == 'matmul':
            e1, e2 = e.args
            return eval(e1) @ eval(e2)
        else:
            raise Exception(e)
    else:
        raise Exception(e)

def emit(s=''):
    global emp_output_string
    emp_output_string += s + '\n'

def print_exp(e):
    if isinstance(e, (SecretArray, SecretTensor, SecretInt)):
        return e.name
    elif isinstance(e, int):
        r = gensym('public_intval')

        if bitsof(e) < 32:
            emit(f'  Integer {r} = Integer({bitwidth}, {e}, PUBLIC);')
            emit()
            return r
        else:
            emit_bigint(r, e)
            return r

    elif isinstance(e, Prim):
        if e.op == 'relu':
            x = print_exp(e.args[0])
            r = gensym('result_mat')
            emit(f'  QSMatrix<Float> {r} = relu({x});')
            emit()
            return r
        elif e.op == 'softmax':
            x = print_exp(e.args[0])
            r = gensym('result_mat_softmax')
            emit(f'  QSMatrix<Float> {r} = {x};')
            emit()
            return r
        elif e.op == 'matmul':
            e1, e2 = e.args
            x1 = print_exp(e1)
            x2 = print_exp(e2)
            r = gensym('result_mat')

            emit(f'  QSMatrix<Float> {r} = {x1} * {x2};')
            return r
        elif e.op == 'matplus':
            e1, e2 = e.args
            x1 = print_exp(e1)
            x2 = print_exp(e2)
            r = gensym('result_mat')

            emit(f'  QSMatrix<Float> {r} = {x1} + {x2};')
            emit()
            return r
        elif e.op == 'mul':
            e1, e2 = e.args
            x1 = print_exp(e1)
            x2 = print_exp(e2)
            r = gensym('result_intval')

            emit(f'  Integer {r} = {x1} * {x2};')
            emit()
            return r
        elif e.op == 'add':
            e1, e2 = e.args
            x1 = print_exp(e1)
            x2 = print_exp(e2)
            r = gensym('result_intval')

            emit(f'  Integer {r} = {x1} * {x2};')
            emit()
            return r

        elif e.op == 'mod':
            e1, e2 = e.args
            x1 = print_exp(e1)
            x2 = print_exp(e2)
            r = gensym('result_intval')

            emit(f'  Integer {r} = {x1} % {x2};')
            emit()
            return r
        elif e.op == 'exp_mod':
            e1, e2, e3 = e.args
            x1 = print_exp(e1)
            x2 = print_exp(e2)
            x3 = print_exp(e3)
            r = gensym('result_intval')

            emit(f'  Integer {r} = {x1}.modExp({x2}, {x3});')
            emit()
            return r
        elif e.op == 'cat':
            e1, e2, e3 = e.args
            x1 = print_exp(e1)
            x2 = print_exp(e2)
            assert isinstance(e3, int)
            dim = e3
            r = gensym('result_mat')

            emit(f'  QSMatrix<Float> {r} = {x1}.concatenate({x2}, {dim});')
            emit()
            return r
        else:
            raise Exception(e)
    else:
        raise Exception(e)

def bitsof(n):
    bits = 1
    while 2**bits < n:
        bits += 1
        if bits > 10000:
            raise Exception(f'Too many bits! {n}')
    return bits

def emit_bigint(r, e):
    bin_str = "{0:b}".format(e)
    bin_arry = '{' + ','.join(bin_str) + '}'

    emit(f'  bool {r}_init[] = {bin_arry};')
    emit(f'  vector<Bit> {r}_vec;')
    emit(f'  for (int i = 0; i < {len(bin_str)}; ++i)')
    emit(f'    {r}_vec.push_back(Bit({r}_init[i], PUBLIC));')
    emit(f'  Integer {r} = Integer({r}_vec);')
    emit(f'  {r}.resize({bitwidth});')
    emit()


def print_defs(defs):
    global bitwidth

    for d in defs:
        name = d.name
        x = d.val()

        if isinstance(d, SecretInt):
            if bitsof(x) < 32:
                emit(f'  Integer {name} = Integer({bitwidth}, {x}, ALICE);')
                emit()
            else:
                emit_bigint(name, x)
        elif isinstance(d, (SecretTensor, SecretArray)):
            e2s = x.shape
            if len(e2s) == 1:
                n1 = 1
                n2 = e2s[0]
            elif len(e2s) == 2:
                n1 = e2s[0]
                n2 = e2s[1]
            else:
                raise Exception(f'unsupported array shape: {e2s}')

            p = f"""
float {name}_init[{n1}][{n2}] = {print_mat(x)};
QSMatrix<Float> {name}({n1}, {n2}, pub_zero);
for (int i = 0; i < {n1}; ++i)
  for (int j = 0; j < {n2}; ++j) {{
    {name}(i, j) = Float({name}_init[i][j], ALICE);
}}
"""
            emit(p)
        else:
            raise Exception(f'unsupported secret type: {type(d)}')


def print_mat(x):
    # convert x into a numpy array
    typ = type(x).__name__
    if typ == 'ndarray':
        pass
    elif typ in ['Tensor', 'Parameter']:
        x = x.detach().numpy()
    else:
        raise Exception(f'unsupported array type: {typ}')

    # print out the numpy array
    if len(x.shape) == 1:
        return '{{' + ', '.join([str(i) for i in x]) + '}}'

    elif len(x.shape) == 2:
        return '{' + ', '.join(['{' + ', '.join([str(x) for x in row]) + '}'
                            for row in x]) + '}'
    else:
        raise Exception(f'unsupported array shape: {x.shape}')

def set_bitwidth(b):
    global bitwidth
    bitwidth = b

def print_emp(outp, filename):
    global all_defs
    global emp_output_string

    with open(os.path.dirname(__file__) + '/boilerplate/mini_wizpl_top.cpp', 'r') as f1:
        top_boilerplate = f1.read()
            
    emit(top_boilerplate)

    print_defs(all_defs)
    emit()
    emit('  cout << "defs complete\\n";')
    emit()
    print_exp(outp)

    with open(os.path.dirname(__file__) + '/boilerplate/mini_wizpl_bottom.cpp', 'r') as f2:
        bottom_boilerplate = f2.read()
            
    emit(bottom_boilerplate)

    with open(filename, 'w') as f:
        f.write(emp_output_string)

