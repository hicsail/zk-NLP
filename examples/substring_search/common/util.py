import random
from faker import Faker
from miniwizpl import *
from miniwizpl.expr import *
import re
import hashlib
sys.path.append("/usr/src/app/examples/poseidon_hash")
from parameters import *
from hash import Poseidon



def word_to_integer(word_to_convert):

    '''
        This function takes a string input called "word_to_convert" 
        and uses the SHA-256 hash algorithm to generate a unique 256-bit hash 
        from the input string. 

        It then converts this hash to an integer using the "int.from_bytes" method 
        and shifts the bits to the right by 8*28+1, dropping some digits. 
        Then it returns this modified integer as the output.
    
    '''

    hash = hashlib.sha256(word_to_convert.encode('utf-8')).digest()
    hash = int.from_bytes(hash, 'big')
    hash = hash >> 8*28+1
    return hash



def is_in_found_states(initial_state, found_states):

    '''
        This function generates a conditional statement used in cond_push of SecretStack
        Since the size of found_states varies, it requires to concatenate iteratively
    '''

    if len(found_states)==0:
      return False

    else:
      res="("
      for val in found_states:
          res += "(initial_state=="
          res += f"{val}"
          res += ")|"
      res=res[0:-1]
      res += ")"
      # print(res, '\n')

    return eval(res,{'initial_state':initial_state})



def generate_text(scale=0, file_name=None):
    
    '''
        This function takes an optional parameter "scale" to generate fake text of a certain length using the Faker library. 
        It then cleans regular expressions and returns the first 10 words of the cleaned text, 
        with the number of words being 10 multiplied by 2 raised to the power of the scale. 
    '''

    if scale<0:
        raise ValueError("Scale should be non-negative integer")
    
    if not isinstance(scale, int):
        raise TypeError("Scale should be integer")

    print("\n")
    
    fake = Faker(['en_US'])
    file_data=fake.text(1500*(2**scale))
    regex = re.compile('[,\.!?]')
    file_data=regex.sub('', file_data)
    file_data = file_data.split()[:10*(2**scale)]

    if file_name=="string_search": # string_search requires a text input
        file_data=" ".join([str(item) for item in file_data])

    return file_data



def generate_target(txt, type, length=1, n_string=1):

    if isinstance(txt, str):
        txt = txt.split()
    
    
    if type=="after_all":

        if length>len(txt)-1:
            length=len(txt)-1
            print(f'The length of input corpus is {len(txt)}. The length value is set to {length}')
            
        elif length<=0:
            print(f'The length value must be positive integer. The length value is set to 1')
            length=1

        string_a=txt[-length-1]
        string_target=txt[-length:]

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

        if length>len(txt)-1:
            length=len(txt)-1
            print(f'The length of input corpus is {len(txt)}. The length value is set to {length}')

        elif length<=0:
            print(f'The length value must be positive integer. The length value is set to 1')
            length=1

        idx_a=random.randint(-len(txt),-length-1) # Avoiding index out of range
        string_a=txt[idx_a]
        idx_b=idx_a+1+length
        
        '''
            If idx_a + length use up the space of idx_b, then string_b will be set empty
        '''

        if idx_b==0:
            string_b=''
            string_target=txt[idx_a+1:]

        else:
            string_b=txt[idx_b]
            string_target=txt[idx_a+1:idx_b]

        return string_a, string_target, string_b


    elif type=="point_to":

        if length>len(txt):
            length=len(txt)
            print(f'The length of input corpus is {len(txt)}. The length value is set to {length}')

        elif length<=0:
            print(f'The length value must be positive integer. The length value is set to 1')
            length=1

        idx_a=length

        '''
            If idx_a == txt length, then string_a will be set empty
        '''

        if idx_a==len(txt):
            string_a=''
            string_target=txt[:idx_a]
        
        else:
            string_a=txt[idx_a]
            string_target=txt[:idx_a]

        return string_a, string_target
    

    elif type=="string_search":

        string_target=random.sample(txt, 1)
        string_target=string_target[0]

        return string_target


    elif type=="stringlist_search":

        if length>len(txt):
            length=len(txt)
            print(f'The length of input corpus is {len(txt)}. The n_strint value is set to {length}')

        if n_string*length>len(txt):
            n_strint=int(len(txt)/n_string)
            print(f'The length of input corpus is {len(txt)}. The n_strint value is set to {n_strint}')

        if length<0:
            print(f'The length value must be positive integer. The length value is set to 1')
            length=1

        if n_string<0:
            print(f'The n_string value must be positive integer. The n_string value is set to 1')
            n_string=1

        res=[]

        for i in range(0, n_string):
            curr_str =""
            idx_a=random.randint(0, len(txt)-length) # Avoiding index out of range
            curr_lst=txt[idx_a:idx_a+length]
            curr_str=" ".join([str(item) for item in curr_lst])
            res.append(curr_str)
        
        return res



def check_prime():
  txt_dir='./ccc.txt' #Reative to where you run the generate_statements
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



'''
The following functions are no longer used
'''



# def integer_to_word(integer):
#     word=""
#     bit = (1<<8)-1
#     while integer>0:
#         bit_char = integer&bit
#         integer=integer>>8
#         char=chr(bit_char)
#         word+=char
#     return word

# def isLaststring(word, text):
#     lastString=word_to_integer(text[-1])
#     return   lastString== val_of(word)

# def isNotlaststring(word, text):
#     lastString=word_to_integer(text[-1])
#     return   lastString!= val_of(word)


# def flip_interim_found_state(curr_state, found_states):
#     x=len(found_states)
#     res=""
#     for i in range(1,x+1):
#         res += f"mux(curr_state=={-i}, {i},"
#     res += "curr_state"
#     for i in range(1,x+1):
#         res += ")"
#     # print(res, '\n')
#     return eval(res,{'curr_state':curr_state, 'mux':mux, 'val_of':val_of})

# def is_in_found_states_todelete(initial_state, found_states):
#     res="("
#     for val in found_states:
#         res += "(val_of(initial_state)=="
#         res += f"{val}"
#         res += ")|"
#     res=res[0:-1]
#     res += ")"
#     print(res, '\n')

#     return eval(res,{'initial_state':initial_state, 'val_of':val_of})