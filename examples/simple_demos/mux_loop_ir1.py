from miniwizpl import *

ls = SecretList(list(range(1, 5)))

def f(x, accum):
    return mux(x == 3, accum + x, accum)

sum_result = public_foreach(ls, f, 0)
output = assert0(sum_result - 15)

print(sum_result)
#print_ir0("miniwizpl_test_ir0")
print_ir1("miniwizpl_test_ir1")
