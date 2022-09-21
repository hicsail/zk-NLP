from .mini_wizpl import *
from .expr import *
from .data_types import *
from .compile_emp import print_emp
from .compile_ir1 import print_ir1

__pdoc__ = {}
for m in ['torch', 'compile_emp', 'compile_ir1', 'expr', 'globals', 'utils']:
    __pdoc__[m] = False


