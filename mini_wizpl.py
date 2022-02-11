import sys
import numpy as np
from dataclasses import dataclass

all_defs = []

gensym_num = 0
def gensym(x):
    """
    Constructs a new variable name guaranteed to be unique.
    :param x: A "base" variable name (e.g. "x")
    :return: A unique variable name (e.g. "x_1")
    """

    global gensym_num
    gensym_num = gensym_num + 1
    return f'{x}_{gensym_num}'

class AST:
    def __matmul__(self, other):
        return Prim('matmul', [self, other])

    def __rmatmul__(self, other):
        return Prim('matmul', [other, self])

@dataclass
class Prim(AST):
    op: str
    args: any

    def val(self):
        if self.op == 'relu':
            x = self.args[0].val()
            return x * (x > 0)
        elif self.op == 'softmax':
            x = self.args[0].val()
            return x
        elif self.op == 'matmul':
            e1, e2 = self.args
            return e1.val() @ e2.val()
        elif self.op == 'matplus':
            e1, e2 = self.args
            return e1.val() + e2.val()
        else:
            raise Exception(self)


def relu(x):
    return Prim('relu', [x])

class SecretArray(AST):
    def __init__(self, arr):
        global all_defs
        all_defs.append(self)
        self.arr = arr
        self.name = gensym('mat')
        
    def __str__(self):
        return f'SecretArray({self.arr.shape})'
    __repr__ = __str__

    def val(self):
        return self.arr

class SecretTensor(AST):
    def __init__(self, arr):
        global all_defs
        all_defs.append(self)
        self.arr = arr
        self.name = gensym('tensor')
        
    def __str__(self):
        return f'SecretTensor({self.arr.shape})'
    __repr__ = __str__

    def val(self):
        return self.arr

    def tensor(self):
        return self.arr

    def __getattr__(self, name):
        print('getattr', name)
        return getattr(self.arr, name)

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

def print_exp(e):
    if isinstance(e, SecretArray):
        return e.name
    elif isinstance(e, SecretTensor):
        return e.name
    elif isinstance(e, Prim):
        if e.op == 'relu':
            x = print_exp(e.args[0])
            r = gensym('result_mat')
            r1, r2 = e.val().shape
            print(f'  static Integer {r}[{r1}][{r2}];')
            print(mk_relu(e.args[0], x, r))
            print()
            return r
        elif e.op == 'softmax':
            x = print_exp(e.args[0])
            r = gensym('result_mat_softmax')
            r1, r2 = e.val().shape
            print(f'  static Integer {r}[{r1}][{r2}];')
            print(mk_relu(e.args[0], x, r))
            print()
            return r
        elif e.op == 'matmul':
            e1, e2 = e.args
            x1 = print_exp(e1)
            x2 = print_exp(e2)
            r = gensym('result_mat')

            n1, n2 = e1.val().shape
            m1, m2 = e2.val().shape
            r1, r2 = e.val().shape
            print(f'  static Integer {r}[{r1}][{r2}];');
            print(mk_matmul(e1, e2, x1, x2, r))
            return r
        elif e.op == 'matplus':
            e1, e2 = e.args
            x1 = print_exp(e1)
            x2 = print_exp(e2)
            r = gensym('result_mat')

            n1, n2 = e1.val().shape
            e2s = e2.val().shape
            if len(e2s) == 1:
                m1 = 1
                m2 = e2s[0]
            elif len(e2s) == 2:
                m1 = e2s[0]
                m2 = e2s[1]

            r1, r2 = e.val().shape
            print(f'  static Integer {r}[{r1}][{r2}];');
            print(mk_matplus(e1, e2, x1, x2, r))
            #print(f'wizpl_matmul({x1}, {x2}, {r}, {n1}, {n2}, {m1}, {m2});')
            print()
            return r
        else:
            raise Exception(e)
    else:
        raise Exception(e)

def mk_relu(x1, x1_name, out):
    r1, c1 = x1.val().shape
    return f'  matrix_relu(*{x1_name}, {r1}, {c1}, *{out});\n'
#     return f"""
#   for(int i = 0; i < {r1}; ++i)
#       for(int j = 0; j < {c1}; ++j)
#       {{
#           {out}[i][j]={x1_name}[i][j].select({x1_name}[i][j] > Integer(32, 0, PUBLIC), Integer(32, 0, PUBLIC));
#       }}
# """
#     return f"""
#   for(int i = 0; i < {r1}; ++i)
#       for(int j = 0; j < {c1}; ++j)
#       {{
#           {out}[i][j]={x1_name}[i][j].select({x1_name}[i][j] > Integer(32, 0, PUBLIC), Integer(32, 0, PUBLIC));
#       }}
# """
    

def mk_matmul(x1, x2, x1_name, x2_name, out):
    r1, c1 = x1.val().shape
    r2, c2 = x2.val().shape

    return f'  matrix_mult(*{x1_name}, *{x2_name}, {r1}, {c1}, {r2}, {c2}, *{out});\n'

def mk_matplus(x1, x2, x1_name, x2_name, out):
    r1, c1 = x1.val().shape

    e2s = x2.val().shape
    if len(e2s) == 1:
        r2 = 1
        c2 = e2s[0]
    elif len(e2s) == 2:
        r2 = e2s[0]
        c2 = e2s[1]


    return f'  matrix_plus(*{x1_name}, *{x2_name}, {r1}, {c1}, {r2}, {c2}, *{out});\n'

#     return f"""
#   for(int i = 0; i < {r1}; ++i)
#       for(int j = 0; j < {c2}; ++j)
#       {{
#           {out}[i][j]=Integer(32, 0, PUBLIC);
#       }}

#   for(int i = 0; i < {r1}; ++i)
#       for(int j = 0; j < {c2}; ++j)
#           for(int k = 0; k < {c1}; ++k)
#           {{
#               {out}[i][j] = {out}[i][j] + ({x1_name}[i][k] * {x2_name}[k][j]);
#           }}
# """

def print_defs(defs):
    for d in defs:
        name = d.name
        x = d.val()

        e2s = x.shape
        if len(e2s) == 1:
            n1 = 1
            n2 = e2s[0]
        elif len(e2s) == 2:
            n1 = e2s[0]
            n2 = e2s[1]

        p = f"""
  int {name}_init[{n1}][{n2}] = {print_mat(x)};
  static Integer {name}[{n1}][{n2}];
  for (int i = 0; i < {n1}; ++i)
    for (int j = 0; j < {n2}; ++j)
      {name}[i][j] = Integer(32, {name}_init[i][j], ALICE);
"""
        print(p)


def print_mat(x):
    x = x.detach().numpy()

    if len(x.shape) == 1:
        return '{{' + ', '.join([str(int(i)) for i in x]) + '}}'

    elif len(x.shape) == 2:
        return '{' + ', '.join(['{' + ', '.join([str(int(x)) for x in row]) + '}'
                            for row in x]) + '}'

def print_emp(outp, filename):
    global all_defs

    original_stdout = sys.stdout

    with open(filename, 'w') as f:
        sys.stdout = f

        with open('mini_wizpl_top.cpp', 'r') as f1:
            top_boilerplate = f1.read()
            
        print(top_boilerplate)

        print_defs(all_defs)
        print()
        print_exp(outp)

        with open('mini_wizpl_bottom.cpp', 'r') as f2:
            bottom_boilerplate = f2.read()
            
        print(bottom_boilerplate)

        sys.stdout = original_stdout


