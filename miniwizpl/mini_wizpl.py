import sys
import numpy as np
from dataclasses import dataclass
from functools import wraps
import os
from .globals import *
from .expr import *
from .data_types import *

def miniwizpl_recursive(*args, **kwargs):
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        raise RuntimeError('For recursive functions, you must provide an unrolling bound')

    bound = kwargs['unrolling_bound']
    def decorator(func):
        top = True
        name = gensym('func')
        @wraps(func)
        def wrapped(*args):
            result = Prim('rec', [name, bound, list(args), func], None)
            return result
        return wrapped

    return decorator

def index(arr, val, start, length):
    #return arr[start:end].index(val)
    xn = gensym('list_idx')
    x = SymVar(xn, int, None)
    params['all_statements'].append(Prim('assign',
                               [x, Prim('listindex', [arr, val, start, length], None)],
                               None))
    return x


def assert0EMP(a):
    params['all_statements'].append(Prim('assert0EMP', [a], val_of(a) == 0))

def assertTrueEMP(a):
    params['all_statements'].append(Prim('assertTrueEMP', [a], val_of(a) == True))

def assertFalseEMP(a):
    params['all_statements'].append(Prim('assertFalseEMP', [a], val_of(a) == False))

def comment(msg):
    """
    Prints a comment in the compiler's output.
    """
    params['all_statements'].append(Prim('comment', [msg], None))

def log_int(msg, val):
    """
    Logs an integer (i.e. reveals it publicly) in the compiler's output.
    """
    params['all_statements'].append(Prim('log_val', [int, msg, val], None))

def log_bool(msg, val):
    """
    Logs a boolean (i.e. reveals it publicly) in the compiler's output.
    """
    params['all_statements'].append(Prim('log_val', [bool, msg, val], None))

_original_pow = pow
def pow(a, b, c):
    """
    Performs modular exponentiation.
    """
    if isinstance(a, AST) or isinstance(b, AST) or isinstance(c, AST):
        return Prim('exp_mod', [a, b, c], _original_pow(int(val_of(a)), val_of(b), val_of(c)))
    else:
        return _original_pow(a, b, c)

def reduce_unroll(f, xs, init):
    a = init
    if isinstance(xs, SecretList):
        for x in val_of(xs):
            a = f(SecretInt(x), a)
    else:
        for x in xs:
            a = f(x, a)
    return a

def reduce(f, xs, init):
    assert isinstance(xs, SecretList)

    a = val_of(init)
    for x in val_of(xs):
        a = val_of(f(val_of(x), a))

    # f is a function x -> accumulator -> new accumulator
    return Prim('fold', [xs, f, init], a)

def mux(a, b, c):
    return Prim('mux', [a, b, c], val_of(b) if val_of(a) else val_of(c))

def dot(x, y):
    result = [None for _ in x]
    # iterate through rows of X
    for i in range(len(x)):
        # iterate through columns of Y
        for j in range(len(y[0])):
            # iterate through rows of Y
            for k in range(len(y)):
                if result[i] is None:
                    result[i] = x[i] * y[k][j]
                else:
                    result[i] += x[i] * y[k][j]
    return result

def set_bitwidth(b):
    """
    Set the bitwidth for boolean-representation output.
    """
    params['bitwidth'] = b

def set_field(b):
    """
    Set the field size for arithmetic-representation output.
    """
    global params
    params['arithmetic_field'] = b

def assert0(v):
    params['all_statements'].append(Prim('assert0', [v], val_of(v) == 0))

def reveal_array(v):
    params['all_statements'].append(Prim('reveal_array', [v], val_of(v)))
