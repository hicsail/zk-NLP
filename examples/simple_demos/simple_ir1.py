from miniwizpl import SecretInt, Prim, print_ir1, assert0

x = SecretInt(3)
y = SecretInt(2)
output = x + y
assert0(output)

print_ir1("miniwizpl_test")
