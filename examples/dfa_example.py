import pprint
import random
import sys
from miniwizpl import SecretInt, SecretList, assertTrueEMP, mux, print_emp, reduce

if len(sys.argv) != 2:
    print("Usage: python dfa_example.py <target_filename>")
    sys.exit()

# the transition function for the DFA
# the accept state is 1000000
# this is a regular Python dict (public)
# the DFA here looks for the string WANACRY!
accept_state = 1000000
dfa = {
    (0, 87): 1,
    (1, 65): 2,
    (1, 87): 1,
    (2, 78): 3,
    (2, 87): 1,
    (3, 65): 4,
    (3, 87): 1,
    (4, 67): 5,
    (4, 87): 1,
    (5, 82): 6,
    (5, 87): 1,
    (6, 87): 1,
    (6, 89): 7,
    (7, 33): accept_state,
    (7, 87): 1,
    }

# the next-state function
def next_state(char, state):
    output = 0

    # this is a regular Python loop
    # for each possible transition, check if it applies
    for (dfa_state, dfa_char), next_state in dfa.items():
        # state and char will be secret values
        # miniWizPL operators used: mux, ==, &
        output = mux((state == dfa_state) & (char == dfa_char),
                     next_state,
                     output)

 # if we're in the accept state, stay in it
    output = mux(state == accept_state, accept_state, output)
    return output

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
with open(sys.argv[1], "r") as f:
    file_data = f.read()
file_string = SecretList([ord(c) for c in file_data])

# function for running a DFA
def run_dfa(dfa, string):
    def next_state_fun(state, char):
        output = 0

        for (dfa_state, dfa_char), next_state in dfa.items():
            output = mux((state == dfa_state) &
                         (char == dfa_char),
                         next_state,
                         output)

        output = mux(state == accept_state,
                     accept_state,
                     output)
        return output

    return reduce(next_state_fun,
                  string,
                  0)

# search for strings present & not present
dfa1 = dfa_from_string('os.system(f"python client_request.py')
assertTrueEMP(run_dfa(dfa1, file_string) == accept_state)

dfa2 = dfa_from_string("import socket")
assertTrueEMP(run_dfa(dfa2, file_string) != accept_state)

print_emp("miniwizpl_test.cpp")
