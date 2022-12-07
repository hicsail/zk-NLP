import sys
from miniwizpl import *

assert len(sys.argv) == 5, "Invalid arguments"
_, target_dir, prime, prime_name, size = sys.argv

set_field(int(prime))

n = 10**int(size)

ls = SecretList(list(range(1, n)))

def add(a, b):
    return b + a

sum_result = reduce(add, ls, 0)
output = assert0(sum_result - val_of(sum_result))

#print(val_of(sum_result))
#print_ir0("miniwizpl_test_ir0")
print_ir0(target_dir + "/" + f"list_sum_{prime_name}_{size}")
