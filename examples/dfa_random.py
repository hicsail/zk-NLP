import pprint
import random
from miniwizpl import SecretInt, SecretList, mux, public_foreach, print_emp

# the transition function for the DFA
# the accept state is 1000000
# this is a regular Python dict (public)
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
    (7, 33): 1000000,
    (7, 87): 1,
    }

# the next-state function
def next_state(char, state):
    output = 0
    
    # this is a regular Python loop
    for (dfa_state, dfa_char), next_state in dfa.items():
        # state and char will be secret values
        # miniWizPL operators used: mux, ==, &
        output = mux((state == dfa_state) & (char == dfa_char),
                     next_state,
                     output)
    return output

mb_size = .1
kb_size = 1000*mb_size
randlist = [random.randint(1, 100) for _ in range(int(1000*kb_size))]

#string = SecretList([87, 65])
string = SecretList(randlist + [87, 65, 78, 65, 67, 82, 89, 33])
#string = SecretList(randlist)

# this runs a "public foreach" loop, on each element of the string
# the string is represented as a SecretList
# the length of the string is revealed, but not its contents
def dfa_loop(string):
    # miniWizPL operator used: public_foreach
    # public_foreach calls a function on each element of the list
    # it also maintains an accumulator value
    # in each iteration, it calls the function on:
    #  - the element (first argument)
    #  - the current accumulator value (second argument)
    return public_foreach(string,       # list to loop over
                          next_state,   # function to call for each iteration
                          0)            # initial value for loop accumulator
output = dfa_loop(string)
#pprint.pprint(output)

print_emp(output, 'miniwizpl_test.cpp')
