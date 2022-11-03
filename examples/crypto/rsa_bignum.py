import sys
import random

from miniwizpl import SecretInt, assertTrueEMP, exp_mod, print_emp, set_bitwidth

sys.setrecursionlimit(10000)
# taken from:
# https://stackoverflow.com/questions/41363791/calculating-modulus-for-larger-numbers-in-python
def geom(a, k, n):
    """calculates (1 + a + a^2 + ... + a^(k-1)) mod n)"""
    if k <= 2:
        s = 0
        i = 0
        while k > i:
            s += a**i
            i += 1
        return s % n
        # return sum([a**i for i in range(k)]) % n
    else:
        m = k//2
        b = pow(a,2,n)
        g = ((1+a)*geom(b,m,n))%n
        return g if k%2 == 0 else (g + pow(a,k-1,n))%n

# modular exponentiation
# a^m (mod n)
def mod_exp(a, m, n):
    """ returns aaaa...a (m times) modulo n"""
    k = len(str(a))
    print(k)
    r = pow(10,k,n)
    return (a*geom(r,m,n))%n

def parse(x):
    return int(x.replace(':', ''), 16)

modulus = parse("00:c5:ce:04:c6:bd:88:69:bb:ce:2f:0d:00:f8:93:80:c0:cc:52:96:12:32:cf:01:63:cd:22:3b:ac:04:15:e5:7d:77:02:5a:33:55:c6:4e:4c:cd:8b:f0:af:20:10:c3:c1:0b:22:6d:6c:92:20:ce:a7:79:8a:6b:c0:6b:78:21:59:be:b7:6c:67:a1:15:54:c5:3d:34:1e:ab:ee:0c:2a:67:72:5c:89:45:1b:db:06:10:14:86:30:f9:2a:ac:1e:a5:2d:06:79:b8:3f:d7:ab:f9:a6:73:99:52:a7:23:9e:48:bc:0a:37:72:a9:cf:ef:ea:08:f4:a9:ed:6c:e6:6b:b9:4d:51:1b:29:69:b1:d4:81:f6:fb:7d:2d:7f:36:59:44:c8:17:c0:4a:35:1d:54:52:16:3a:08:a9:57:67:94:74:58:32:15:ca:8f:af:f7:da:30:67:db:a6:df:2a:0f:88:9c:16:0d:05:ad:44:96:08:e2:d8:06:73:db:f1:75:13:bf:60:09:56:01:9d:20:1d:d5:9c:5e:d1:d8:0a:74:ff:70:84:0e:d8:07:02:b6:a0:9b:e7:e7:46:81:aa:f6:1d:ef:4a:99:6b:75:ed:b1:bf:d5:77:23:49:33:c9:29:1d:f9:28:63:27:8d:e6:da:b7:82:bf:86:b3:c9:5b:04:73")

publicExponent = 65537

privateExponent = parse("78:e5:ca:95:8e:12:6a:4d:97:5f:ba:9a:f5:53:72:46:64:9b:b5:8d:b9:f0:3b:f1:3b:d7:c8:91:02:8e:3f:8d:c7:c7:70:4a:20:0a:ec:a0:94:a1:0b:a2:7d:fe:c1:26:a4:1f:8e:b1:e5:3e:98:10:54:80:fe:0a:c5:a4:ce:fd:83:4b:a8:be:4d:fe:33:a9:ba:16:b9:08:6c:9e:92:ec:57:41:a7:c4:cd:99:b8:c2:eb:48:79:76:51:56:92:04:72:d8:9a:5c:ba:e8:9e:fc:1f:78:58:25:e4:72:28:b4:5b:fa:02:99:da:a0:75:0a:9e:1e:ac:1d:a9:89:cc:1c:8a:a6:6e:c0:eb:00:b9:fe:8c:25:b1:a3:7f:cd:25:43:11:95:17:10:73:d3:8b:37:91:49:58:94:11:d6:4e:f7:e8:83:cf:a1:56:93:b2:cf:17:10:56:2b:e1:ba:23:4a:95:18:60:9d:82:d7:2a:3a:8f:4a:74:18:b2:9c:47:b4:7e:a8:71:1a:ca:2a:f4:cc:35:4e:b1:68:6d:82:e8:44:34:eb:21:db:5e:64:58:d9:c9:25:68:16:67:c9:14:62:35:9b:e5:7d:82:13:ec:dd:1c:29:ff:f2:8a:24:54:ea:c5:3b:d2:af:8e:e7:d9:bd:ab:7d:c6:38:e5:06:62:81")

prime1 = parse("00:e8:34:86:db:64:71:f8:bb:21:88:27:5b:ad:ee:28:e1:a1:c1:24:93:25:dd:ff:f7:f5:2a:73:b8:12:6a:cb:75:e7:ce:8d:ff:83:87:48:d5:51:d1:47:c0:55:73:cb:14:43:cc:30:be:f7:62:bc:be:59:6a:27:44:ca:fd:54:9a:31:af:9a:7f:c6:c6:07:75:88:b9:0a:7f:97:85:e3:af:97:2a:e5:2c:fe:a5:7e:c3:ea:2f:cd:aa:fe:4a:41:2f:e6:32:ad:40:5e:81:ab:db:0e:45:f2:a9:51:60:8e:00:1a:f4:52:b2:d7:b5:03:f1:42:1c:85:a3:a8:63:77:4b")

prime2 = parse("00:da:13:0f:7a:2f:2a:0b:bd:63:0c:94:cd:5c:31:9b:e8:b4:5f:3e:ad:53:a1:b4:e9:ec:b3:14:1d:88:00:68:fc:72:c4:9f:54:98:2a:df:92:bd:27:64:1e:a0:5f:e1:22:06:90:fe:a5:e3:b6:eb:6e:44:11:27:82:ab:61:79:ca:8d:25:77:a9:51:74:11:32:b1:07:b0:9d:1c:66:5d:6c:17:03:6d:a0:99:d3:88:c2:59:ae:60:b3:e6:fa:ad:cd:4c:f3:f5:9e:3c:46:c1:d5:ca:78:55:9c:cd:a8:5e:7b:ee:37:2f:02:53:c6:b8:85:b1:ea:51:3d:a9:d7:a6:79")

exponent1 = parse("00:8b:6e:a7:1f:ec:73:c7:90:ce:b4:cc:35:6f:fe:97:8b:cd:2e:86:40:d9:b7:31:b1:fa:04:90:d2:12:35:10:91:6f:2d:87:f4:cb:4d:1b:fe:04:10:30:0e:9d:01:58:0b:86:1e:81:92:da:47:ee:e0:3a:1e:d5:0f:a8:f8:6f:a9:db:75:ff:c7:04:5b:fb:34:a7:71:bd:8d:1a:36:6a:9f:10:9d:d0:59:b1:5b:3d:00:75:8a:58:ec:79:9f:aa:ff:11:32:92:f8:19:07:b2:63:6a:71:b4:21:d9:dc:a9:c8:04:67:7b:95:2a:93:e6:97:23:44:af:36:b3:b1:6e:7b")

exponent2 = parse("07:00:45:a6:ee:8c:b3:03:c9:82:45:e4:b1:e9:05:d0:5a:ba:14:11:0c:76:4c:90:96:00:c9:cc:88:e9:3a:75:a0:59:9f:a3:df:9e:c0:be:bd:43:de:7a:fd:3b:16:c7:38:de:be:ce:24:99:62:c5:8f:79:dd:82:dc:6d:ac:b3:4c:04:bf:ea:b7:aa:ba:42:9e:5c:58:d7:32:6a:36:e5:99:77:8a:b5:75:3a:cd:51:2f:ff:e1:2a:e5:67:76:dc:f8:73:7c:97:2f:e8:35:a0:df:77:2d:88:73:31:cc:96:bd:f7:17:93:43:8d:45:af:45:1e:f8:ac:ba:1f:2a:41")

coefficient = parse("6f:63:ae:03:5f:53:78:ec:b7:3d:ea:97:6e:2c:b4:e7:45:53:07:80:74:92:fb:15:fd:29:83:20:51:a1:c9:12:03:52:2f:5c:70:a9:9e:f2:9a:45:28:6b:ab:1b:92:f6:37:cb:b4:da:c7:ff:51:77:df:60:75:a7:c2:e4:7a:5a:b7:93:6f:de:a1:fd:20:0c:15:b8:dc:8c:33:17:0b:54:0a:01:12:09:9e:b9:d0:60:d0:a3:e3:4b:c2:a8:7a:c4:18:4d:05:3a:68:6f:9c:6f:d6:ee:c9:e6:21:7b:42:32:c1:ef:c3:58:e3:7f:54:66:b5:6a:d6:f0:d3:80:e7:59")

def enc(m):
    return exp_mod(m, publicExponent, modulus)

def dec(c):
    return exp_mod(c, SecretInt(privateExponent), modulus)

m = SecretInt(1)

encrypted_one = enc(m)
print('enc:', encrypted_one)
decrypted_one = dec(encrypted_one)
print('result:', decrypted_one)

assertTrueEMP(decrypted_one == 1)

set_bitwidth(128)
print_emp('miniwizpl_test.cpp')
