import sys
import numpy as np
from dataclasses import dataclass
import os
from .globals import *
from .expr import *

def index(arr, val, start, length):
    #return arr[start:end].index(val)
    global all_statements
    xn = gensym('list_idx')
    x = SymVar(xn, int, None)
    all_statements.append(Prim('assign',
                               [x, Prim('listindex', [arr, val, start, length], None)],
                               None))
    return x

def comment(msg):
    """
    Prints a comment in the compiler's output.
    """
    global all_statements
    all_statements.append(Prim('comment', [msg], None))

def log_int(msg, val):
    """
    Logs an integer (i.e. reveals it publicly) in the compiler's output.
    """
    global all_statements
    all_statements.append(Prim('log_val', [int, msg, val], None))

def log_bool(msg, val):
    """
    Logs a boolean (i.e. reveals it publicly) in the compiler's output.
    """
    global all_statements
    all_statements.append(Prim('log_val', [bool, msg, val], None))

_original_pow = pow
def pow(a, b, c):
    """
    Performs modular exponentiation.
    """
    if isinstance(a, AST) or isinstance(b, AST) or isinstance(c, AST):
        return Prim('exp_mod', [a, b, c], _original_pow(val_of(a), val_of(b), val_of(c)))
    else:
        return _original_pow(a, b, c)

def public_foreach(xs, f, init):
    assert isinstance(xs, SecretList)
    t_a = type(init)

    # TODO: how can we handle the values here?
    x = SymVar(gensym('x'), SecretInt, None)
    a = SymVar(gensym('a'), t_a, None)
    r = f(x, a)

    # compute the actual result
    a_val = val_of(init)
    for x_val in val_of(xs):
        a_val = val_of(f(x_val, a_val))

    loop = Prim('fold', [x, r, a, xs, init], a_val)
    return loop

def mux(a, b, c):
    return Prim('mux', [a, b, c], val_of(b) if val_of(a) else val_of(c))

def set_bitwidth(b):
    global bitwidth
    bitwidth = b

def assert0(v):
    global assertions
    assertions.append(Prim('assert0', [v], val_of(v) == 0))
