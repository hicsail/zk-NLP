import sys
from miniwizpl import *
from miniwizpl.expr import *
sys.path.append("/usr/src/app/examples/substring_search/common")
from util import *


def dfa_from_string(string_a, target, zero_states, found_states, accept_state):
    next_state = {}
    assert(len(target)>0)
    
    # defining zero states traversal
    for i in range(0,len(zero_states)-1):
      next_state[(zero_states[i], word_to_integer(string_a[i]))]=zero_states[i+1]

    # when the last element in string_a found, move to the first found states
    next_state[(zero_states[-1], word_to_integer(string_a[-1]))]=found_states[0]

    # defining found states traversal
    for i in range(0,len(target)-1):
      next_state[(found_states[i], word_to_integer(target[i]))]=found_states[i+1]
    
    # when the last element in target found, move to the accepted states
    next_state[(found_states[-1], word_to_integer(target[-1]))]=accept_state
    return next_state



def run_dfa(dfa, text_input, zero_states, found_states, accept_state, error_state, Secret_str_after_all):
    def next_state_fun(string, initial_state):
        curr_state=initial_state
        for (dfa_state, dfa_str), next_state in dfa.items():

            # print(
            #     "curr state: ", val_of(curr_state),
            #     "dfa state: ", dfa_state,"\n",
            #     "input string: ", val_of(string),
            #     "dfa string: ", dfa_str,"\n",
            #     "next_state", next_state,"\n")

            curr_state = mux((initial_state == dfa_state) & (string == dfa_str),
                         next_state,
                            mux((initial_state == dfa_state) & (string != dfa_str) & is_in_target_states(initial_state, zero_states),
                            zero_states[0], 
                                mux((initial_state == dfa_state) & (string != dfa_str),
                                error_state,
                                    curr_state)))
                         
            # print("Updated state: ", val_of(curr_state))

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
        Secret_str_after_all.cond_push(is_in_target_states(initial_state, found_states),string)

        ''' 
            When there is a duplicated word(s) and the word is the part of string_a, this algorithm pushes it to the secret stack 
            As soon as the algorithm identifies that the duplicated word it was reading is not part of string_a, then it moves back to zero_state[0]
            Therefore, whenever it's in zero_states[0] and the secretstack is not empty, all contents shall be removed
            The following for loop implements this emptying process
        '''

        for i in range(len(zero_states)):
           
            Secret_str_after_all.cond_pop((curr_state== zero_states[0]) & (len(Secret_str_after_all.val) > 0))

        return curr_state

    latest_state=reduce(next_state_fun, text_input, zero_states[0])
    
    # Push negative value if you end up in the error state
    Secret_str_after_all.cond_push(latest_state==error_state, 1)

    return latest_state



def main(target_dir, prime, prime_name, size, operation):
        
    # Importing ENV Var & Checking if prime meets our requirement

    assert len(sys.argv) == 6, "Invalid arguments"
    _, target_dir, prime, prime_name, size, operation = sys.argv
    file_name="after_all_multi"
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
        string_a = ['manager', 'across', 'marriage', 'field', 'amount', 'ground', 'Style', 'job'] 
        string_target =  ['bring', 'improve', 'sister', 'pick', 'likely', 'because', 'Executive', 'spring'] 
        with open("/usr/src/app/examples/dfa_test_input.txt", 'r') as f:
            corpus = f.read()
        corpus = corpus.split()
        print("Text: ", corpus, "\n")

    print("Start: ", string_a, "\n", "Target: ", string_target, "\n")


    # Transform the text file to search into miniwizpl format
    
    file_string = SecretList([word_to_integer(_str) for _str in corpus])

    zero_states = [i for i in range(0,len(string_a))]
    found_states=[i for i in range(zero_states[-1]+1,zero_states[-1]+len(string_target)+1)]

    if len(found_states)==0:
        accept_state = 100
        error_state = 101
    else:
        accept_state = found_states[-1]*10
        error_state = found_states[-1]*100

    Secret_str_after_all = SecretStack([], max_size=50)


    # Build and traverse a DFA

    dfa = dfa_from_string(string_a, string_target, zero_states, found_states, accept_state)
    print("\n", "DFA: ",dfa, "\n")
    print("Traversing DFA")
    latest_state = run_dfa(dfa, file_string, zero_states, found_states, accept_state, error_state, Secret_str_after_all)
    print("latest_state", val_of(latest_state))
    print("Output Assertion")
    assert0(latest_state - accept_state)
    print("Running Poseidon Hash")
    run_poseidon_hash(file_string)
    print("\n", "Latest State: ",val_of(latest_state), "\n")

    print("\n", "Result:   ", val_of(Secret_str_after_all), "\n")
    expected=create_exepected_result(file_name, corpus, string_target, string_a)
    print("\n", "Expected: ",expected, "\n")

    # Reconciling the content of the secret stack
    reconcile_secretstack(expected, Secret_str_after_all)
       
    if val_of(latest_state)==accept_state:
        print("DFA successfully reached the accept state \n")
    else:
        print("DFA did not reached the accept state \n")
    
    print("Generating Output for",file_name, "\n")
    print_ir0(target_dir + "/" + f"{file_name}_{prime_name}_{size}")


if __name__ == '__main__':
    main(*sys.argv[1:])
