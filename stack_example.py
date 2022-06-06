from miniwizpl import SecretInt, SecretStack, print_emp

xs = SecretStack([1,2,3])
xs.push(5)
y = xs.pop()

print_emp(y, 'miniwizpl_test.cpp')
