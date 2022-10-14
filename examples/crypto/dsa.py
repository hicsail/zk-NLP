import random
import sys

from cryptography.hazmat.primitives.asymmetric import dsa
from miniwizpl import assertFalseEMP, SecretInt, print_emp, exp_mod, set_bitwidth, pow

private_key = dsa.generate_private_key(key_size=2048)
p = private_key.parameters().parameter_numbers()._p
q = private_key.parameters().parameter_numbers()._q

print('bitwidth p:', p.bit_length())
print('bitwidth q:', q.bit_length())

h = random.randint(2, p-2)

g = private_key.parameters().parameter_numbers()._g
print('g:', g)

def gen_key():
    x = random.randint(1, q-1)
    y = pow(g, x, p)
    return x, y

sk, pk = gen_key()
print('secret key:', sk)
print('public key:', pk)
m = 5

def sign(m):
    k = random.randint(1, q-1)
    r = pow(g, k, p) % q
    s = (pow(k, q-2, q) * (m + sk*r)) % q
    return r, s

def verify(r, s, m):
    w = pow(s, q-2, q)
    u1 = (m*w) % q
    u2 = (r*w) % q
    v = ((pow(g, u1, p) * pow(pk, u2, p)) % p) % q
    return v == r

r, s = sign(m)
print('r:', r)
print('s:', s)

output = verify(r, s, SecretInt(m))
output = assertFalseEMP(~output)
set_bitwidth(2048)
print_emp(output, 'miniwizpl_test.cpp')
