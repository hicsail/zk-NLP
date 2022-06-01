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
assertions = []

int_ops = {
    'add': '+',
    'sub': '-',
    'mul': '*',
    'div': '/',
    'mod': '%'
}

bool_ops = {
    'and': '&',
    'or': '|'
    }

def emit(s=''):
    global emp_output_string
    emp_output_string += s + '\n'

def print_exp(e):
    global all_pubvals
    if isinstance(e, (SecretList, SecretIndexList, SecretArray, SecretTensor, SecretInt, SymVar)):
        return e.name
    elif isinstance(e, int):
        if e in all_pubvals:
            return all_pubvals[e]
        else:
            r = gensym('public_intval')
            all_pubvals[e] = r

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
        elif e.op == 'mux':
            arg_names = [print_exp(a) for a in e.args]
            args = ', '.join(arg_names)
            r = gensym('result_int')
            emit(f'  Integer {r} = mux({args});')
            emit()
            return r
        elif e.op == 'softmax':
            x = print_exp(e.args[0])
            r = gensym('result_mat_softmax')
            emit(f'  QSMatrix<Float> {r} = softmax({x});')
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
        elif e.op == 'round':
            x = print_exp(e.args[0])
            r = gensym('result_int')
            emit(f'  Integer {r} = {x}; // round as no-op')
            emit()
            return r
        elif e.op == 'listref':
            e1, e2 = e.args
            x1 = print_exp(e1)
            x2 = print_exp(e2)
            r = gensym('listref_result')

            emit(f'  Integer {r} = {x1}->read({x2});')
            return r
        elif e.op == 'listset':
            e1, e2, e3 = e.args
            x1 = print_exp(e1)
            x2 = print_exp(e2)
            x3 = print_exp(e3)

            emit(f'  {x1}->write({x2}, {x3});')
            return None
        elif e.op in int_ops:
            e1, e2 = e.args
            x1 = print_exp(e1)
            x2 = print_exp(e2)
            op_sym = int_ops[e.op]
            r = gensym('result_intval')

            emit(f'  Integer {r} = {x1} {op_sym} {x2};')
            emit()
            return r
        elif e.op in bool_ops:
            e1, e2 = e.args
            x1 = print_exp(e1)
            x2 = print_exp(e2)
            op_sym = bool_ops[e.op]
            r = gensym('result_bitval')

            emit(f'  Bit {r} = {x1} {op_sym} {x2};')
            emit()
            return r
        elif e.op == 'equals':
            e1, e2 = e.args
            x1 = print_exp(e1)
            x2 = print_exp(e2)
            r = gensym('result_intval')

            emit(f'  Bit {r} = {x1} == {x2};')
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
        elif e.op == 'fold':
            x, body, accum, xs, init = e.args

            assert isinstance(x, SymVar)
            assert isinstance(accum, SymVar)
            assert isinstance(xs, SecretList)

            a = print_exp(init)
            emit(f'Integer {accum.name} = {a};')

            emit(f'for (Integer {x.name} : {xs.name}) {{')
            output = print_exp(body)
            emit(f'  {accum.name} = {output};')
            emit('}')
            return accum.name
        else:
            raise Exception(e)
    else:
        raise Exception(e)


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
        elif isinstance(d, (SecretList)):
            n1 = len(d.arr)
            p = f"""
  static int {name}_init[] = {print_list(x)};
  vector<Integer> {name};
  for (int i = 0; i < {n1}; ++i)
    {name}.push_back(Integer(32, {name}_init[i], ALICE));
"""
            emit(p)
        elif isinstance(d, (SecretIndexList)):
            n1 = len(d.arr)
            p = f"""
  static int {name}_init[] = {print_list(x)};
  ZKRAM<BoolIO<NetIO>> *{name} = new ZKRAM<BoolIO<NetIO>>(party, index_sz, step_sz, val_sz);
  for (int i = 0; i < {n1}; ++i)
    {name}->write(Integer(index_sz, i, PUBLIC), Integer(32, {name}_init[i], ALICE));
"""
            emit(p)
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

def print_list(x):
    return '{' + ', '.join([str(i) for i in x]) + '}'

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

def print_ram_checks(defs):
    for d in defs:
        name = d.name
        x = d.val()

        if isinstance(d, (SecretIndexList)):
            emit(f'  {name}->check();')

def print_emp(outp, filename):
    global all_defs
    global emp_output_string
    global all_statements

    with open(os.path.dirname(__file__) + '/boilerplate/mini_wizpl_top.cpp', 'r') as f1:
        top_boilerplate = f1.read()
            
    emit(top_boilerplate)

    emit('  cout << "starting defs\\n";')
    print_defs(all_defs)
    emit()
    emit('  cout << "defs complete\\n";')
    emit()
    for s in all_statements:
        print_exp(s)
    final_output_var = print_exp(outp)
    emit(f'  int final_result = {final_output_var}.reveal<int>(PUBLIC);')
    emit('  cout << "final result:" << final_result << "\\n";')
    emit()

    print_ram_checks(all_defs)
    

    with open(os.path.dirname(__file__) + '/boilerplate/mini_wizpl_bottom.cpp', 'r') as f2:
        bottom_boilerplate = f2.read()
            
    emit(bottom_boilerplate)

    with open(filename, 'w') as f:
        f.write(emp_output_string)
