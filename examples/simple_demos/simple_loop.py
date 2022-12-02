from miniwizpl import SecretInt, SecretList, assert0EMP, print_emp, public_foreach

ls = SecretList([1,2,3,4,5])

def add(a, b):
    return a + b

sum_result = public_foreach(ls, add, 0)
assert0EMP(sum_result - 15)

print_emp(True, "miniwizpl_test.cpp")
