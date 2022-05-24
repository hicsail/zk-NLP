from miniwizpl import SecretInt, SecretList, print_emp

xs = SecretList([1,2,3])
i = SecretInt(1)
print(xs)
print(xs[1])
print(xs[i])
