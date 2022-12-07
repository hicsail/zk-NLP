import sys
from miniwizpl import *
from miniwizpl.expr import *
from common.util import *

''' Checking if prime meets our requirement'''
txt_dir='./ccc.txt' #Relative to where generate_statements(_ta1)
target='@field (equals (2305843009213693951))'
assert check_prime(txt_dir, target)== True

assert len(sys.argv) == 5, "Invalid arguments"
_, target_dir, prime, prime_name, size = sys.argv
set_field(int(prime))

''' Prepping target text and substrings'''
file_data=generate_text(int(size))
string_target=generate_target(file_data, "begins")

print("Text: ", file_data, "\n")
print("Target: ", string_target, "\n")
# Transform the text file to search into miniwizpl format
file_string = SecretList([word_to_integer(_str) for _str in file_data])

zero_state = 0
accept_state=100
error_state=101

def dfa_from_string(target):
    next_state = {}
    next_state[(zero_state, word_to_integer(target))]=accept_state
    return next_state

# run a dfa
def run_dfa(dfa, text_input):
    def next_state_fun(string, initial_state):
        curr_state=initial_state

        for (dfa_state, dfa_str), next_state in dfa.items():
            curr_state = mux((initial_state == dfa_state) & (string == dfa_str),
                         next_state,
                         mux((initial_state == dfa_state) & (string != dfa_str),
                         error_state,
                         curr_state))

        return curr_state
    latest_state=reduce(next_state_fun, text_input, zero_state)
    return latest_state

dfa = dfa_from_string(string_target)
print("\n", "DFA: ",dfa, "\n")

# define the ZK statement
latest_state = run_dfa(dfa, file_string)
assert0(latest_state - accept_state)

# compile the ZK statement to an EMP file
print_ir0(target_dir + "/" + f"begins_{prime_name}_{size}")

