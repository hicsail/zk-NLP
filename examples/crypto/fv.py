import sys
import random

from miniwizpl import SecretInt, print_emp, exp_mod, set_bitwidth

q = 2**128
p = q**3

t = 2

def noise():
    return random.randint(-5, 5) % q

def keygen():
    s = random.randint(0, t-1)
    a = random.randint(1, q-1)
    e = noise()
    pk = (-(a*s+e)%q, a)
    return s,pk

def eval_keygen(sk):
    s = sk
    a = random.randint(1, p*q-1)
    e = noise()
    rlk = (-(a*s + e) + p * s**2) % (p*q)
    return (rlk, a)

def encrypt(pk, m):
    p0, p1 = pk
    u = random.randint(0, t-1)
    e1 = noise()
    e2 = noise()
    Delta = (q // t)
    ct1 = (p0*u + e1 + Delta*m) % q
    ct2 = (p1 * u + e2) % q
    return (ct1, ct2)

def decrypt(sk, ct):
    s = sk
    c0, c1 = ct
    print('Decrypt, before rounding:', t * ((c0 + c1 * s) % q) // q)
    m = round(t * ((c0 + c1 * s) % q) // q) % t
    return m

print('p:', p, 'q:', q)
sk, pk = keygen()
print(pk)
m = SecretInt(0)
e = encrypt(pk, m)
print('encrypted', e)
decrypted = decrypt(sk, e)
print('decrypted', decrypted)

set_bitwidth(256)
print_emp(decrypted, 'miniwizpl_test.cpp')
