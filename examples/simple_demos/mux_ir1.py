from miniwizpl import *
set_field(2**61 - 1)

x = SecretInt(3)
y = SecretInt(2)
a = SecretInt(20)
b = SecretInt(30)
z = mux(x == y, a, b+a)
output = z
assert0(output - 50)

w = mux(x != y, a, b)
assert0(w - val_of(a))

print_ir0("miniwizpl_test")
