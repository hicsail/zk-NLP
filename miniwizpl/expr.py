import sys
import numpy as np
from dataclasses import dataclass
import os
from .globals import *

def val_of(x):
    if isinstance(x, AST):
        if x.val is None:
            return 0      ######## TODO: FIX THIS HACK
        else:
            return x.val
    else:
        return x

class AST:
    def __matmul__(self, other):
        return Prim('matmul', [self, other], val_of(self) @ val_of(other))

    def __rmatmul__(self, other):
        return Prim('matmul', [other, self], val_of(other) @ val_of(self))

    def __neg__(self):
        return Prim('neg', [self], -val_of(self))

    def __add__(self, other):
        return Prim('add', [self, other], val_of(self) + val_of(other))

    def __radd__(self, other):
        return Prim('add', [other, self], val_of(other) + val_of(self))

    def __sub__(self, other):
        return Prim('sub', [self, other], val_of(self) - val_of(other))

    def __rsub__(self, other):
        return Prim('sub', [other, self], val_of(other) - val_of(self))

    def __mul__(self, other):
        return Prim('mul', [self, other], val_of(self) * val_of(other))

    def __rmul__(self, other):
        return Prim('mul', [other, self], val_of(other) * val_of(self))

    def __floordiv__(self, other):
        return Prim('div', [self, other], val_of(self).__floordiv__(val_of(other)))

    def __rfloordiv__(self, other):
        return Prim('div', [other, self], val_of(self).__rfloordiv__(val_of(other)))

    def __mod__(self, other):
        return Prim('mod', [self, other], val_of(self) % val_of(other))

    def __rmod__(self, other):
        return Prim('mod', [other, self], val_of(other) % val_of(self))

    def __le__(self, other):
        return Prim('le', [self, other], val_of(self) <= val_of(other))

    def __lt__(self, other):
        return Prim('lt', [self, other], val_of(self) < val_of(other))

    def __ge__(self, other):
        return Prim('ge', [self, other], val_of(self) >= val_of(other))

    def __gt__(self, other):
        return Prim('gt', [self, other], val_of(self) > val_of(other))

    def __round__(self):
        return Prim('round', [self], val_of(self).__round__())

    def __eq__(self, other):
        return Prim('equals', [self, other], val_of(self) == val_of(other))
    def __req__(self, other):
        return Prim('equals', [other, self], val_of(other) == val_of(self))

    def __ne__(self, other):
        return Prim('not_equals', [self, other], val_of(self) != val_of(other))
    def __rne__(self, other):
        return Prim('not_equals', [other, self], val_of(other) != val_of(self))

    def __and__(self, other):
        return Prim('and', [self, other], val_of(self) & val_of(other))
    def __rand__(self, other):
        return Prim('and', [self, other], val_of(other) & val_of(self))
    def __invert__(self):
        return Prim('not', [self], not val_of(self))

    def __int__(self):
        raise RuntimeError('unsupported: convert AST to int')

    def __bool__(self):
        raise RuntimeError('unsupported: convert AST to bool')

    def if_else(self, ifval, elseval):
        return Prim('mux', [self, ifval, elseval], None)

    def __or__(self, other):
        return Prim('or', [self, other], val_of(self) | val_of(other))
    def __ror__(self, other):
        return Prim('or', [self, other], val_of(other) | val_of(self))

@dataclass
class SymVar(AST):
    name: str
    type: type
    val: any

    def __eq__(self, other):
        return Prim('equals', [self, other], val_of(self) == val_of(other))
    def __req__(self, other):
        return Prim('equals', [other, self], val_of(other) == val_of(self))
    def __str__(self):
        return f'SymVar({self.name})'
    __repr__ = __str__

@dataclass
class Prim(AST):
    op: str
    args: any
    val: any

    def __eq__(self, other):
        return Prim('equals', [self, other], val_of(self) == val_of(other))
    def __req__(self, other):
        return Prim('equals', [other, self], val_of(other) == val_of(self))
    def __invert__(self):
        return Prim('not', [self], not val_of(self))

def exp_mod(a, b, c):
    return Prim('exp_mod', [a, b, c], pow(val_of(a), val_of(b), val_of(c)))

def relu(x):
    output_val = np.maximum(val_of(x), 0)
    return Prim('relu', [x], output_val)

def compare_tensors(a, b):
    return Prim('compare_tensors', [a, b], None) # TODO: fill in value
