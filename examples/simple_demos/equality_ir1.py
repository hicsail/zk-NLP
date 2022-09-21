from miniwizpl import SecretInt, Prim, print_ir1, assert0, set_field, mux
set_field(2**61 - 1)

x = SecretInt(3)
y = SecretInt(2)
output = mux(x == y, 10, 20)
assert0(output)

print_ir1("miniwizpl_test")
