import sys
import numpy as np
from dataclasses import dataclass
import os
from .globals import *
from .expr import *
from .utils import *
from .data_types import *

emp_output_string = ""
witness_output_string = ""
witness_map = []
current_wire = 0
assertions = []

prim_ops = {
    'relu': 'relu',
    'mux': 'mux',
    'log_softmax': 'log_softmax',
    'round': 'round',
}

bin_ops = {
    'add': '+',
    'sub': '-',
    'mul': '*',
    'div': '/',
    'mod': '%',
    'matmul': '*',
    'matplus': '+',
    'lt': '<',
    'gt': '>',
    'lte': '<=',
    'gte': '>=',
    'equals': '==',
    'not_equals': '!=',
    'and': '&',
    'or': '|'
    }

output_types = {
    'round': 'Integer',
    'add': 'Integer',
    'sub': 'Integer',
    'mul': 'Integer',
    'div': 'Integer',
    'mod': 'Integer',
    'lt': 'Bit',
    'gt': 'Bit',
    'lte': 'Bit',
    'gte': 'Bit',
    'equals': 'Bit',
    'not_equals': 'Bit',
    'relu': 'QSMatrix<Float>',
    'mux': 'Integer',
    'log_softmax': 'QSMatrix<Float>',
    'matmul': 'QSMatrix<Float>',
    'matplus': 'QSMatrix<Float>',
    'and': 'Bit',
    'or': 'Bit',
    }

def emit(s=''):
    global emp_output_string
    emp_output_string += s + '\n'

def emit_witness(s=''):
    global witness_output_string
    witness_output_string += s + '\n'

def print_exp(e):
    global all_pubvals
    if isinstance(e, (SecretList, SecretIndexList, SecretArray, SecretStack,
                      SecretTensor, SecretInt, SymVar, PublicTensor)):
        return e.name
    elif isinstance(e, bool):
        if e in all_pubvals:
            return all_pubvals[e]
        else:
            ss = str(e).replace('-', 'minus')
            r = f'public_bit_{ss}'
            all_pubvals[e] = r
            emit(f'  Bit {r} = Bit({int(e)}, PUBLIC);')
            emit()
            return r
    elif isinstance(e, int):
        if e in all_pubvals:
            return all_pubvals[e]
        else:
            ss = str(e).replace('-', 'minus')
            r = f'public_int_{ss}'
            all_pubvals[e] = r

            if bitsof(e) < 32:
                bw = params['bitwidth']
                emit(f'  Integer {r} = Integer({bw}, {e}, PUBLIC);')
                emit()
                return r
            else:
                emit_bigint(r, e)
                return r

    elif isinstance(e, Prim):
        if e.op in prim_ops:
            xs = [print_exp(a) for a in e.args]
            ns = ', '.join(xs)
            r = gensym('result')
            t = output_types[e.op]
            op = prim_ops[e.op]

            emit(f'  {t} {r} = {op}({ns});')
            return r
        elif e.op in bin_ops:
            e1, e2 = e.args
            x1 = print_exp(e1)
            x2 = print_exp(e2)
            r = gensym('result')
            t = output_types[e.op]
            op = bin_ops[e.op]

            emit(f'  {t} {r} = {x1} {op} {x2};')
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
        elif e.op == 'neg':
            assert len(e.args) == 1
            e1 = e.args[0]
            x1 = print_exp(e1)
            r = gensym('result_bitval')
            emit(f'  Bit {r} = !{x1};')
            emit()
            return r
        elif e.op == 'not':
            assert len(e.args) == 1
            e1 = e.args[0]
            x1 = print_exp(e1)
            r = gensym('result_bitval')
            emit(f'  Bit {r} = !{x1};')
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
            xs, f, init = e.args

            assert isinstance(xs, SecretList)

            x = SymVar(gensym('x'), int, None)
            accum = SymVar(gensym('a'), int, None)
            body = f(x, accum)

            a = print_exp(init)
            emit(f'Integer {accum.name} = {a};')

            old_pubvals = all_pubvals.copy()
            emit(f'for (Integer {x.name} : {xs.name}) {{')
            output = print_exp(body)
            emit(f'  {accum.name} = {output};')
            emit('}')
            all_pubvals = old_pubvals

            return accum.name

        elif e.op == 'compare_tensors':
            e1, e2 = e.args
            x1 = print_exp(e1)
            x2 = print_exp(e2)
            emit(f'  assert(compare_qs_matrices({x1}, {x2}));')
        elif e.op == 'assert0EMP':
            e1 = e.args[0]
            x1 = print_exp(e1)
            emit(f'  assert(assert0EMP({x1}));')
            return x1
        elif e.op == 'assertTrueEMP':
            e1 = e.args[0]
            x1 = print_exp(e1)
            emit(f'  assert({x1}.reveal<bool>(PUBLIC));')
            return x1
        elif e.op == 'assertFalseEMP':
            e1 = e.args[0]
            x1 = print_exp(e1)
            emit(f'  assert(!{x1}.reveal<bool>(PUBLIC));')
            return x1
        elif e.op == 'stack_pop':
            assert len(e.args) == 1
            e1 = e.args[0]
            x1 = print_exp(e1)

            # unconditional; address should always be ok
            r = gensym('stack_val')
            #emit(f'  cout << "P" << party << " stack POP, old top: " << {x1}_top.reveal<int>(PUBLIC) << "\\n";')
            emit(f'  Integer {r} = {x1}->read({x1}_top);')
            emit(f'  {x1}_top = {x1}_top - Integer(32, 1, ALICE);')
            #emit(f'  cout << "P" << party << " stack POP, new top: " << {x1}_top.reveal<int>(PUBLIC) << "\\n";')
            return r
        elif e.op == 'stack_push':
            e1, e2 = e.args
            x1 = print_exp(e1)
            x2 = print_exp(e2)

            emit(f'  {x1}_top = {x1}_top + Integer(32, 1, ALICE);')
            emit(f'  {x1}->write({x1}_top, {x2});')
            return None
        elif e.op == 'stack_cond_push':
            # stack, cond, val
            e1, e2, e3 = e.args
            x1 = print_exp(e1)
            x2 = print_exp(e2)
            x3 = print_exp(e3)
            a = gensym('cond_addr')

            # conditional, address might be out of range!
            #emit(f'  cout << "P" << party << " stack PUSH, old top: " << {x1}_top.reveal<int>(PUBLIC) << " condition: " << {x2}.reveal<bool>(PUBLIC) << "\\n";')

            emit(f'  {x1}_top = mux({x2}, {x1}_top + Integer(32, 1, ALICE), {x1}_top);')
            emit(f'  Integer {a} = mux({x2}, {x1}_top, Integer(32, 0, ALICE));')
            emit(f'  {x1}->write({a}, mux({x2}, {x3}, {x1}->read({a})));')

            #emit(f'  cout << "P" << party << " stack PUSH, new top: " << {x1}_top.reveal<int>(PUBLIC) << " condition: " << {x2}.reveal<bool>(PUBLIC) << "\\n";')
            return None
        elif e.op == 'assign':
            e1, e2 = e.args
            assert isinstance(e1, SymVar)
            x1 = e1.name
            x2 = print_exp(e2)
            emit(f'  Integer {x1} = {x2};')
            return None
        elif e.op == 'listindex':
            # array, val, start, length
            e1, e2, e3, e4 = e.args
            assert isinstance(e4, int)
            x1 = print_exp(e1)
            x2 = print_exp(e2)
            x3 = print_exp(e3)
            r = gensym('listidx_result')

            emit(f'  Integer {r} = Integer(32, -1, PUBLIC);')
            emit(f'  for (int i = 0; i < {e4}; i++) {{')
            emit(f'    Integer idx = Integer(32, i, PUBLIC);')
            emit(f'    Integer val = {x1}->read({x3} + idx);')
            emit(f'    {r} = mux(val == {x2}, idx, {r});')
            emit(f'  }}')

            return r
        elif e.op == 'comment':
            emit()
            emit(f'  // COMMENT: {e.args[0]}')
        elif e.op == 'log_val':
            t, msg, val = e.args
            xv = print_exp(val)
            x = gensym('log_val')

            if t == int:
                emit(f'  int {x} = {xv}.reveal<int>(PUBLIC);')
                emit(f'  cout << "P" << party << " {msg}: " << {x} << "\\n";')
            elif t == bool:
                emit(f'  bool {x} = {xv}.reveal<bool>(PUBLIC);')
                emit(f'  cout << "P" << party << " {msg}:" << {x} << "\\n";')
            else:
                raise Exception(e)
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
    bw = params['bitwidth']
    emit(f'  {r}.resize({bw});')
    emit()


def print_defs(defs):
    for d in defs:
        name = d.name
        x = d.val

        if isinstance(d, SecretInt):
            if bitsof(x) < 32:
                bw = params['bitwidth']

                emit(f'  Integer {name} = Integer({bw}, {x}, ALICE);')
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
            print_witness(x)
#             p = f"""
#   static int {name}_init[] = {print_list(x)};
#   ZKRAM<BoolIO<NetIO>> *{name} = new ZKRAM<BoolIO<NetIO>>(party, index_sz, step_sz, val_sz);
#   for (int i = 0; i < {n1}; ++i)
#     {name}->write(Integer(index_sz, i, PUBLIC), Integer(32, {name}_init[i], ALICE));
# """
            p = f"""
  ZKRAM<BoolIO<NetIO>> *{name} = new ZKRAM<BoolIO<NetIO>>(party, index_sz, step_sz, val_sz);
  for (int i = 0; i < {n1}; ++i) {{
    is >> tmp;
    {name}->write(Integer(index_sz, i, PUBLIC), Integer(32, tmp, ALICE));
  }}
"""
            emit(p)
        elif isinstance(d, (SecretStack)):
            n1 = len(d.arr)
            print_witness(x)
#             p = f"""
#   static int {name}_init[] = {print_list(x)};
#   ZKRAM<BoolIO<NetIO>> *{name} = new ZKRAM<BoolIO<NetIO>>(party, index_sz, step_sz, val_sz);
#   for (int i = 0; i < {n1}; ++i)
#     {name}->write(Integer(index_sz, i, PUBLIC), Integer(32, {name}_init[i], ALICE));
#   Integer {name}_top = Integer(32, {n1-1}, ALICE);
# """
            p = f"""
  ZKRAM<BoolIO<NetIO>> *{name} = new ZKRAM<BoolIO<NetIO>>(party, index_sz, step_sz, val_sz);
  for (int i = 0; i < {n1}; ++i) {{
    is >> tmp;
    {name}->write(Integer(index_sz, i, PUBLIC), Integer(32, tmp, ALICE));
  }}
  Integer {name}_top = Integer(32, {n1-1}, ALICE);
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
        elif isinstance(d, PublicTensor):
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
QSMatrix<float> {name}({n1}, {n2}, 0);
for (int i = 0; i < {n1}; ++i)
  for (int j = 0; j < {n2}; ++j) {{
    {name}(i, j) = {name}_init[i][j];
}}
"""
            emit(p)
        else:
            raise Exception(f'unsupported secret type: {type(d)}')

def print_witness(x):
    for e in x:
        emit_witness(str(e))

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
        x = d.val

        if isinstance(d, (SecretIndexList, SecretStack)):
            emit(f'  {name}->check();')

def print_emp(filename):
    global all_defs
    global emp_output_string
    global witness_output_string
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

    # if isinstance(outp.val, bool):
    #     emit(f'  bool final_result = {final_output_var}.reveal<bool>(PUBLIC);')
    #     emit('  cout << "final result:" << final_result << "\\n";')
    #     emit()
    # elif isinstance(outp.val, int):
    #     emit(f'  int final_result = {final_output_var}.reveal<int>(PUBLIC);')
    #     emit('  cout << "final result:" << final_result << "\\n";')
    #     emit()

    print_ram_checks(all_defs)


    with open(os.path.dirname(__file__) + '/boilerplate/mini_wizpl_bottom.cpp', 'r') as f2:
        bottom_boilerplate = f2.read()

    emit(bottom_boilerplate)

    with open(filename, 'w') as f:
        f.write(emp_output_string)

    with open(filename + '.emp_wit', 'w') as f:
        f.write(witness_output_string)
