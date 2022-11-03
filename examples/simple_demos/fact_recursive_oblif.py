from miniwizpl import *
from oblif.decorator import oblif

@miniwizpl_recursive(unrolling_bound = 10)
@oblif
def fact(n):
    if n == 0:
        return 1
    else:
        return n * fact(n-1)

n = SecretInt(5)
r = fact(n)
assert0(r - 120)
print_ir0("miniwizpl_test_ir0")
