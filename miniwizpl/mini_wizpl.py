import sys
import numpy as np
from dataclasses import dataclass
import os
from .globals import *
from .expr import *

def comment(msg):
    global all_statements
    all_statements.append(Prim('comment', [msg]))

original_pow = pow
def pow(a, b, c):
    if isinstance(a, AST) or isinstance(b, AST) or isinstance(c, AST):
        return Prim('exp_mod', [a, b, c])
    else:
        return original_pow(a, b, c)

def public_foreach(xs, f, init):
    assert isinstance(xs, SecretList)
    t_a = type(init)

    x = SymVar(gensym('x'), SecretInt)
    a = SymVar(gensym('a'), t_a)
    r = f(x, a)
    loop = Prim('fold', [x, r, a, xs, init])
    return loop

def mux(a, b, c):
    return Prim('mux', [a, b, c])

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

def set_bitwidth(b):
    global bitwidth
    bitwidth = b

def assert0(v):
    global assertions
    assertions.append(Prim('assert0', [v]))
