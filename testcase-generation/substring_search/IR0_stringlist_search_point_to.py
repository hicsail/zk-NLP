import sys
from miniwizpl import *
from miniwizpl.expr import *
from common.util import *

''' Checking if prime meets our requirement'''
txt_dir='./ccc.txt' #Relative to where generate_statements(_ta1)
target='@field (equals (2305843009213693951))'
try:
    assert check_prime(txt_dir, target)== True
except:
    print("no equivalent prime (2305843009213693951) in ccc.txt")
    sys.exit(1)

assert len(sys.argv) == 5, "Invalid arguments"
_, target_dir, prime, prime_name, size = sys.argv
set_field(int(prime))

''' Prepping target text and substrings'''
file_data=generate_text(int(size))
string_a, string_target=generate_target(file_data, "point_to")

print("Text: ", file_data, "\n")
print("Target: ", string_target, "\n", "End: ", string_a, "\n",)
# Transform the text file to search into miniwizpl format
file_string = SecretList([word_to_integer(_str) for _str in file_data])


zero_state = 0
append_states=[i for i in range(1,len(string_target))]

if len(append_states)==0:
    appendedAll_state=10
    accept_state = 100
    error_state = 101
else:
    appendedAll_state=append_states[-1]*10
    accept_state = append_states[-1]*100
    error_state = append_states[-1]*101

Secret_str_before = SecretStack([])
str_before = []

def dfa_from_string(last, target):
    next_state = {}
    assert(len(target)>0)
    if len(target)==1:
        next_state[(zero_state, word_to_integer(target[0]))]=appendedAll_state
        next_state[(appendedAll_state, word_to_integer(last))]=accept_state
        return next_state
    else:
        next_state[(zero_state, word_to_integer(target[0]))]=append_states[0]
        for i in range(1,len(target)-1):
            next_state[(append_states[i-1], word_to_integer(target[i]))]=append_states[i]
        next_state[(append_states[-1], word_to_integer(target[-1]))]=appendedAll_state
        next_state[(appendedAll_state, word_to_integer(last))]=accept_state
        return next_state

# run a dfa
def run_dfa(dfa, text_input):
    def next_state_fun(string, initial_state):
        curr_state=initial_state
        for (dfa_state, dfa_str), next_state in dfa.items():
            curr_state = mux((initial_state == dfa_state) & (string == dfa_str),
                         next_state, 
                         mux((initial_state == dfa_state) & (string != dfa_str),
                         error_state, 
                         curr_state))
        ''' 
            1) If alreayd in error state, then always error state
            2) If already in accept_state, then always accept_state
            3) Otherwise stay in the current state
        '''
        curr_state = mux(initial_state == error_state, error_state, 
                     mux(initial_state == accept_state,accept_state,
                     curr_state))
        
        ''' 
            Adding sub string if in one of found states or accept state and reading the last word in the text
        '''
        # Secret_str_before.cond_push(is_in_found_states(curr_state, append_states)|(curr_state == appendedAll_state), string)

        return curr_state
    latest_state=reduce(next_state_fun, text_input, zero_state)
    ''' 
        Pop the last element if no string_b found and if you're read the last substring of the target between strings
    '''
    # Secret_str_before.cond_pop(latest_state==appendedAll_state)
    return latest_state

# build DFA
dfa = dfa_from_string(string_a, string_target)
print("\n", "DFA: ",dfa, "\n")

# define the ZK statement
latest_state = run_dfa(dfa, file_string)
assert0((latest_state - accept_state)*(latest_state - appendedAll_state))

# compile the ZK statement
print_ir0(target_dir + "/" + f"point_to_{prime_name}_{size}")