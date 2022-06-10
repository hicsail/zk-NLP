import sys
import numpy as np
from dataclasses import dataclass
import os
from .globals import *

def val_of(x):
    if isinstance(x, AST):
        if x.val == None:
            return 0      ######## TODO: FIX THIS HACK
        else:
            return x.val
    else:
        return x

class AST:
    def __matmul__(self, other):
        print(self)
        print(other)
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

    def __and__(self, other):
        return Prim('and', [self, other], val_of(self) & val_of(other))
    def __rand__(self, other):
        return Prim('and', [self, other], val_of(other) & val_of(self))

@dataclass
class SymVar(AST):
    name: str
    type: type
    val: any

    def __eq__(self, other):
        return Prim('equals', [self, other], val_of(self) == val_of(other))
    def __req__(self, other):
        return Prim('equals', [other, self], val_of(other) == val_of(self))

@dataclass
class Prim(AST):
    op: str
    args: any
    val: any

    def __eq__(self, other):
        return Prim('equals', [self, other], val_of(self) == val_of(other))
    def __req__(self, other):
        return Prim('equals', [other, self], val_of(other) == val_of(self))

def exp_mod(a, b, c):
    return Prim('exp_mod', [a, b, c], pow(val_of(a), val_of(b), val_of(c)))

def relu(x):
    output_val = np.maximum(val_of(x), 0)
    return Prim('relu', [x], output_val)

def compare_secret_tensors(a, b):
    return Prim('compare_secret_tensors', [a, b], None) # TODO: fill in value

class SecretInt(AST):
    def __init__(self, intval):
        global all_defs
        all_defs.append(self)
        self.val = intval
        self.name = gensym('intval')

    def __str__(self):
        return f'SecretInt({self.val})'
    __repr__ = __str__

class SecretArray(AST):
    def __init__(self, arr):
        global all_defs
        all_defs.append(self)
        self.arr = arr
        self.val = arr
        self.name = gensym('mat')
        
    def __str__(self):
        return f'SecretArray({self.val.shape})'
    __repr__ = __str__

class SecretList(AST):
    def __init__(self, arr):
        global all_defs
        all_defs.append(self)
        self.arr = arr
        self.val = arr
        self.name = gensym('list')

    def __str__(self):
        return f'SecretList({len(self.arr)})'
    __repr__ = __str__

class SecretIndexList(AST):
    def __init__(self, arr):
        global all_defs
        all_defs.append(self)
        self.arr = arr
        self.val = arr
        self.name = gensym('list')

    def __getitem__(self, key):
        global all_statements
        xn = gensym('list_val')
        x = SymVar(xn, int, None)
        all_statements.append(Prim('assign', [x, Prim('listref', [self, key],
                                                      val_of(self)[val_of(key)])],
                                             None))
        return x

    def __setitem__(self, key, val):
        global all_statements
        all_statements.append(Prim('listset', [self, key, val], None))

    def __str__(self):
        return f'SecretIndexList({len(self.arr)})'
    __repr__ = __str__

class SecretStack(AST):
    def __init__(self, arr):
        global all_defs
        all_defs.append(self)
        self.arr = arr
        self.val = arr
        self.name = gensym('stack')
        self.max_size = len(arr)

    # TODO: need to fix values for these
    def push(self, item):
        global all_statements
        self.max_size += 1
        
        all_statements.append(Prim('stack_push', [self, item], None))

    def cond_push(self, condition, item):
        global all_statements
        self.max_size += 1
        all_statements.append(Prim('stack_cond_push', [self, condition, item], None))

    def pop(self):
        global all_statements
        xn = gensym('stack_val')
        x = SymVar(xn, int, None)
        all_statements.append(Prim('assign', [x, Prim('stack_pop', [self], None)], None))
        return x

    def __str__(self):
        return f'SecretStack({len(self.arr)})'
    __repr__ = __str__

class SecretTensor(AST):
    def __init__(self, arr):
        global all_defs
        all_defs.append(self)
        self.arr = arr
        self.val = arr
        self.name = gensym('tensor')
        
    def __str__(self):
        return f'SecretTensor({self.val.shape})'
    __repr__ = __str__

    def tensor(self):
        return self.arr

    def __getattr__(self, name):
        print('getattr', name)
        return getattr(self.arr, name)
