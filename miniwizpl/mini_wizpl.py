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
    global all_statements
    xn = gensym('list_idx')
    x = SymVar(xn, int, None)
    all_statements.append(Prim('assign',
                               [x, Prim('listindex', [arr, val, start, length], None)],
                               None))
    return x


def assert0EMP(a):
    global all_statements
    all_statements.append(Prim('assert0EMP', [a], val_of(a) == 0))

def assertTrueEMP(a):
    global all_statements
    all_statements.append(Prim('assertTrueEMP', [a], val_of(a) == True))

def assertFalseEMP(a):
    global all_statements
    all_statements.append(Prim('assertFalseEMP', [a], val_of(a) == False))

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

def public_foreach_unroll(xs, f, init):
    a = init
    if isinstance(xs, SecretList):
        for x in val_of(xs):
            a = f(SecretInt(x), a)
    else:
        for x in xs:
            a = f(x, a)
    return a

def public_foreach(xs, f, init):
    assert isinstance(xs, SecretList)

    # f is a function x -> accumulator -> new accumulator
    return Prim('fold', [xs, f, init], None)

def mux(a, b, c):
    return Prim('mux', [a, b, c], val_of(b) if val_of(a) else val_of(c))

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
    global assertions
    assertions.append(Prim('assert0', [v], val_of(v) == 0))
