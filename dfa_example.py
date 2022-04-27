import pprint
import random
from miniwizpl import SecretInt, SecretList, mux, public_foreach, print_emp

def next_state(char, state):
    return mux((state == 0) & (char == 87), 1,
    mux((state == 1) & (char == 65), 2,
    mux((state == 1) & (char == 87), 1,
    mux((state == 2) & (char == 78), 3,
    mux((state == 2) & (char == 87), 1,
    mux((state == 3) & (char == 65), 4,
    mux((state == 3) & (char == 87), 1,
    mux((state == 4) & (char == 67), 5,
    mux((state == 4) & (char == 87), 1,
    mux((state == 5) & (char == 82), 6,
    mux((state == 5) & (char == 87), 1,
    mux((state == 6) & (char == 87), 1,
    mux((state == 6) & (char == 89), 7,
    mux((state == 7) & (char == 33), 1000000,
    mux((state == 7) & (char == 87), 1,
        0)))))))))))))))

kb_size = 1000
randlist = [random.randint(1, 100) for _ in range(1000*kb_size)]

#string = SecretList([87, 65])
string = SecretList(randlist)

def dfa_loop(string):
    return public_foreach(string,
                          next_state,
                          0)

output = dfa_loop(string)
#pprint.pprint(output)

print_emp(output, 'miniwizpl_test.cpp')
