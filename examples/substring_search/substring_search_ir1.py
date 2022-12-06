import pprint
import random
import sys
import functools
from miniwizpl import *

sys.path.append("../poseidon_hash")
from parameters import *
from hash import Poseidon

if len(sys.argv) != 2:
    print("Usage: python dfa_example.py <target_filename>")
    sys.exit()

# the accept state is 1000000
accept_state = 1000000

# a Python function to create a dfa from a string
# we assume a default transition back to 0
def dfa_from_string(text):
    next_state = {}
    alphabet = set(text)

    for i in range(len(text)):
        for j in alphabet:
            if j == text[i]:
                if i == len(text) - 1:
                    # accept state
                    next_state[(i, ord(j))] = accept_state
                else:
                    next_state[(i, ord(j))] = i+1
            else:
                for k in range(len(text)):
                    try:
                        if text.index(text[k:i] + j) == 0 and k <= i:
                            next_state[(i, ord(j))] = len(text[k:i] + j)
                            break
                    except ValueError:
                        pass
    return next_state

# read the target file & convert to secret string
with open(sys.argv[1], 'r') as f:
    file_data = f.read()

file_string = SecretList([ord(c) for c in file_data])

# run a dfa
def run_dfa(dfa, string):
    def next_state_fun(char, state):
        output = 0

        for (dfa_state, dfa_char), next_state in dfa.items():
            output = mux((state == dfa_state) & (char == dfa_char),
                         next_state,
                         output)

        output = mux(state == accept_state, accept_state, output)
        return output

    return reduce(next_state_fun,
                  string,
                  0)

# define the ZK statement
dfa = dfa_from_string('import')
print(dfa)
output = run_dfa(dfa, file_string)

assert0(~(output == accept_state))
print(output)

# prove validity of the input text by Poseidon Hash
security_level = 128
input_rate = 3
t = input_rate # these should be the same
alpha = 17     # depends on the field size (unfortunately)
prime = 2**61-1
set_field(prime)
poseidon_new = Poseidon(prime, security_level, alpha, input_rate, t)

print('converting to gfs')
split_gfs = file_string.as_field_elements(input_rate)
print('need to do this many hashes:', len(split_gfs))

for g in split_gfs:
    poseidon_digest = poseidon_new.run_hash(g)
    #print('digest:', val_of(poseidon_digest))
    assert0(poseidon_digest - val_of(poseidon_digest))


# compile the ZK statement to an EMP file
print_ir0('miniwizpl_test_ir0')
