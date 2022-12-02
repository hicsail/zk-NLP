from miniwizpl import *

xs = SecretStack([1,2,3])

xs.push(5)
print('xs', xs.current_val)
y = xs.pop()
print('y', val_of(y))
print('xs', xs.current_val)
xs.push(6)
print('xs', xs.current_val)
z = xs.pop()
print('z', val_of(z))
print('xs', xs.current_val)
xs.cond_push(z == y, 7)
print('xs', xs.current_val)
a = xs.cond_pop(z == y)
print('a', val_of(a))
print('xs', xs.current_val)

assert0EMP(a)
assert0EMP(z-6)

b = xs.cond_pop(z == z)
print('b', val_of(b))
print('xs', xs.current_val)
assert0EMP(b-5)

print_emp('miniwizpl_test.cpp')
