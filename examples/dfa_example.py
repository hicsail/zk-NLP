import pprint
import random
import sys
from miniwizpl import SecretInt, SecretList, mux, reduce, print_emp

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

# read the target file
with open(sys.argv[1], 'r') as f:
    data = f.read()

# convert each character to its ascii code (as an integer)
# and wrap it in a SecretList
string = SecretList([ord(c) for c in data])

# this runs a "reduce" loop, on each element of the string
# the string is represented as a SecretList
# the length of the string is revealed, but not its contents
def dfa_loop(string):
    # miniWizPL operator used: reduce
    # reduce calls a function on each element of the list
    # it also maintains an accumulator value
    # in each iteration, it calls the function on:
    #  - the element (first argument)
    #  - the current accumulator value (second argument)
    return reduce(next_state,   # function to call for each iteration
                  string,       # list to loop over
                  0)            # initial value for loop accumulator

# define the ZK statement
output = dfa_loop(string)
#pprint.pprint(output)

# compile the ZK statement to an EMP file
print_emp('miniwizpl_test.cpp')
