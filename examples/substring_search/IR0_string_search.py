import pprint
import random
import sys
import functools
from miniwizpl import *
from miniwizpl.expr import *
from common.util import *

#TODO FIXME : ADD CCC.text check
set_field(2**61-1)

''' Prepping target text and substrings'''
if (len(sys.argv)>2 and (sys.argv[2] =="debug"or sys.argv[2] =="test")):
    file_data=generate_text(int(sys.argv[3]))
    string_target =generate_target(file_data, "string_search")

else:
    string_target =  'in'
    with open(sys.argv[1], 'r') as f:
        file_data = f.read()
    file_data = file_data.split()

print("Text: ", file_data, "\n")
print("Target: ", string_target)
# Transform the text file to search into miniwizpl format
file_string = SecretList([word_to_integer(_str) for _str in file_data])

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
dfa = dfa_from_string(string_target)
print(dfa)
output = run_dfa(dfa, file_string)

assert0((output == accept_state))
print(output)

# compile the ZK statement to an EMP file
print_ir0(sys.argv[4]+'/miniwizpl_test_ir0')
