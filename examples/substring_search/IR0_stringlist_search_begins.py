import sys
from miniwizpl import *
from miniwizpl.expr import *
from common.util import *

set_field(2**61-1)

''' Prepping target text and substrings'''

if (len(sys.argv)>1 and sys.argv[1] =="test") or (len(sys.argv)>2 and sys.argv[2] =="debug"):
    file_data=generate_text()
    string_target=generate_target(file_data, "begins")

else:
    string_target =  'not'
    with open(sys.argv[1], 'r') as f:
        file_data = f.read()
    file_data = file_data.split()

print("Text: ", file_data, "\n")
print("Target: ", string_target, "\n")
# Transform the text file to search into miniwizpl format
file_string = SecretList([word_to_integer(_str) for _str in file_data])

zero_state = 0
accept_state=100
error_state=101

def dfa_from_string(target):
    next_state = {}
    next_state[(zero_state, word_to_integer(target))]=accept_state
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
                         mux((initial_state == dfa_state) & (string != dfa_str),
                         error_state,
                         curr_state))

            if len(sys.argv)==3 and sys.argv[2] =="debug":
                print("Updated state: ", val_of(curr_state))

        return curr_state

    if len(sys.argv)==3 and sys.argv[2] =="debug":
        latest_state=reduce_unroll(next_state_fun, text_input, zero_state)
    else:
        latest_state=reduce(next_state_fun, text_input, zero_state)
    return latest_state

dfa = dfa_from_string(string_target)
print("\n", "DFA: ",dfa, "\n")

# define the ZK statement
latest_state = run_dfa(dfa, file_string)
assert0(latest_state - accept_state)

if len(sys.argv)==3 and sys.argv[2] =="debug":
    print("\n", "Latest State: ",val_of(latest_state), "\n")

# compile the ZK statement to an EMP file
print_ir0('miniwizpl_test_ir0')

