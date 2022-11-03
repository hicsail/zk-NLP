from miniwizpl import SecretInt, Prim, assert0EMP, print_emp

x = SecretInt(3)
y = SecretInt(2)
output = x + y - 5

assert0EMP(output)
print_emp("miniwizpl_test.cpp")
