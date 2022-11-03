from miniwizpl import *

@miniwizpl_recursive(unrolling_bound = 10)
def fact(n):
    return mux(n == 0,
               1,
               n * fact(n-1))

n = SecretInt(5)
r = fact(n)
assert0(r - 120)
print_ir0("miniwizpl_test_ir0")
