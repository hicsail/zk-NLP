import sys
from miniwizpl import *
from miniwizpl.expr import *
from common.util import *

''' Checking if prime meets our requirement'''
txt_dir='./ccc.txt' #Relative to where generate_statements(_ta1)
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
string_target=generate_target(file_data, "stringlist")

print("Text: ", file_data, "\n")
print("Target: ", string_target, "\n")
# Transform the text file to search into miniwizpl format
file_string = SecretList([word_to_integer(_str) for _str in file_data])

accept_state = 255


def islast(i, word):
    if len(word.split()) - 1 == i:
        return True
    else:
        return False


def equals(pointer, state):
    for i in range(len(pointer)):
        if pointer[i] != state[i]:
            return False
    return True


def dfa_from_string(stringlist):
    length = len(stringlist)
    pointer = [0] * length
    next_state = {}
    wordlist = set(' '.join(stringlist).split())

    states = [pointer]  # keep track of all states
    count = 0
    finished = False  # not all accepted

    while not finished:
        state = states[count]
        counter = len(states)
        for word in wordlist:
            pointer = state.copy()
            for i in range(length):  # 0,1,2
                if state[i] != accept_state:
                    if word == stringlist[i].split()[state[i]]:
                        if islast(state[i], stringlist[i]):
                            pointer[i] = accept_state
                        else:
                            pointer[i] += 1
                    else:
                        pointer[i] = 0
            if not equals(pointer, state):
                states.append(pointer)
                next_state[tuple(state), word_to_integer(word)] = tuple(pointer)
        if counter < len(states):
            count += 1
        else:
            finished = True
    return next_state



dfa = dfa_from_string(string_target)


# The helper function for comparing two state values
def stateCal(s):
    result = 0
    for i in range(len(s)):
        result += (s[i] << 8 * i)
    return result


# TODO: a reverse version of stateCal() to transform a number back to a state tuple.

accept = tuple([255] * len(string_target))
accept = stateCal(accept)
zero_state = tuple([0] * len(string_target))
zero_state = stateCal(zero_state)


# TODO: actual_counter = [0,0,0,...]
# TODO: expected_counter = [1,2,3,...]

def run_dfa(dfa, string):
    def next_state_fun(word, state):
        output = zero_state

        for (dfa_state, dfa_word), next_state in dfa.items():
            # transform all tuples to numbers
            dfa_state = stateCal(dfa_state)
            next_state = stateCal(next_state)
            output = mux((state == dfa_state) & (word == dfa_word),
                         next_state,
                         output)  # output here is a number, not a tuple
            # TODO: check if output has any accept state for a single string: need to use the reverse version of
            #  stateCal()
            # TODO: if any accept state, actual_counter[index]++ and change the state back to 0
        output = mux(state == accept, accept, output)  # TODO: this line might need to be changed for the counter.

        return output

    return reduce(next_state_fun,string,zero_state)


'''
def public_foreach(ls, fn, init):
    accumulator = init
    for x in ls:
        accumulator = fn(x, accumulator)
    return accumulator
'''

# define the ZK statement
outputs = run_dfa(dfa, file_string)
# TODO: instead of comparing the run_dfa result, we will need to compare the actual_counter with the expected_counter.
print('output', outputs)
assert0(outputs - accept)

# compile the ZK statement
print_ir0(target_dir + "/" + f"stringlist_{prime_name}_{size}")