import sys
from miniwizpl import *
from miniwizpl.expr import *
from common.util import *

#TODO FIXME : ADD CCC.text check
set_field(2**61-1)

''' Prepping target text and substrings'''
if (len(sys.argv)>2 and (sys.argv[2] =="debug"or sys.argv[2] =="test")):
    file_data=generate_text(int(sys.argv[3]))
    string_a, string_target=generate_target(file_data, "after_all")

else:
    string_a = 'not'
    string_target =  ['in', 'our', 'alphabet']
    with open(sys.argv[1], 'r') as f:
        file_data = f.read()
    file_data = file_data.split()

print("Text: ", file_data, "\n")
print("Start: ", string_a, "\n", "Target: ", string_target, "\n")
# Transform the text file to search into miniwizpl format
file_string = SecretList([word_to_integer(_str) for _str in file_data])

zero_state = 0
found_states=[i for i in range(1,len(string_target)+1)]
if len(found_states)==0:
    accept_state = 100
    error_state = 101
else:
    accept_state = found_states[-1]*10
    error_state = found_states[-1]*100
Secret_str_after = SecretStack([])
str_after = []

def dfa_from_string(first, target):
    next_state = {}
    assert(len(target)>0)
    next_state[(zero_state, word_to_integer(first))]=found_states[0]
    for i in range(0,len(target)-1):
      next_state[(found_states[i], word_to_integer(target[i]))]=found_states[i+1]
    next_state[(found_states[-1], word_to_integer(target[-1]))]=accept_state
    return next_state

# run a dfa
def run_dfa(dfa, text_input):
    def next_state_fun(string, initial_state):
        curr_state=initial_state
        for (dfa_state, dfa_str), next_state in dfa.items():

            if len(sys.argv)==3 and (sys.argv[2] =="debug" or sys.argv[2] =="debug/own") :
                print(
                    "curr state: ", val_of(curr_state),
                    "dfa state: ", dfa_state,"\n",
                    "input string: ", val_of(string),
                    "dfa string: ", dfa_str,"\n",
                    "next_state", next_state,"\n")

            curr_state = mux((initial_state == dfa_state) & (string == dfa_str),
                         next_state,
                         mux((initial_state == dfa_state) & (string != dfa_str) & (initial_state!=zero_state),
                         error_state,
                         curr_state))
                         
            if len(sys.argv)==3 and (sys.argv[2] =="debug" or sys.argv[2] =="debug/own") :
                print("Updated state: ", val_of(curr_state))

        ''' 
            Determine whether or not to go to the error state:
            1) If alreayd in error state, then always error state
            2) If already in accept_state but not the last substring, go to error)
            3) Otherwise stay in the current state
        '''
        curr_state = mux(initial_state == error_state, error_state, 
                     mux(initial_state == accept_state, error_state,
                     curr_state))
        
        ''' 
            Adding sub string if in one of found states
            If you're initially in accept state, it should fail into error state because you were not reading the last word in the text in the previous iteration
        '''
        Secret_str_after.cond_push(is_in_found_states(initial_state, found_states),string)
        return curr_state
    if len(sys.argv)==3 and sys.argv[2] =="debug":
        latest_state=reduce_unroll(next_state_fun, text_input, zero_state)
    else:
        latest_state=reduce(next_state_fun, text_input, zero_state)
    return latest_state

# build DFA
dfa = dfa_from_string(string_a, string_target)
print("\n", "DFA: ",dfa, "\n")

# define the ZK statement
latest_state = run_dfa(dfa, file_string)
assert0(latest_state - accept_state)

run_poseidon_hash(file_string)

if len(sys.argv)==3 and (sys.argv[2] =="debug" or sys.argv[2] =="debug/own") :
    print("\n", "Latest State: ",val_of(latest_state), "\n")
    print("\n", "Result:   ",Secret_str_after.current_val, "\n")
    expected=[word_to_integer(x) for x in string_target]
    print("\n", "Expected: ",expected, "\n")

else:
    # compile the ZK statement to an EMP file
    print_ir0(sys.argv[4]+'/miniwizpl_test_ir0')