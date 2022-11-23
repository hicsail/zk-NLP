from dataclasses import dataclass
import galois
import os
from .globals import *
from .expr import *

class SecretInt(AST):
    """
    A secret integer. Its value will be part of the witness for the compiled ZK statement.
    """
    def __init__(self, intval):
        global all_defs
        all_defs.append(self)
        self.val = intval
        self.name = gensym('intval')

    def __str__(self):
        return f'SecretInt({self.val})'
    __repr__ = __str__

class SecretGF(AST):
    """
    A secret finite field element. Its value will be part of the witness for the compiled ZK statement.
    """
    def __init__(self, intval):
        global all_defs
        all_defs.append(self)
        p = params['arithmetic_field']
        self.val = galois.GF(p)(intval)
        self.name = gensym('gfval')

    def __str__(self):
        return f'SecretGF({self.val})'
    __repr__ = __str__

class SecretArray(AST):
    """
    An array of secret values. The length of the array is public.
    """
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
    """
    A list of secret values. The length of the list is public.
    """
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
    """
    A list of secret values with secret indexing. The maximum length of the list is public.

    Allows indexing into the list with a SecretInt, e.g.:

    - Get an item: `arr[SecretInt(5)]`
    - Set an item: `arr[SecretInt(5)] = SecretInt(6)`
    """
    def __init__(self, arr):
        global all_defs
        all_defs.append(self)
        self.arr = arr
        self.val = arr
        self.name = gensym('list')

    def __getitem__(self, key):
        xn = gensym('list_val')
        x = SymVar(xn, int, None)
        params['all_statements'].append(Prim('assign', [x, Prim('listref', [self, key],
                                                      val_of(self)[val_of(key)])],
                                             None))
        return x

    def __setitem__(self, key, val):
        params['all_statements'].append(Prim('listset', [self, key, val], None))

    def __str__(self):
        return f'SecretIndexList({len(self.arr)})'
    __repr__ = __str__

class SecretStack(AST):
    """
    An oblivious stack with conditional push and pop. The maximum size of the stack
    is public.
    """
    def __init__(self, arr):
        global all_defs
        all_defs.append(self)
        self.arr = arr
        self.val = arr
        self.name = gensym('stack')
        self.max_size = len(arr)

    # TODO: need to fix values for these
    def push(self, item):
        """Unconditional push."""
        self.max_size += 1

        params['all_statements'].append(Prim('stack_push', [self, item], None))

    def cond_push(self, condition, item):
        """Conditional push."""
        self.max_size += 1
        params['all_statements'].append(Prim('stack_cond_push', [self, condition, item], None))

    def pop(self):
        """Unconditional pop."""
        xn = gensym('stack_val')
        x = SymVar(xn, int, None)
        params['all_statements'].append(Prim('assign', [x, Prim('stack_pop', [self], None)], None))
        return x

    def __str__(self):
        return f'SecretStack({len(self.arr)})'
    __repr__ = __str__

class SecretTensor(AST):
    """
    An n-dimensional tensor of secret values, integrated with PyTorch's tensor library.
    """
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

class PublicTensor(AST):
    """
    An n-dimensional tensor of public values, integrated with PyTorch's tensor library.
    """
    def __init__(self, arr):
        global all_defs
        all_defs.append(self)
        self.arr = arr
        self.val = arr
        self.name = gensym('tensor')

    def __str__(self):
        return f'PublicTensor({self.val.shape})'
    __repr__ = __str__

    def tensor(self):
        return self.arr

    def __getattr__(self, name):
        print('getattr', name)
        return getattr(self.arr, name)
