import pprint
import random
import sys
import functools
from miniwizpl import SecretInt, SecretList, mux, reduce, print_emp

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

strings_present = [
    'os.system(f"python client_request.py {param_string}")',
    'import '
    ]

strings_not_present = [
    'import socket'
    ]

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
outputs = []
for s in strings_present:
    dfa = dfa_from_string(s)
    outputs.append(run_dfa(dfa, file_string) == accept_state)
for s in strings_not_present:
    dfa = dfa_from_string(s)
    outputs.append(run_dfa(dfa, file_string) != accept_state)

# compile the ZK statement to an EMP file
output = functools.reduce(lambda a, b: a & b, outputs)
print_emp('miniwizpl_test.cpp')
