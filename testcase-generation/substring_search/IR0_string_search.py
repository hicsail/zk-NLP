import sys
from miniwizpl import *
from miniwizpl.expr import *
from common.util import *

''' Checking if prime meets our requirement'''
txt_dir='./testcase-generation/ccc.txt' #Reative to where you run the generate_statements
target='@field (equals (2305843009213693951))'
try:
    assert check_prime(txt_dir, target)== True
except:
    print("no equivalent prime (2305843009213693951) in ccc.txt")
    sys.exit(1)

assert len(sys.argv) == 5, "Invalid arguments"
_, target_dir, prime, prime_name, size = sys.argv
set_field(int(prime))

''' Prepping target text and substrings'''
file_data=generate_text(int(size))
string_target =generate_target(file_data, "string_search")

print("Text: ", file_data, "\n")
print("Target: ", string_target)
# Transform the text file to search into miniwizpl format
file_string = SecretList([word_to_integer(_str) for _str in file_data])

# the accept state is 1000000
accept_state = 1000000

# a Python function to create a dfa from a string
# we assume a default transition back to 0
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

# run a dfa
def run_dfa(dfa, string):
    def next_state_fun(char, state):
        output = 0

        for (dfa_state, dfa_char), next_state in dfa.items():
            output = mux((state == dfa_state) & (char == dfa_char),
                         next_state,
                         output)

        output = mux(state == accept_state, accept_state, output)
        return output

    return reduce(next_state_fun,
                  string,
                  0)

# define the ZK statement
dfa = dfa_from_string(string_target)
print(dfa)
output = run_dfa(dfa, file_string)

assert0((output == accept_state))
print(output)

# compile the ZK statement
print_ir0(target_dir + "/" + f"string_{prime_name}_{size}")
