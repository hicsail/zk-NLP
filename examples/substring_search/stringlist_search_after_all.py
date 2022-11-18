import sys
from miniwizpl import *
from miniwizpl.expr import *
from common.util import *

if len(sys.argv) != 2:
    print("Usage: python dfa_example.py <target_filename>")
    sys.exit()

file_data=generate_text()
string_a, string_target=generate_target(file_data, "after_all")
print("start: ", string_a, "\n", "target: ", string_target, "\n")

'''
    Change this section to experiment
'''

zero_state = 0
found_states=[i for i in range(1,len(string_target)+1)]
accept_state = found_states[-1]*10
error_state = found_states[-1]*100
# Secret_str_after = SecretStack([])
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
            ''' 
                This control flow is just for the sake of debugging and must be deleted
            '''
            # if (val_of(curr_state) in found_states) & (val_of(string) == dfa_str):
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
            Adding sub string if in one of found states or accept state and reading the last word in the text
        '''
        # Secret_str_after.cond_push(is_in_found_states(initial_state, found_states)|(curr_state == accept_state) & isLaststring(string, file_data),string)
        # print(Secret_str_between.current_val)
        ''' 
            The following part needs to be updated with Stack without if statement
        '''
        if (is_in_found_states_todelete(initial_state, found_states)) or (val_of(curr_state) == accept_state):
            print("Appended '", integer_to_word(val_of(string)), "' \n")
            str_after.append(integer_to_word(val_of(string)))
        if (val_of(curr_state) == error_state and str_after[-1]!="Error") or (val_of(initial_state) == accept_state):
            print("Error ----------------- \n")
            str_after.clear()
            str_after.append("Error")
        return curr_state

    # latest_state=public_foreach_unroll(text_input, next_state_fun, zero_state)
    latest_state=public_foreach(text_input, next_state_fun, zero_state)
    return latest_state

file_string = SecretList([word_to_integer(_str) for _str in file_data])

# build DFA
dfa = dfa_from_string(string_a, string_target)
print("\n", "DFA: ",dfa, "\n")

# define the ZK statement
latest_state = run_dfa(dfa, file_string)
assertTrueEMP(latest_state == accept_state)
print("\n", "Latest State: ",val_of(latest_state), "\n")
print("\n", "Result: ",str_after, "\n")
# compile the ZK statement to an EMP file
print_emp(True, 'miniwizpl_test.cpp')

