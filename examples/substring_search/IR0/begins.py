import sys
from miniwizpl import *
from miniwizpl.expr import *
sys.path.append("/usr/src/app/examples/substring_search/common")
from util import *


def dfa_from_string(target, zero_state, accept_state):
    next_state = {}
    next_state[(zero_state, word_to_integer(target))]=accept_state
    return next_state



def run_dfa(dfa, text_input, zero_state, error_state):
    def next_state_fun(string, initial_state):
        curr_state=initial_state

        for (dfa_state, dfa_str), next_state in dfa.items():
            
            # print(
            #         "curr state: ", val_of(curr_state),
            #         "dfa state: ", dfa_state,"\n",
            #         "input string: ", val_of(string),
            #         "dfa string: ", dfa_str,"\n")

            curr_state = mux((initial_state == dfa_state) & (string == dfa_str),
                         next_state,
                         mux((initial_state == dfa_state) & (string != dfa_str),
                         error_state,
                         curr_state))

            # print("Updated state: ", val_of(curr_state))

        return curr_state
    latest_state=reduce(next_state_fun, text_input, zero_state)
    return latest_state



def main(target_dir, prime, prime_name, size, operation):

    # Importing ENV Var & Checking if prime meets our requirement

    assert len(sys.argv) == 6, "Invalid arguments"
    _, target_dir, prime, prime_name, size, operation = sys.argv
    file_name="begins"
    set_field(int(prime))

    try:
        assert check_prime()== True
    except:
        print("no equivalent prime (2305843009213693951) in ccc.txt")
        sys.exit(1)


    # Prepping target text and substrings

    if operation =="test":
        corpus=generate_text(int(size))
        string_target=generate_target(corpus, file_name)
        print("Test (First 10 Strings): ",corpus[0:10])
        print("Actual text length:", len(corpus))

    else:
        string_target =  'one'
        with open("/usr/src/app/examples/dfa_test_input.txt", 'r') as f:
            corpus = f.read()
        corpus = corpus.split()
        print("Text: ", corpus, "\n")

    print("Target: ", string_target, "\n")


    # Transform the text file to search into miniwizpl format

    file_string = SecretList([word_to_integer(_str) for _str in corpus])

    zero_state = 0
    accept_state=100
    error_state=101


    # Build and traverse a DFA

    dfa = dfa_from_string(string_target, zero_state, accept_state)
    # print("\n", "DFA: ",dfa, "\n")
    print("Traversing DFA")
    latest_state = run_dfa(dfa, file_string, zero_state, error_state)
    print("Output Assertion")
    assert0(latest_state - accept_state)
    print("Running Poseidon Hash")
    run_poseidon_hash(file_string)
    print("\n", "Latest State: ",val_of(latest_state), "\n")

    if val_of(latest_state)==accept_state:
        print("DFA successfully reached the accept state \n")
    else:
        print("DFA did not reached the accept state \n")

    print("Generating Output \n")
    print_ir0(target_dir + "/" + f"{file_name}_{prime_name}_{size}")


if __name__ == '__main__':
    main(*sys.argv[1:])