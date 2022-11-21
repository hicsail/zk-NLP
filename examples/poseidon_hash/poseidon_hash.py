from miniwizpl import *
from parameters import *
from hash import Poseidon


security_level = 128
input_rate = 8
t = 9
alpha = 17
prime = 2**61-1
set_field(prime)
poseidon_new = Poseidon(prime, security_level, alpha, input_rate, t)

#poseidon_simple, t = case_simple()

input_vec = SecretList([x for x in range(0, t)])

# [SecretInt(x) for x in range(0, t)]
print("Input: ", input_vec)
#
poseidon_digest = poseidon_new.run_hash(input_vec)
assert0(poseidon_digest - val_of(poseidon_digest))
#print('digest:', poseidon_digest)
print_ir0("miniwizpl_test_ir0")
