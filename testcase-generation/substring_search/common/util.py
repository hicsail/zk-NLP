import random
from faker import Faker
from miniwizpl import *
from miniwizpl.expr import *
import re
import hashlib
sys.path.append("/usr/src/app/examples/poseidon_hash")
from parameters import *
from hash import Poseidon

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
    file_data=fake.text(1500*(2**scale))
    # print("Before cleaning text: ", file_data, "\n")
    regex = re.compile('[,\.!?]')
    file_data=regex.sub('', file_data)
    # print("Removing [,\.!?]: ", file_data, "\n")
    #final_data = file_data.split()[:1000000*(2**scale)]
    final_data = file_data.split()[:10*(2**scale)]
    # print("Removing [,\.!?]: ", file_data, "\n")
    return final_data

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
        string_a=random.sample(txt[:-2], 1) # Avoiding the last substring to be picked as target
        string_a=string_a[0]
        idx_a=txt.index(string_a)
        string_b=random.sample(txt[idx_a+2:], 1)
        string_b=string_b[0]
        idx_b=txt[idx_a+2:].index(string_b)+idx_a+2
        string_target=txt[idx_a+1:idx_b]
        return string_a, string_target, string_b

    elif type=="point_to":
        string_a=random.sample(txt[1:], 1) # Avoiding the first substring to be picked as target
        string_a=string_a[0]
        idx_a=txt.index(string_a)
        string_target=txt[:idx_a]
        return string_a, string_target
    
    elif type=="string_search":
        string_target=random.sample(txt, 1)
        string_target=string_target[0]
        return string_target

    elif type=="stringlist":
        string_a=random.sample(txt[:-1],1)  # Avoiding the last substring to be picked as a first target
        string_a=string_a[0]
        idx_a=txt.index(string_a)
        idx_b=idx_a+1
        string_b= txt[idx_b]
        return [string_a + ' '+string_b]

def check_prime():
  txt_dir='./testcase-generation/ccc.txt' #Reative to where you run the generate_statements
  target='@field (equals (2305843009213693951))'
  with open(txt_dir) as f:
      txt = f.read().splitlines() 
  for t in txt:
    print(t) # TODO FIXME: Delete this line later
    if t.find(target)!=-1:
      return True
  return False

def run_poseidon_hash(file_string):
    # prove validity of the input text by Poseidon Hash
    security_level = 128
    input_rate = 3
    t = input_rate # these should be the same
    alpha = 17     # depends on the field size (unfortunately)
    prime = 2**61-1
    set_field(prime)
    poseidon_new = Poseidon(prime, security_level, alpha, input_rate, t)

    print('converting to gfs')
    split_gfs = file_string.as_field_elements(input_rate)
    print('need to do this many hashes:', len(split_gfs))

    for g in split_gfs:
        poseidon_digest = poseidon_new.run_hash(g)
        #print('digest:', val_of(poseidon_digest))
    assert0(poseidon_digest - val_of(poseidon_digest))
