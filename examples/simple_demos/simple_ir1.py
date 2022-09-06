from miniwizpl import SecretInt, Prim, print_ir1, assert0, set_field
set_field(2**61 - 1)

x = SecretInt(3)
y = SecretInt(2)
output = x + y
assert0(output - 5)

print_ir1("miniwizpl_test")
