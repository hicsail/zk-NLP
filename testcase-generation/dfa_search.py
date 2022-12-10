import pprint
import random
import sys
import functools
import string
from miniwizpl import *

assert len(sys.argv) == 5, "Invalid arguments"
_, target_dir, prime, prime_name, size = sys.argv
prime = int(prime)
set_field(prime)
n = 2**int(size)

file_data = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=n))
target_string = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=int(size)))

accept_state = 1000

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

# simulated bytes of the file
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
dfa = dfa_from_string(target_string)
#print(dfa)
output = run_dfa(dfa, file_string)

assert0(output - val_of(output))
print_ir0(target_dir + "/" + f"dfa_search_{prime_name}_{size}")
