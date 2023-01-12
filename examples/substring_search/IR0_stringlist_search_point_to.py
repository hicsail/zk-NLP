import sys
from miniwizpl import *
from miniwizpl.expr import *
from common.util import *



''' Importing ENV Var & Checking if prime meets our requirement'''
assert len(sys.argv) == 6, "Invalid arguments"
_, target_dir, prime, prime_name, size, operation = sys.argv
file_name="point_to"
set_field(int(prime))

try:
    assert check_prime()== True
except:
    print("no equivalent prime (2305843009213693951) in ccc.txt")
    sys.exit(1)



''' Prepping target text and substrings'''
if operation =="test":
    corpus=generate_text(int(size))
    string_a, string_target=generate_target(corpus, file_name, length=10)
    print("Test (First 10 Strings): ",corpus[0:10])
    print("Actual text length:", len(corpus))

else:
    string_target =  ['one', 'two'] # TODO : Fix is in find state (in case this leng is 1)
    string_a = 'three'
    with open("/usr/src/app/examples/dfa_test_input.txt", 'r') as f:
        corpus = f.read()
    corpus = corpus.split()
    print("Text: ", corpus, "\n")

print("Target: ", string_target, "\n", "End: ", string_a, "\n",)
# Transform the text file to search into miniwizpl format
file_string = SecretList([word_to_integer(_str) for _str in corpus])

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



def run_dfa(dfa, text_input):
    def next_state_fun(string, initial_state):
        curr_state=initial_state
        
        for (dfa_state, dfa_str), next_state in dfa.items():

            # print(
            #             "curr state: ", val_of(curr_state),
            #             "dfa state: ", dfa_state,"\n",
            #             "input string: ", val_of(string),
            #             "dfa string: ", dfa_str,"\n",
            #             "next_state", next_state,"\n")

            curr_state = mux((initial_state == dfa_state) & (string == dfa_str),
                         next_state, 
                         mux((initial_state == dfa_state) & (string != dfa_str),
                         error_state, 
                         curr_state))

            # print("Updated state: ", val_of(curr_state))

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
        Secret_str_before.cond_push(is_in_found_states(curr_state, append_states)|(curr_state == appendedAll_state), string)

        return curr_state
    latest_state=reduce(next_state_fun, text_input, zero_state)
    ''' 
        Pop the last element if no string_b found and if you're read the last substring of the target between strings
    '''
    Secret_str_before.cond_pop(latest_state==appendedAll_state)
    return latest_state



'''Build and traverse a DFA'''
dfa = dfa_from_string(string_a, string_target)
# print("\n", "DFA: ",dfa, "\n")
print("Traversing DFA")
latest_state = run_dfa(dfa, file_string)
print("Output Assertion")
assert0((latest_state - accept_state)*(latest_state - appendedAll_state))
print("Running Poseidon Hash")
run_poseidon_hash(file_string)
print("\n", "Latest State: ",val_of(latest_state), "\n")


print("\n", "Result:   ", val_of(Secret_str_before), "\n")
expected=[word_to_integer(x) for x in string_target]
print("\n", "Expected: ",expected, "\n", "# This debugger does not work if either/both string_a/b is absent \n") 

if val_of(latest_state)==accept_state or val_of(latest_state)==appendedAll_state:
    print("DFA successfully reached the accept state \n")
else:
    print("DFA did not reached the accept state \n")

print("Generating Output \n")
print_ir0(target_dir + "/" + f"{file_name}_{prime_name}_{size}")