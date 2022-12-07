import sys
from miniwizpl import *

assert len(sys.argv) == 5, "Invalid arguments"
_, target_dir, prime, prime_name, size = sys.argv

set_field(int(prime))

n = 10**int(size)

xs = [SecretInt(x) for x in range(1, n)]
ys = [SecretInt(y) for y in range(1, n)]

def dot_product(xs, ys):
    return sum([x*y for x, y in zip(xs, ys)])

result = dot_product(xs, ys)
output = assert0(result - val_of(result))

print_ir0(target_dir + "/" + f"dot_product_{prime_name}_{size}")
