import numpy as np
from miniwizpl import *

sys.path.append("../examples/poseidon_hash")
from parameters import *
from hash import Poseidon, calculate_alpha, calculate_length

assert len(sys.argv) == 5, "Invalid arguments"
_, target_dir, prime, prime_name, size = sys.argv
prime = int(prime)
set_field(prime)
n = 2**int(size)

security_level = 128
alpha = calculate_alpha(prime)
input_rate = calculate_length(prime)
t = input_rate
poseidon_new = Poseidon(prime, security_level, alpha, input_rate, t)

# generate random input of length 2^size
# split it into blocks of length t
input_vec = np.pad(np.random.randint(0, 100, n), (0, t - n%t)).reshape((-1, t))
blocks = [[SecretGF(int(x)) for x in a] for a in input_vec]

# print(f'parameters: alpha = {alpha}, t = {t}, blocks = {len(blocks)}')

for block in blocks:
    poseidon_digest = poseidon_new.run_hash(block)
    digest_val = val_of(poseidon_digest)
    #print('digest:', digest_val)
    assert0(poseidon_digest - digest_val)

print_ir0(target_dir + "/" + f"poseidon_hash_{prime_name}_{size}")
