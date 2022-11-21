import sys
from miniwizpl import *
from miniwizpl.expr import *
from common.util import *

if len(sys.argv) != 2:
    print("Usage: python dfa_example.py <target_filename>")
    sys.exit()

string_target = 'not'
zero_state = 0
accept_state=1
error_state=accept_state*100

def dfa_from_string(target):
    next_state = {}
    next_state[(zero_state, word_to_integer(target))]=accept_state
    return next_state

# run a dfa
def run_dfa(dfa, text_input):
    def next_state_fun(string, initial_state):
        curr_state=initial_state

        for (dfa_state, dfa_str), next_state in dfa.items():
            ''' 
                This control flow is just for the sake of debugging and must be deleted
            '''
            print(
                "curr state: ", val_of(curr_state),
                "dfa state: ", dfa_state,"\n",
                "input string: ", val_of(string),
                "dfa string: ", dfa_str,"\n")

            curr_state = mux((initial_state == dfa_state) & (string == dfa_str),
                         next_state,
                         mux((initial_state == dfa_state) & (string != dfa_str),
                         error_state,
                         curr_state))
        
        return curr_state

    # latest_state=public_foreach_unroll(text_input, next_state_fun, zero_state)
    latest_state=public_foreach(text_input, next_state_fun, zero_state)
    return latest_state

with open(sys.argv[1], 'r') as f:
    file_data = f.read()

# Transform the text file to search into miniwizpl format
file_data = file_data.split()
file_string = SecretList([word_to_integer(_str) for _str in file_data])

dfa = dfa_from_string(string_target)
print("\n", "DFA: ",dfa, "\n")

# define the ZK statement
latest_state = run_dfa(dfa, file_string)
assertTrueEMP(latest_state == accept_state)
print("\n", "Latest State: ",val_of(latest_state), "\n")
# compile the ZK statement to an EMP file
print_emp(True, 'miniwizpl_test.cpp')

