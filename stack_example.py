from miniwizpl import SecretInt, SecretStack, print_emp

# NOTE: we currently don't handle ordering correctly here, due to the way
# we capture side effects and how they can interleave with assignments

xs = SecretStack([1,2,3])

xs.push(5)
y = xs.pop()
xs.push(6)
z = xs.pop()

print_emp(y, 'miniwizpl_test.cpp')
