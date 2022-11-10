from miniwizpl import *

xs = SecretStack([1,2,3])

xs.push(5)
y = xs.pop()
xs.push(6)
z = xs.pop()
xs.cond_push(z == y, 7)
a = xs.cond_pop(z == y)

assert0EMP(a)
assert0EMP(z-6)

b = xs.cond_pop(z == z)
assert0EMP(b-5)

print_emp(y, 'miniwizpl_test.cpp')
