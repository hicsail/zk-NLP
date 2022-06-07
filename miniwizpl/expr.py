import sys
import numpy as np
from dataclasses import dataclass
import os
from .globals import *

class AST:
    def __matmul__(self, other):
        return Prim('matmul', [self, other])

    def __rmatmul__(self, other):
        return Prim('matmul', [other, self])

    def __add__(self, other):
        return Prim('add', [self, other])

    def __radd__(self, other):
        return Prim('add', [other, self])

    def __sub__(self, other):
        return Prim('sub', [self, other])

    def __rsub__(self, other):
        return Prim('sub', [other, self])

    def __mul__(self, other):
        return Prim('mul', [self, other])

    def __rmul__(self, other):
        return Prim('mul', [other, self])

    def __floordiv__(self, other):
        return Prim('div', [self, other])

    def __rfloordiv__(self, other):
        return Prim('div', [other, self])

    def __mod__(self, other):
        return Prim('mod', [self, other])

    def __rmod__(self, other):
        return Prim('mod', [other, self])

    def __le__(self, other):
        return Prim('le', [self, other])

    def __lt__(self, other):
        return Prim('lt', [self, other])

    def __ge__(self, other):
        return Prim('ge', [self, other])

    def __gt__(self, other):
        return Prim('gt', [self, other])

    def __round__(self):
        return Prim('round', [self])

    def __eq__(self, other):
        return Prim('equals', [self, other])
    def __req__(self, other):
        return Prim('equals', [other, self])

    def __and__(self, other):
        return Prim('and', [self, other])
    def __rand__(self, other):
        return Prim('and', [self, other])

@dataclass
class SymVar(AST):
    name: str
    type: type

    def __eq__(self, other):
        return Prim('equals', [self, other])
    def __req__(self, other):
        return Prim('equals', [other, self])

@dataclass
class Prim(AST):
    op: str
    args: any

    def val(self):
        if self.op == 'relu':
            x = self.args[0].val()
            return x * (x > 0)
        elif self.op == 'log_softmax':
            x = self.args[0].val()
            return x
        elif self.op == 'matmul':
            e1, e2 = self.args
            return e1.val() @ e2.val()
        elif self.op == 'matplus':
            e1, e2 = self.args
            return e1.val() + e2.val()
        elif self.op == 'compare_secret_tensors':
            e1, e2 = self.args
            return e1.val() == e2.val()
        else:
            raise Exception(self)

    def __eq__(self, other):
        return Prim('equals', [self, other])
    def __req__(self, other):
        return Prim('equals', [other, self])

def exp_mod(a, b, c):
    return Prim('exp_mod', [a, b, c])

def relu(x):
    return Prim('relu', [x])

def compare_secret_tensors(a, b):
    return Prim('compare_secret_tensors', [a, b])

class SecretInt(AST):
    def __init__(self, intval):
        global all_defs
        all_defs.append(self)
        self.intval = intval
        self.name = gensym('intval')

    def __str__(self):
        return f'SecretInt({self.intval})'
    __repr__ = __str__

    def val(self):
        return self.intval

class SecretArray(AST):
    def __init__(self, arr):
        global all_defs
        all_defs.append(self)
        self.arr = arr
        self.name = gensym('mat')
        
    def __str__(self):
        return f'SecretArray({self.shape})'
    __repr__ = __str__

    def val(self):
        return self.arr

class SecretList(AST):
    def __init__(self, arr):
        global all_defs
        all_defs.append(self)
        self.arr = arr
        self.name = gensym('list')

    def __str__(self):
        return f'SecretList({len(self.arr)})'
    __repr__ = __str__

    def val(self):
        return self.arr

class SecretIndexList(AST):
    def __init__(self, arr):
        global all_defs
        all_defs.append(self)
        self.arr = arr
        self.name = gensym('list')

    def __getitem__(self, key):
        return Prim('listref', [self, key])

    def __setitem__(self, key, val):
        global all_statements
        all_statements.append(Prim('listset', [self, key, val]))

    def __str__(self):
        return f'SecretIndexList({len(self.arr)})'
    __repr__ = __str__

    def val(self):
        return self.arr

class SecretStack(AST):
    def __init__(self, arr):
        global all_defs
        all_defs.append(self)
        self.arr = arr
        self.name = gensym('stack')
        self.max_size = len(arr)

    def push(self, item):
        global all_statements
        #self.arr.append(item)
        self.max_size += 1
        
        all_statements.append(Prim('stack_push', [self, item]))

    def pop(self):
        xn = gensym('stack_val')
        x = SymVar(xn, int)
        all_statements.append(Prim('assign', [x, Prim('stack_pop', [self])]))
        return x

    def __str__(self):
        return f'SecretStack({len(self.arr)})'
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
