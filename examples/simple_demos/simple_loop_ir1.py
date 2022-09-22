from miniwizpl import SecretInt, SecretList, assert0, print_ir1, public_foreach

ls = SecretList([1,2,3,4,5])

def add(a, b):
    return a + b

sum_result = public_foreach(ls, add, 0)
output = assert0(sum_result - 15)

print(sum_result)
print_ir1("miniwizpl_test")
