import sys
from miniwizpl import *
from miniwizpl.expr import *
sys.path.append("/usr/src/app/examples/substring_search/common")
from util import *

if (len(sys.argv)>1 and sys.argv[1] =="test") or (len(sys.argv)>2 and sys.argv[2] =="debug"):
    file_data=generate_text()
    string_a, string_target, string_b =generate_target(file_data, "between")

else:
    string_a = 'not'
    string_target =  ['in', 'our']
    string_b = 'alphabet'
    with open(sys.argv[1], 'r') as f:
        file_data = f.read()
    file_data = file_data.split()

print("Text: ", file_data, "\n")
print("Start: ", string_a, "\n", "Target: ", string_target, "\n", "End: ", string_b)
# Transform the text file to search into miniwizpl format
file_string = SecretList([word_to_integer(_str) for _str in file_data])

zero_state = 0
found_states=[i for i in range(1,len(string_target)+1)]
if len(found_states)==0:
    appendedAll_state=10
    accept_state = 100
    error_state = -100
else:
    appendedAll_state=found_states[-1]*10
    accept_state = found_states[-1]*100
    error_state = found_states[-1]*-100

Secret_str_between = SecretStack([])
str_between = []

def dfa_from_string(first,target,last):
    next_state = {}
    if len(target)>0:
        next_state[(zero_state, word_to_integer(first))]=found_states[0]
        for i in range(0,len(target)-1):
            next_state[(found_states[i], word_to_integer(target[i]))]=found_states[i+1]
            next_state[(found_states[-1], word_to_integer(target[-1]))]=appendedAll_state
            next_state[(appendedAll_state, word_to_integer(last))]=accept_state
    else:
        next_state[(zero_state, word_to_integer(first))]=1
        for i in range(0,len(target)-1):
            next_state[(1, word_to_integer(last))]=accept_state
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
            Regardless of changes above, if
            1) already in accept state, always accept state
            2) already in error state, always error state
        '''
        curr_state = mux(initial_state == accept_state, accept_state, 
                     mux(initial_state == error_state, error_state, 
                     curr_state))
        ''' 
            Add substring if in one of found states or accept state and reading the last word in the text
        '''
        Secret_str_between.cond_push(is_in_target_states(curr_state, found_states)|(curr_state == appendedAll_state),string)
        return curr_state

    if len(sys.argv)==3 and sys.argv[2] =="debug":
        latest_state=reduce_unroll(next_state_fun, text_input, zero_state)
    else:
        latest_state=reduce(next_state_fun, text_input, zero_state)

    ''' 
        Pop the last element if no string_b found and if you're read the last substring of the target between strings
    '''
    Secret_str_between.cond_pop(latest_state==appendedAll_state)
    return latest_state

# build DFA
dfa = dfa_from_string(string_a, string_target, string_b)
print("\n", "DFA: ",dfa, "\n")

# define the ZK statement
latest_state = run_dfa(dfa, file_string)
assertTrueEMP((latest_state == accept_state)|(latest_state == appendedAll_state))

if len(sys.argv)==3 and (sys.argv[2] =="debug" or sys.argv[2] =="debug/own") :
    print("\n", "Latest State: ",val_of(latest_state), "\n")
    print("\n", "Result:   ",Secret_str_between.current_val, "\n")
    expected=[word_to_integer(x) for x in string_target]
    expected.insert(0, word_to_integer(string_a))
    print("\n", "Expected: ",expected, "\n")

else:
    # compile the ZK statement to an EMP file
    print_emp('miniwizpl_test.cpp')
