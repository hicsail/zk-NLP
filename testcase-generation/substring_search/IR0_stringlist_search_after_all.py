import sys
from miniwizpl import *
from miniwizpl.expr import *
from common.util import *

''' Checking if prime meets our requirement'''
try:
    assert check_prime()== True
except:
    print("no equivalent prime (2305843009213693951) in ccc.txt")
    sys.exit(1)

assert len(sys.argv) == 5, "Invalid arguments"
_, target_dir, prime, prime_name, size = sys.argv
set_field(int(prime))

''' Prepping target text and substrings'''
file_data=generate_text(int(size))
string_a, string_target=generate_target(file_data, "after_all")

print("Test (First 10 Strings): ",file_data[0:10], "length:", len(file_data))
# print("Text: ", file_data, "\n")
# print("Target: ", string_target)
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
            curr_state = mux((initial_state == dfa_state) & (string == dfa_str),
                         next_state,
                         mux((initial_state == dfa_state) & (string != dfa_str) & (initial_state!=zero_state),
                         error_state,
                         curr_state))
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
        # Secret_str_after.cond_push(is_in_found_states(initial_state, found_states),string)
        return curr_state
    latest_state=reduce(next_state_fun, text_input, zero_state)
    return latest_state

# build DFA
print("Creating DFA")
dfa = dfa_from_string(string_a, string_target)
print("\n", "DFA: ",dfa, "\n")

# define the ZK statement
print("TRaversing DFA")
latest_state = run_dfa(dfa, file_string)
print("Output Assertion")
assert0(latest_state - accept_state)
print("Running Poseidon Hash")
run_poseidon_hash(file_string)
# compile the ZK statement
print("Generating Output")
print_ir0(target_dir + "/" + f"after_all_{prime_name}_{size}")