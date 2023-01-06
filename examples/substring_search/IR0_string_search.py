import sys
from miniwizpl import *
from miniwizpl.expr import *
from common.util import *



''' Importing ENV Var & Checking if prime meets our requirement'''
assert len(sys.argv) == 6, "Invalid arguments"
_, target_dir, prime, prime_name, size, operation = sys.argv
file_name="string_search"
set_field(int(prime))

try:
    assert check_prime()== True
except:
    print("no equivalent prime (2305843009213693951) in ccc.txt")
    sys.exit(1)



''' Prepping target text and substrings'''
if operation =="test":
    corpus=generate_text(int(size))
    string_target =generate_target(corpus, file_name)
    print("Test (First 10 Strings): ",corpus[0:10])
    print("Actual text length:", len(corpus))

else:
    string_target = 'one'
    with open("/usr/src/app/examples/dfa_test_input.txt", 'r') as f:
        corpus = f.read()
    corpus = corpus.split()
    print("Text: ", corpus, "\n")

print("Target: ", string_target, "\n")
# Transform the text file to search into miniwizpl format
file_string = SecretList([word_to_integer(_str) for _str in corpus])

accept_state = 1000000



def dfa_from_string(text):
    next_state = {}
    alphabet = set(text)

    for i in range(len(text)):
        for j in alphabet:
            if j == text[i]:
                if i == len(text) - 1:
                    # accept state
                    next_state[(i, ord(j))] = accept_state
                else:
                    next_state[(i, ord(j))] = i+1
            else:
                for k in range(len(text)):
                    try:
                        if text.index(text[k:i] + j) == 0 and k <= i:
                            next_state[(i, ord(j))] = len(text[k:i] + j)
                            break
                    except ValueError:
                        pass
    return next_state



def run_dfa(dfa, string):
    def next_state_fun(char, state):
        curr_state = 0

        for (dfa_state, dfa_char), next_state in dfa.items():

            print(
                "curr state: ", val_of(curr_state),
                "dfa state: ", dfa_state,"\n",
                "input string: ", val_of(string),
                "dfa string: ", dfa_char,"\n",
                "next_state", next_state,"\n")

            curr_state = mux((state == dfa_state) & (char == dfa_char),
                         next_state,
                         curr_state)

            print("Updated state: ", val_of(curr_state))

        curr_state = mux(state == accept_state, accept_state, curr_state)
        return curr_state
    latest_state = reduce(next_state_fun, string, 0)
    return latest_state



'''Build and traverse a DFA'''
dfa = dfa_from_string(string_target)
# print("\n", "DFA: ",dfa, "\n")
print("Traversing DFA")
latest_state = run_dfa(dfa, file_string)
print("Output Assertion")
assert0(latest_state == accept_state)
print("Running Poseidon Hash")
run_poseidon_hash(file_string)
print("\n", "Latest State: ",val_of(latest_state), "\n")

if operation =="debug":
    if val_of(latest_state)==accept_state:
        print("DFA successfully reached the accept state \n")
    else:
        print("DFA did not reached the accept state \n")

print("Generating Output \n")
print_ir0(target_dir + "/" + f"{file_name}_{prime_name}_{size}")