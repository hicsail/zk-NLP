import sys
from miniwizpl import *
from miniwizpl.expr import *
sys.path.append("/usr/src/app/examples/substring_search/common")
from util import *


def dfa_from_string(string_a, target, string_b, zero_states, found_states, appendedAll_state, closing_states, accept_state):
    next_state = {}
    assert(len(target)>0)

    # defining zero states traversal
    for i in range(0,len(zero_states)-1):
        next_state[(zero_states[i], word_to_integer(string_a[i]))]=zero_states[i+1]

    next_state[(zero_states[-1], word_to_integer(string_a[-1]))]=found_states[0]
    
    for i in range(0,len(target)-1):
      next_state[(found_states[i], word_to_integer(target[i]))]=found_states[i+1]
    
    # when the last element in target found, move to the appendedall states
    next_state[(found_states[-1], word_to_integer(target[-1]))]=appendedAll_state

    if len(string_b)==1:
        next_state[(appendedAll_state, word_to_integer(string_b[0]))]=accept_state
    else:
        next_state[(appendedAll_state, word_to_integer(string_b[0]))]=closing_states[0]

        # Traversing b_string and closing states
        for i in range(1,len(closing_states)):
            if len(string_b)-1==i:
                next_state[(closing_states[i-1], word_to_integer(string_b[i]))]=accept_state
            
            else:
                print(string_b[i])
                next_state[(closing_states[i-1], word_to_integer(string_b[i]))]=closing_states[i]
    
    
    return next_state



def run_dfa(dfa, text_input, zero_states, found_states, appendedAll_state, closing_states, accept_state, error_state, Secret_str_between):
    def next_state_fun(string, initial_state):
        curr_state=initial_state
        for (dfa_state, dfa_str), next_state in dfa.items():

            # print(
            #         "curr state: ", val_of(curr_state),
            #         "dfa state: ", dfa_state,"\n",
            #         "input string: ", val_of(string),
            #         "dfa string: ", dfa_str,"\n",
            #         "next_state", next_state,"\n")

            curr_state = mux((initial_state == dfa_state) & (string == dfa_str),
                         next_state,
                         mux((initial_state == dfa_state) & (string != dfa_str) & (initial_state!=zero_states[0]),
                         error_state,
                         curr_state))
                         
            # print("Updated state: ", val_of(curr_state))                     

        ''' 
            Regardless of changes above, if
            1) already in accept state, always accept state
            2) already in error state, always error state
        '''
        curr_state = mux(initial_state == accept_state, accept_state, 
                     mux(initial_state == error_state, error_state, 
                     curr_state))
        ''' 
            Add substring if in one of zero_state(except first), found states, and accept state
        '''
        Secret_str_between.cond_push(is_in_target_states(curr_state, zero_states[1:])|is_in_target_states(curr_state, found_states)|(curr_state == appendedAll_state),string)
        return curr_state
    latest_state=reduce(next_state_fun, text_input, zero_states[0])

    ''' 
        Pop the last len(string_b) elements if no string_b found and if you're reading the last substring of the target strings
        Push negative value if you end up in the error state
    '''
    for i in range(0, len(closing_states)):
        Secret_str_between.cond_pop(latest_state==appendedAll_state)

    Secret_str_between.cond_push(latest_state==error_state, -1)
    return latest_state



def main(target_dir, prime, prime_name, size, operation):

    # Importing ENV Var & Checking if prime meets our requirement

    assert len(sys.argv) == 6, "Invalid arguments"
    _, target_dir, prime, prime_name, size, operation = sys.argv
    file_name="between_multi"
    set_field(int(prime))

    try:
        assert check_prime()== True
    except:
        print("no equivalent prime (2305843009213693951) in ccc.txt")
        sys.exit(1)


    # Prepping target text and substrings

    if operation =="test":
        corpus=generate_text(int(size))
        substring_len=1
        piv_len=1
        string_a, string_target, string_b =generate_target(corpus, file_name, substring_len=substring_len, piv_len=piv_len)
        print("Test (First 10 Strings): ",corpus[0:10])
        print("Actual text length:", len(corpus))

    else:
        string_a = ['one']
        string_target =  ['two']
        string_b = ['three']
        with open("/usr/src/app/examples/dfa_test_input.txt", 'r') as f:
            corpus = f.read()
        corpus = corpus.split()
        print("Text: ", corpus, "\n")

    print("Start: ", string_a, "\n", "Target: ", string_target, "\n", "End: ", string_b)


    # Transform the text file to search into miniwizpl format
    
    file_string = SecretList([word_to_integer(_str) for _str in corpus])

    zero_states = [i for i in range(0,len(string_a))]
    found_states=[i for i in range(zero_states[-1]+1,zero_states[-1]+len(string_target)+1)]
    appendedAll_state=found_states[-1]*10
    closing_states=[i for i in range(appendedAll_state+1, appendedAll_state+len(string_b)+1)]
    accept_state = found_states[-1]*100
    error_state = found_states[-1]*100+1

    Secret_str_between = SecretStack([])
    

    #Build and traverse a DFA

    dfa = dfa_from_string(string_a, string_target, string_b, zero_states, found_states, appendedAll_state, closing_states, accept_state)
    print("\n", "DFA: ",dfa, "\n")
    print("Traversing DFA")
    latest_state = run_dfa(dfa, file_string, zero_states, found_states, appendedAll_state, closing_states, accept_state, error_state, Secret_str_between)
    print("Output Assertion")
    assert0((latest_state - accept_state)*(latest_state - appendedAll_state))
    print("Running Poseidon Hash")
    run_poseidon_hash(file_string)
    print("\n", "Latest State: ",val_of(latest_state), "\n")
        

    # Converting strings, target, and corpus into integers, and creating expected list to reconcile the result

    print("\n", "Result:   ", val_of(Secret_str_between), "\n")
    expected=create_exepected_result(file_name, corpus, string_target, string_a, string_b)
    print("\n", "Expected: ",expected, "\n") 


    # Reconciling the content of the secret stack

    reconcile_secretstack(expected, Secret_str_between)

    if val_of(latest_state)==accept_state or val_of(latest_state)==appendedAll_state:
        print("DFA successfully reached the accept state \n")
    else:
        print("DFA did not reached the accept state \n")

    print("Generating Output \n")
    print_ir0(target_dir + "/" + f"{file_name}_{prime_name}_{size}")


if __name__ == '__main__':
    main(*sys.argv[1:])