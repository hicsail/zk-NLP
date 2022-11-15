import sys
from miniwizpl import *
from miniwizpl.expr import *

if len(sys.argv) != 2:
    print("Usage: python dfa_example.py <target_filename>")
    sys.exit()

def word_to_integer(word):
    hash = 0

    for i in range(len(word)):
        hash += (ord(word[i]) << 8 * i)

    return hash

def integer_to_word(integer):
    word=""
    bit = (1<<8)-1
    while integer>0:
        bit_char = integer&bit
        integer=integer>>8
        char=chr(bit_char)
        word+=char
    return word

'''
    Change this section to experiment
'''
string_a = 'import'
string_b = 'socket'
string_target = ['numpy','import','import']
zero_state = 0
found_states=[i for i in range(1,len(string_target)+1)]
appendedAll_state = found_states[-1]*10
accept_state = found_states[-1]*11
error_state = found_states[-1]*100

def dfa_from_string(first,target,last):
    next_state = {}
    assert(len(target)>0)
    next_state[(zero_state, word_to_integer(first))]=found_states[0]
    for i in range(0,len(target)-1):
      next_state[(found_states[i], word_to_integer(target[i]))]=found_states[i+1]
    next_state[(found_states[-1], word_to_integer(target[-1]))]=appendedAll_state
    next_state[(appendedAll_state, word_to_integer(last))]=accept_state
    return next_state

def flip_interim_found_state(curr_state):
    x=len(found_states)
    res=""
    for i in range(1,x+1):
        res += f"mux(curr_state=={-i}, {i},"
    res += "curr_state"
    for i in range(1,x+1):
        res += ")"
    # print(res, '\n')
    return eval(res,{'curr_state':curr_state, 'mux':mux, 'val_of':val_of})

def is_in_found_states(initial_state):
    res="("
    for val in found_states:
        res += "(initial_state=="
        res += f"{val}"
        res += ")|"
    res=res[0:-1]
    res += ")"
    # print(res, '\n')
    return eval(res,{'initial_state':initial_state})

# run a dfa
def run_dfa(dfa, text_input):
    Secret_str_between = SecretStack([])
    def next_state_fun(string, initial_state):
        curr_state=initial_state
        for (dfa_state, dfa_str), next_state in dfa.items():
            curr_state = mux((curr_state == dfa_state) & (string == dfa_str),
                         -next_state,
                         mux((curr_state == dfa_state) & (curr_state >0) & (curr_state!=appendedAll_state) & (string != dfa_str),
                         error_state,
                         curr_state))
                         
        ''' Flip the current state if Found/Accepted this iteration
            If you found the target string in this iteration, the state will be set interim_found state, which does not exist in DFA, till the end of the current iteration, 
            because right after finding the target string, the next state of the DFA is found_state but the dfa_string of that state is different from our taerget,
            unless the string_a you just found and the target string are same.
            With the interim_found state, subsequent process of this iteration will have no effect, but after the above iteration in the below line, interim_found will be updated to found_state, which exists in the DFA.
            Therefore, the next iteration can examine whether or not the target string immeidately follow the string_a.
        '''
        curr_state=flip_interim_found_state(curr_state)

        ''' 
            Combined transformation for all error state, accept state, and illegal case(accept state in the middle of the input text)
        '''
        curr_state = mux(initial_state == accept_state, accept_state, mux(initial_state == error_state, error_state, curr_state))
                         
        Secret_str_between.cond_push(is_in_found_states(initial_state)|(curr_state == appendedAll_state)|(curr_state == -accept_state),string)
        print(Secret_str_between.current_val)
        ''' 
            Adding sub string if in one of found states or accept state, reading the last word in the text
        '''
        curr_state=mux(curr_state == -appendedAll_state, appendedAll_state, mux(curr_state == -accept_state, accept_state, curr_state))
        
        return curr_state

    # public_foreach basically runs the above function but returns in an emp format
    loop=public_foreach(text_input, next_state_fun, zero_state)
    ''' 
        Pop the last element if no string_b found and if you're read the last substring of the target between strings
    '''
    Secret_str_between.cond_pop(loop==appendedAll_state)

    return loop, Secret_str_between

with open(sys.argv[1], 'r') as f:
    file_data = f.read()

# Transform the text file to search into miniwizpl format
file_data = file_data.split()
file_string = SecretList([word_to_integer(_str) for _str in file_data])

dfa = dfa_from_string(string_a, string_target, string_b)
print("\n", "DFA: ",dfa, "\n")

# define the ZK statement
latest_state ,Secret_str_between = run_dfa(dfa, file_string)
print("\n", "Result: ",Secret_str_between.current_val, "\n")
# assertTrueEMP((latest_state == accept_state)|(latest_state == appendedAll_state))
assertTrueEMP((latest_state == accept_state)|(latest_state == appendedAll_state))
print("\n", "Latest State: ",val_of(latest_state), "\n")
# compile the ZK statement to an EMP file
print_emp(True, 'miniwizpl_test.cpp')