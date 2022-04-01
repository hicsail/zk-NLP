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

    def __mul__(self, other):
        return Prim('mul', [self, other])

    def __rmul__(self, other):
        return Prim('mul', [other, self])

    def __mod__(self, other):
        return Prim('mod', [other, self])

    def __rmod__(self, other):
        return Prim('mod', [self, other])

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
