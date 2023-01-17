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
        assert intval <= p
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

    def as_field_elements(self, k):
        """
        Returns the elements of this list as field elements, in chunks of size k
        """

        # TODO: this is wrong; it adds the value to the witness twice and doesn't
        # prove a correspondence between the two witness values
        p = params['arithmetic_field']
        for x in self.arr:
            assert x <= p

        pad_len = k*(len(self.arr) // k)+k - len(self.arr)
        gf_arr_pad = np.pad(self.arr, (0, pad_len)).reshape((-1, k))

        blocks = [[SecretGF(int(x)) for x in a] for a in gf_arr_pad]

        return blocks

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
        params['ram_num_allocs'] += 1
        params['ram_total_alloc_size'] += len(arr)

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
        self.val = arr.copy()
        self.original_val = arr.copy()
        self.name = gensym('stack')
        self.max_size = len(arr)

    def push(self, item):
        """Unconditional push."""
        self.max_size += 1
        self.val.append(val_of(item))
        self.max_size = max(self.max_size, len(self.val))

        params['all_statements'].append(Prim('stack_push', [self, item], None))

    def cond_push(self, condition, item):
        """Conditional push."""

        if val_of(condition):
            self.val.append(val_of(item))
            self.max_size = max(self.max_size, len(self.val))

        params['all_statements'].append(Prim('stack_cond_push', [self, condition, item], None))

    def pop(self):
        """Unconditional pop."""
        xn = gensym('stack_val')
        v = self.val.pop()
        x = SymVar(xn, int, v)

        params['all_statements'].append(Prim('assign', [x, Prim('stack_pop', [self], v)], None))
        return x

    def cond_pop(self, condition):
        """Conditional pop."""
        xn = gensym('stack_val')

        if val_of(condition):
            v = self.val.pop()
        else:
            v = None

        x = SymVar(xn, int, v)
        params['all_statements'].append(Prim('assign', [x, Prim('stack_cond_pop',
                                                                [self, condition], v)],
                                             None))
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
