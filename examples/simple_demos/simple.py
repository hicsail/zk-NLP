from miniwizpl import SecretInt, Prim, print_emp

x = SecretInt(3)
y = SecretInt(2)
output = x + y
print(output)

print_emp(output, "miniwizpl_test.cpp")
