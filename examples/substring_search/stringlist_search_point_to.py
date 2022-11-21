import sys
from miniwizpl import *
from miniwizpl.expr import *
from common.util import *

if len(sys.argv) != 2:
    print("Usage: python dfa_example.py <target_filename>")
    sys.exit()

'''
    Change this section to experiment
'''

string_target =  ['not', 'in']
string_a = 'our'
zero_state = 0
append_states=[i for i in range(1,len(string_target))]
appendedAll_state=append_states[-1]*10
accept_state = append_states[-1]*11
error_state = append_states[-1]*100
# Secret_str_before = SecretStack([])
str_before = []

def dfa_from_string(last, target):
    next_state = {}
    assert(len(target)>0)
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
                         mux((initial_state == dfa_state) & (string != dfa_str),
                         error_state, 
                         curr_state))
            print("Updated state: ", val_of(curr_state))

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
        # Secret_str_before.cond_push(initial_state == zero_state,string)
        # print(Secret_str_before.current_val)
        ''' 
            The following part needs to be updated with Stack without if statement
        '''
        if is_in_found_states_todelete(curr_state, append_states)or (val_of(curr_state) == appendedAll_state):
            print("Appended '", integer_to_word(val_of(string)), "' \n")
            str_before.append(integer_to_word(val_of(string)))
        if val_of(curr_state) == error_state and len(str_before)==0:
            print("Error ----------------- \n")
            str_before.append("Error")
        elif val_of(curr_state) == error_state and str_before[-1]!="Error":
            print("Error ----------------- \n")
            str_before.clear()
            str_before.append("Error")
        return curr_state

    # latest_state=public_foreach_unroll(text_input, next_state_fun, zero_state)
    latest_state=public_foreach(text_input, next_state_fun, zero_state)
    ''' 
        Pop the last element if no string_b found and if you're read the last substring of the target between strings
    '''
    # Secret_str_between.cond_pop(loop==appendedAll_state)
    if val_of(latest_state) == appendedAll_state:
        str_before.pop()
    return latest_state

with open(sys.argv[1], 'r') as f:
    file_data = f.read()

# Transform the text file to search into miniwizpl format
file_data = file_data.split()
file_string = SecretList([word_to_integer(_str) for _str in file_data])

dfa = dfa_from_string(string_a, string_target)
print("\n", "DFA: ",dfa, "\n")

# define the ZK statement
latest_state = run_dfa(dfa, file_string)
assertTrueEMP((latest_state == accept_state)|(latest_state == appendedAll_state))
print("\n", "Latest State: ",val_of(latest_state), "\n")
print("\n", "Result: ",str_before, "\n")
# compile the ZK statement to an EMP file
print_emp(True, 'miniwizpl_test.cpp')

