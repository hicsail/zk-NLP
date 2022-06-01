from miniwizpl import SecretInt, SecretIndexList, print_emp

xs = SecretIndexList([1,2,3])
i = SecretInt(1)
print(xs)
print(xs[1])
print(xs[i])
xs[i] = SecretInt(5)
print(xs[i])

print_emp(xs[i], 'miniwizpl_test.cpp')
