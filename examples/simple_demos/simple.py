from miniwizpl import SecretInt, Prim, assert0EMP, print_emp

x = SecretInt(3)
y = SecretInt(2)
output = assert0EMP(x + y - 5)

print_emp(output, "miniwizpl_test.cpp")
