from miniwizpl import *
from parameters import *

poseidon_simple, t = case_simple()

input_vec = SecretList([x for x in range(0, t)])

# [SecretInt(x) for x in range(0, t)]
print("Input: ", input_vec)
#
poseidon_digest = poseidon_simple.run_hash(input_vec)
assert0(len(input_vec.val) - 9)
print(poseidon_digest)
print_ir1("miniwizpl_test_ir1")