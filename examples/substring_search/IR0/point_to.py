import sys
from miniwizpl import *
from miniwizpl.expr import *
sys.path.append("/usr/src/app/examples/substring_search/common")
from util import *


def dfa_from_string(string_a, target, zero_state, found_states, appendedAll_state, accept_state):
    next_state = {}
    assert(len(target)>0)
    if len(target)==1:
        next_state[(zero_state, word_to_integer(target[0]))]=appendedAll_state
        next_state[(appendedAll_state, word_to_integer(string_a))]=accept_state
        return next_state
    else:
        next_state[(zero_state, word_to_integer(target[0]))]=found_states[0]
        for i in range(1,len(target)-1):
            next_state[(found_states[i-1], word_to_integer(target[i]))]=found_states[i]
        next_state[(found_states[-1], word_to_integer(target[-1]))]=appendedAll_state
        next_state[(appendedAll_state, word_to_integer(string_a))]=accept_state
        return next_state



def run_dfa(dfa, text_input, zero_state, found_states, appendedAll_state, accept_state, error_state, Secret_str_before):
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
                     mux(initial_state == accept_state, accept_state,
                     curr_state))
        
        ''' 
            Adding sub string if in one of found states or accept state and reading the last word in the text
        '''
        Secret_str_before.cond_push(is_in_target_states(curr_state, found_states)|(curr_state == appendedAll_state), string)

        return curr_state
    latest_state=reduce(next_state_fun, text_input, zero_state)
    ''' 
        Pop the last element if no string_a found and if you're reading the last substring of the target strings
        Push negative value if you end up in the error state
    '''
    Secret_str_before.cond_pop(latest_state==appendedAll_state)
    Secret_str_before.cond_push(latest_state==error_state, 1)
    return latest_state



def main(target_dir, prime, prime_name, size, operation):

    # Importing ENV Var & Checking if prime meets our requirement

    assert len(sys.argv) == 6, "Invalid arguments"
    _, target_dir, prime, prime_name, size, operation = sys.argv
    file_name="point_to"
    set_field(int(prime))

    try:
        assert check_prime()== True
    except:
        print("no equivalent prime (2305843009213693951) in ccc.txt")
        sys.exit(1)


    # Prepping target text and substrings

    if operation =="test":
        corpus=generate_text(int(size))
        substring_len=2**int(size)
        piv_len=2**int(size)
        string_a, string_target=generate_target(corpus, file_name, substring_len=substring_len, piv_len=piv_len)
        print("Test (First 10 Strings): ",corpus[0:10])
        print("Actual text length:", len(corpus))

    else:
        string_target =  ['one', 'two'] 
        string_a = 'three'
        with open("/usr/src/app/examples/dfa_test_input.txt", 'r') as f:
            corpus = f.read()
        corpus = corpus.split()
        print("Text: ", corpus, "\n")

    print("Target: ", string_target, "\n", "End: ", string_a, "\n",)
    # Transform the text file to search into miniwizpl format
    file_string = SecretList([word_to_integer(_str) for _str in corpus])

    zero_state = 0
    found_states=[i for i in range(1,len(string_target))]

    if len(found_states)==0:
        appendedAll_state=10
        accept_state = 100
        error_state = 101
    else:
        appendedAll_state=found_states[-1]*10
        accept_state = found_states[-1]*100
        error_state = found_states[-1]*101

    Secret_str_before = SecretStack([], max_size=50)


    # Build and traverse a DFA

    dfa = dfa_from_string(string_a, string_target, zero_state, found_states, appendedAll_state, accept_state)
    # print("\n", "DFA: ",dfa, "\n")
    print("Traversing DFA")
    latest_state = run_dfa(dfa, file_string, zero_state, found_states, appendedAll_state, accept_state, error_state, Secret_str_before)
    print("Output Assertion")
    assert0((latest_state - accept_state)*(latest_state - appendedAll_state))
    print("Running Poseidon Hash")
    run_poseidon_hash(file_string)
    print("\n", "Latest State: ",val_of(latest_state), "\n")

    print("\n", "Result:   ", val_of(Secret_str_before), "\n")


    # Converting strings, target, and corpus into integers, and creating expected list to reconcile the result

    expected=create_exepected_result(file_name, corpus, string_target, string_a)
    print("\n", "Expected: ",expected, "\n") 

    # Reconciling the content of the secret stack
    
    reconcile_secretstack(expected, Secret_str_before)

    if val_of(latest_state)==accept_state or val_of(latest_state)==appendedAll_state:
        print("DFA successfully reached the accept state \n")
    else:
        print("DFA did not reached the accept state \n")

    print("Generating Output for",file_name, "\n")
    print_ir0(target_dir + "/" + f"{file_name}_{prime_name}_{size}")


if __name__ == '__main__':
    main(*sys.argv[1:])