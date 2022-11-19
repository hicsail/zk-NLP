from miniwizpl import *

stk = SecretStack([])
y = SecretInt(3)
xs = SecretList([1,2,3,4,5])

def push(x, a):
    stk.cond_push(x == y, x)
    return a

def pop(x, a):
    return a + stk.cond_pop(x == y)

result = public_foreach(xs, push, 0)
#result = public_foreach(xs, pop, 0)
assert0EMP(result)

print_emp(True, 'miniwizpl_test.cpp')
