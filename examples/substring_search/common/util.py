import random
from faker import Faker
from miniwizpl import *
from miniwizpl.expr import *
import re
import hashlib

def word_to_integer(word):
    hash = hashlib.sha256(word.encode('utf-8')).digest()
    hash = int.from_bytes(hash, 'big')
    hash = hash >> 8*28+1
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
    # print(res, '\n')
    return eval(res,{'curr_state':curr_state, 'mux':mux, 'val_of':val_of})

def is_in_found_states(initial_state, found_states):
    res="("
    for val in found_states:
        res += "(initial_state=="
        res += f"{val}"
        res += ")|"
    res=res[0:-1]
    res += ")"
    # print(res, '\n')

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

def generate_text(scale=0):
    print("\n")
    fake = Faker(['en_US'])
    file_data=fake.text()
    for s in range(scale):
        file_data+=file_data
    print("Before cleaning text: ", file_data, "\n")
    regex = re.compile('[,\.!?]')
    file_data=regex.sub('', file_data)
    print("Removing [,\.!?]: ", file_data, "\n")
    return file_data.split()

def generate_target(txt, type):
    if type=="after_all":
        string_a=random.sample(txt[:-1], 1) # Avoiding the last substring to be picked as target
        string_a=string_a[0]
        idx_a=txt.index(string_a)
        string_target=txt[idx_a+1:]
        return string_a, string_target

    elif type=="after":
        string_a=random.sample(txt[:-1], 1) # Avoiding the last substring to be picked as target
        string_a=string_a[0]
        idx_a=txt.index(string_a)
        string_target=txt[idx_a+1]
        return string_a, string_target      

    elif type=="begins":
        return txt[0]
    
    elif type=="between":
        string_a=random.sample(txt[:-1], 1) # Avoiding the last substring to be picked as target
        string_a=string_a[0]
        idx_a=txt.index(string_a)

        string_b=random.sample(txt[idx_a+1:], 1) # Avoiding the last substring to be picked as target
        string_b=string_b[0]
        idx_b=txt.index(string_b)
        string_target=txt[idx_a+1:idx_b]
        return string_a, string_target, string_b

    if type=="point_to":
        string_a=random.sample(txt[1:], 1) # Avoiding the first substring to be picked as target
        string_a=string_a[0]
        idx_a=txt.index(string_a)
        string_target=txt[:idx_a]
        return string_a, string_target
