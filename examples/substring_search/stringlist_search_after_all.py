import sys
from miniwizpl import SecretList, mux, public_foreach, print_emp
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

zero_state = 1
accept_state=0
found_state=2
error_state=-1

def dfa_from_string(first, target):
    next_state = {}
    interim_found_state=3 #Explanation inside the run_dfa function
    next_state[(zero_state, word_to_integer(first))]=interim_found_state
    for i in range(len(target)-1):
        next_state[(interim_found_state, word_to_integer(target[i]))]=interim_found_state+1
        interim_found_state+=1
    next_state[(found_state, word_to_integer(target[-1]))]=accept_state

    return next_state

# run a dfa
def run_dfa(dfa, text_input):
    # str_between = SecretStack([])
    str_between = []
    def next_state_fun(string, initial_state):
        curr_state=initial_state
        
        for (dfa_state, dfa_str), next_state in dfa.items():
            ''' 
                This control flow is just for the sake of debugging and must be deleted
            '''
            if (initial_state == found_state) & (val_of(string) == dfa_str):
                print("Found", integer_to_word(val_of(string)), "\n")
            else:
                print("None")

            print(
                "curr state: ", val_of(curr_state),
                "dfa state: ", dfa_state,"\n",
                "input string: ", val_of(string),
                "dfa string: ", dfa_str,"\n")

            curr_state = mux((curr_state == dfa_state) & (string == dfa_str),
                         next_state,
                         mux((curr_state == dfa_state) & (string != dfa_str),
                         error_state,
                         curr_state))

        ''' 
            The following part needs to be updated with Stack without if statement
        '''
        # str_between.cond_push((curr_state == found_state),integer_to_word(val_of(string)))
        if (val_of(curr_state) == accept_state): 
            print("Appended", integer_to_word(val_of(string)), "\n")
            str_between.append(integer_to_word(val_of(string)))
        
        ''' If you found the target string in this iteration, the state will be set interim_found state, which does not exist in DFA, till the end of the current iteration, 
        because right after finding the target string, the next state of the DFA is found_state but the dfa_string of that state is different from our taerget,
        unless the string_a you just found and the target string are same.
        With the interim_found state, subsequent process of this iteration will have no effect, but after the above iteration in the below line, interim_found will be updated to found_state, which exists in the DFA.
        Therefore, the next iteration can examine whether or not the target string immeidately follow the string_a.
        '''
        curr_state = mux(curr_state >2, found_state, curr_state)
        
        '''
        If you have already reached accept_state in the beginning, the returned state will remain final state, no matter what operation is done above
        '''
        curr_state = mux(initial_state == accept_state, accept_state, curr_state)

        return curr_state

    # public_foreach basically runs the above function but returns in an emp format
    loop=public_foreach(text_input, next_state_fun, zero_state)
    return loop, str_between

with open(sys.argv[1], 'r') as f:
    file_data = f.read()

# Transform the text file to search into miniwizpl format
file_data = file_data.split()
file_string = SecretList([word_to_integer(_str) for _str in file_data])

string_a = 'not'
string_target =  ['in', 'our'] 

dfa = dfa_from_string(string_a, string_target)
print("\n", "DFA: ",dfa, "\n")

# define the ZK statement
loop,str_between = run_dfa(dfa, file_string)
print("\n", "Result: ",str_between, "\n")
outputs = (loop == accept_state)

# compile the ZK statement to an EMP file
print_emp(outputs, 'miniwizpl_test.cpp')

