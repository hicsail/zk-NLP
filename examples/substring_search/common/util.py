import random
from faker import Faker
from miniwizpl import *
from miniwizpl.expr import *

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

def isLaststring(word, text):
    lastString=word_to_integer(text[-1])
    return   lastString== val_of(word)

def isNotlaststring(word, text):
    lastString=word_to_integer(text[-1])
    return   lastString!= val_of(word)

def flip_interim_found_state(curr_state, found_states):
    x=len(found_states)
    res=""
    for i in range(1,x+1):
        res += f"mux(curr_state=={-i}, {i},"
    res += "curr_state"
    for i in range(1,x+1):
        res += ")"
    print(res, '\n')
    return eval(res,{'curr_state':curr_state, 'mux':mux, 'val_of':val_of})

def is_in_found_states(initial_state, found_states):
    res="("
    for val in found_states:
        res += "(initial_state=="
        res += f"{val}"
        res += ")|"
    res=res[0:-1]
    res += ")"
    print(res, '\n')

    return eval(res,{'initial_state':initial_state})

'''
    We will delete the following module
'''

def is_in_found_states_todelete(initial_state, found_states):
    res="("
    for val in found_states:
        res += "(val_of(initial_state)=="
        res += f"{val}"
        res += ")|"
    res=res[0:-1]
    res += ")"
    print(res, '\n')

    return eval(res,{'initial_state':initial_state, 'val_of':val_of})

def generate_text():
    print("\n")
    fake = Faker(['en_US'])
    file_data=fake.text()
    print(file_data, "\n")
    return file_data.split()

def generate_target(txt, type):
    if type=="after_all":
        string_a=random.sample(txt, 1)
        string_a=string_a[0]
        idx_a=txt.index(string_a)
        string_target=txt[idx_a+1:]
        return string_a, string_target
