import sys
from miniwizpl import *
from miniwizpl.expr import *
from common.util import *

''' Prepping target text and substrings'''

if (len(sys.argv)>1 and sys.argv[1] =="test") or (len(sys.argv)>2 and sys.argv[2] =="debug"):
    file_data=generate_text()
    string_a, string_target=generate_target(file_data, "after")

else:
    string_a = 'not'
    string_target =  'in'
    with open(sys.argv[1], 'r') as f:
        file_data = f.read()
    file_data = file_data.split()

print("Text: ", file_data, "\n")
print("Start: ", string_a, "\n", "Target: ", string_target, "\n")
# Transform the text file to search into miniwizpl format
file_string = SecretList([word_to_integer(_str) for _str in file_data])

zero_state = 0
found_state=1 
accept_state=100
error_state=-100


def dfa_from_string(first, target):
    next_state = {}
    next_state[(zero_state, word_to_integer(first))]=found_state
    next_state[(found_state, word_to_integer(target))]=accept_state
    return next_state

# run a dfa
def run_dfa(dfa, text_input):
    def next_state_fun(string, initial_state):
        curr_state=initial_state
        for (dfa_state, dfa_str), next_state in dfa.items():

            if len(sys.argv)==3 and sys.argv[2] =="debug":
                print(
                    "curr state: ", val_of(curr_state),
                    "dfa state: ", dfa_state,"\n",
                    "input string: ", val_of(string),
                    "dfa string: ", dfa_str,"\n")

            curr_state = mux((initial_state == dfa_state) & (string == dfa_str),
                         next_state,
                         mux((initial_state == dfa_state) & (string != dfa_str) & (initial_state!=zero_state),
                         error_state,
                         curr_state))
            
            if len(sys.argv)==3 and sys.argv[2] =="debug":
                print("Updated state: ", val_of(curr_state))
        
        ''' 
            Regardless of changes above, if
            1) already in accept state, always accept state
            2) already in error state, always error state
        '''
        curr_state = mux(initial_state == accept_state, accept_state, 
                     mux(initial_state == error_state, error_state, 
                     curr_state))
        
        return curr_state

    if len(sys.argv)==3 and sys.argv[2] =="debug":
        latest_state=public_foreach_unroll(text_input, next_state_fun, zero_state)
    else:
        latest_state=public_foreach(text_input, next_state_fun, zero_state)
    return latest_state

dfa = dfa_from_string(string_a, string_target)
print("\n", "DFA: ",dfa, "\n")

# define the ZK statement
latest_state = run_dfa(dfa, file_string)
assert0(latest_state - accept_state)

if len(sys.argv)==3 and sys.argv[2] =="debug":
    print("\n", "Latest State: ",val_of(latest_state), "\n")
    
# compile the ZK statement to an EMP file
print_ir0('miniwizpl_test_ir0')

