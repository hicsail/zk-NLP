from miniwizpl import SecretInt, Prim, print_ir1, assert0, set_field, mux
set_field(2**61 - 1)

x = SecretInt(3)
y = SecretInt(2)
a = SecretInt(20)
b = SecretInt(30)
z = mux(x == y, a, b+a)
output = z
assert0(output - 30)

print_ir1("miniwizpl_test")
