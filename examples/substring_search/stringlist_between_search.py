import sys
import functools
from miniwizpl import SecretStack, SecretList, mux, public_foreach, public_foreach_v2, print_emp
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


def islast(i, word):
    if len(word.split()) - 1 == i:
        return True
    else:
        return False

zero_state = 0
append_state=1
accept_state=255


def dfa_from_string(first, last):
    next_state = {}
    next_state[(zero_state, word_to_integer(first))]=append_state
    next_state[(append_state, word_to_integer(last))]=accept_state
    return next_state

# run a dfa
def run_dfa(dfa, text_input):
    str_between = []
    def next_state_fun(string, curr_state):
        for (dfa_state, dfa_str), next_state in dfa.items():

            print(
                "curr state: ", curr_state,
                "dfa state: ", dfa_state,"\n",
                "input string: ", string, 
                "dfa string: ", dfa_str,"\n")

            curr_state = val_of(mux((curr_state == dfa_state) & (string == dfa_str),
                         next_state,
                         curr_state))

        if ((curr_state == append_state)): 
            print("Appended", integer_to_word(string), "\n")
            str_between.append(integer_to_word(string))
        return curr_state

    # public_foreach basically runs the above function but returns in an emp format
    loop=public_foreach(text_input, next_state_fun, zero_state)

    if val_of(loop)==append_state:
        str_between.pop()
    return loop, str_between

with open(sys.argv[1], 'r') as f:
    file_data = f.read()

# Transform the text file to search into miniwizpl format
file_data = file_data.split()
file_string = SecretList([word_to_integer(_str) for _str in file_data])

string_a = 'import'
string_b = 'what'

dfa = dfa_from_string(string_a, string_b)
print("\n", "DFA: ",dfa, "\n")

# define the ZK statement
loop, str_between = run_dfa(dfa, file_string)
print("\n", "Result: ",str_between, "\n")
outputs = (loop == accept_state)
print(outputs)
# compile the ZK statement to an EMP file
print_emp(outputs, 'miniwizpl_test.cpp')

