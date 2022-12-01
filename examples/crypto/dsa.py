import random
import sys
import galois
from miniwizpl import *

BITWIDTH = 128
set_bitwidth(BITWIDTH)

# Generate the parameters for DSA
def gen_params():
    N = 8
    L = 12  # we get this many bits of security

    q = galois.random_prime(N)
    p = galois.random_prime(L)
    while (p-1)%q != 0:
        p = galois.next_prime(p)

    h = 2
    g = pow(h, (p-1)//q, p)
    return p, q, g

p, q, g = gen_params()

print('bitwidth p:', p.bit_length())
print('bitwidth q:', q.bit_length())
print('g:', g)

h = random.randint(2, p-2)

# Generate keys
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
assertTrueEMP(output)
print_emp('miniwizpl_test.cpp')
