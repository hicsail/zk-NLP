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



def is_in_target_states(initial_state, target_states):

    '''
        This function generates a conditional statement used in cond_push of SecretStack
        Since the size of target_states varies, it requires to concatenate iteratively
    '''

    if len(target_states)==0:
      return False

    else:
      res="("
      for val in target_states:
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



def generate_target(txt, file_name, substring_len=1, piv_len=1):

    '''
        This method takes an optional parameter "substring_len" and "piv_len" to pick target texts and pivot words for respective statement type. 
        
        substring_len represents the size of a target substring for such algorithms as between, after all, point to.
        When the substring_len is 2 in the between algorithm for the corpus size of 4, this function will pick string_a either at index 0 or 1, so it can accomodate substring substring_len of 2 after it.
        Its value shall be positive integer and shall not exceed the size of the corpus text, and there is correction method in case value exceeding the boundary is chosen.

        piv_len represents different things depending on statements.
        For stringlist_search algorithm, it represents the number of strings to look for
        For others, it represents the size of pivot word(s)
        Its value shall be positive integer, and there is correction method in case negative value is chosen.

        substring_len gets priority when the combined sum of the length of substring_len and pivot_len exceeds the input text size
    '''

    if isinstance(txt, str):
        txt = txt.split()
    
    
    if file_name=="after_all":

        if substring_len>len(txt)-1:
            substring_len=len(txt)-1 # Leaving minimum one string space for the pivot word
            print(f'The length of input corpus is {len(txt)}. The substring_len value is set to {substring_len}')
            
        elif substring_len<=0:
            print(f'The substring_len value must be positive integer. The substring_len value is set to 1')
            substring_len=1

        string_a=txt[-substring_len-1]
        string_target=txt[-substring_len:]

        return string_a, string_target


    if file_name=="after_all_multi":

        '''
            substring_len represents the length of the target string after string_a
            piv_len represents the length of string_a
        '''

        if substring_len>len(txt)-1:
            substring_len=len(txt)-1 # Leaving minimum one string space for the pivot word
            print(f'The length of input corpus is {len(txt)}. The substring_len value is set to {substring_len}')
            
        elif substring_len<=0:
            print(f'The length value must be positive integer. The substring_len value is set to 1')
            substring_len=1

        if piv_len<=0:
            print(f'The piv_len value must be positive integer. The piv_len value is set to 1')
            piv_len=1

        if piv_len+substring_len>len(txt):
            piv_len=len(txt)-substring_len
            print(f'The length of input corpus is {len(txt)}. The piv_len value is set to {piv_len}')

        # This method returns a list of string_a
        string_a=txt[-substring_len-piv_len: -substring_len]
        string_target=txt[-substring_len:]

        return string_a, string_target
        
        
    elif file_name=="after":

        string_a=random.sample(txt[:-1], 1) # Leaving minimum one string space for the pivot word at the end
        string_a=string_a[0]
        idx_a=txt.index(string_a)
        string_target=txt[idx_a+1]

        return string_a, string_target

    elif file_name=="after_multi":

        '''
            substring_len represents the length of the target string after string_a
            piv_len represents the length of string_a
        '''

        if substring_len>len(txt)-1:
            substring_len=len(txt)-1 # Leaving minimum one string space for the pivot word
            print(f'The length of input corpus is {len(txt)}. The substring_len value is set to {substring_len}')
            
        elif substring_len<=0:
            print(f'The length value must be positive integer. The substring_len value is set to 1')
            substring_len=1

        if piv_len<=0:
            print(f'The piv_len value must be positive integer. The piv_len value is set to 1')
            piv_len=1

        if piv_len+substring_len>len(txt):
            piv_len=len(txt)-substring_len
            print(f'The length of input corpus is {len(txt)}. The piv_len value is set to {piv_len}')


        # This method returns a list of string_a and string_target
        if len(txt)-piv_len-substring_len==0:
            idx_a=0
        else:
            idx_a=random.randint(0, len(txt)-piv_len-substring_len)

        string_a=txt[idx_a:idx_a+piv_len]
        string_target=txt[idx_a+piv_len:idx_a+piv_len+substring_len]

        return string_a, string_target


    elif file_name=="begins":

        return txt[0]


    elif file_name=="begins_multi":
        '''
            piv_len represents the length of substrings to look at in the beginning of the corpus
        '''

        return txt[:piv_len]


    elif file_name=="between":
        assert(len(txt)>2) #If less than 3, it cannot form between statement

        if substring_len>len(txt)-2:
            substring_len=len(txt)-2
            print(f'The length of input corpus is {len(txt)}. The substring_len value is set to {substring_len}')

        elif substring_len<=0:
            print(f'The length value must be positive integer. The substring_len value is set to 1')
            substring_len=1

        idx_a=random.randint(-len(txt),-substring_len-2) # Leaving minimum two strings-space for the pivot word and closing word
        string_a=txt[idx_a]
        idx_b=idx_a+1+substring_len

        string_b=txt[idx_b]
        string_target=txt[idx_a+1:idx_b]

        return string_a, string_target, string_b


    elif file_name=="between_multi":

        '''
            substring_len represents the length of the target string between string_a and string_b
            piv_len represents the length of string_a and string_b
        '''
        assert(len(txt)>2) #If less than 3, it cannot form between statement

        if substring_len*2>len(txt)-1:
            substring_len=len(txt)-2 # Leaving minimum two strings-space for the pivot word and closing word
            print(f'The length of input corpus is {len(txt)}. The substring_len value is set to {substring_len}')
            
        elif substring_len<=0:
            print(f'The length value must be positive integer. The substring_len value is set to 1')
            substring_len=1

        if piv_len<=0:
            print(f'The piv_len value must be positive integer. The piv_len value is set to 1')
            piv_len=1

        if piv_len+substring_len*2>len(txt):
            piv_len=int((len(txt)-substring_len)/2)
            print(f'The length of input corpus is {len(txt)}. The piv_len value is set to {piv_len}')


        idx_a=random.randint(0,len(txt)-substring_len-piv_len*2) # Leaving a space for string_b
        string_a=txt[idx_a:idx_a+piv_len]
        idx_b=idx_a+piv_len+substring_len
        string_b=txt[idx_b:idx_b+piv_len]
        string_target=txt[idx_a+piv_len:idx_b]

        return string_a, string_target, string_b


    elif file_name=="point_to":

        '''
            substring_len represents the length of the target string before string_a
        '''

        if substring_len>len(txt)-1:
            substring_len=len(txt)-1 # Leaving minimum one string space for the pivot word
            print(f'The length of input corpus is {len(txt)}. The substring_len value is set to {substring_len}')

        elif substring_len<=0:
            print(f'The length value must be positive integer. The substring_len value is set to 1')
            substring_len=1

        idx_a=substring_len

        string_a=txt[idx_a]
        string_target=txt[:idx_a]

        return string_a, string_target
    

    elif file_name=="point_to_multi":

        '''
            substring_len represents the length of the target string before string_a
            piv_len represents the length of string_a
        '''

        if substring_len>len(txt)-1:
            substring_len=len(txt)-1 # Leaving minimum one string space for the pivot word
            print(f'The length of input corpus is {len(txt)}. The substring_len value is set to {substring_len}')
            
        elif substring_len<=0:
            print(f'The substring_len value must be positive integer. The substring_len value is set to 1')
            substring_len=1

        if piv_len<=0:
            print(f'The piv_len value must be positive integer. The piv_len value is set to 1')
            piv_len=1

        if piv_len+substring_len>len(txt):
            piv_len=len(txt)-substring_len
            print(f'The length of input corpus is {len(txt)}. The piv_len value is set to {piv_len}')


        idx_a=substring_len

        string_a=txt[idx_a:idx_a+piv_len]
        string_target=txt[:idx_a]

        return string_a, string_target


    elif file_name=="string_search":

        string_target=random.sample(txt, 1)
        string_target=string_target[0]

        return string_target


    elif file_name=="stringlist_search":

        '''
            substring_len represents the number of substrings to look for, named string_a
        '''

        if substring_len>len(txt):
            substring_len=len(txt)
            print(f'The length of input corpus is {len(txt)}. The substring_len value is set to {substring_len}')

        if piv_len*substring_len>len(txt):
            piv_len=int(len(txt)/piv_len)
            print(f'The length of input corpus is {len(txt)}. The piv_len value is set to {piv_len}')

        if substring_len<0:
            print(f'The length value must be positive integer. The substring_len value is set to 1')
            substring_len=1

        if piv_len<0:
            print(f'The piv_len value must be positive integer. The piv_len value is set to 1')
            piv_len=1

        string_a=[]

        for i in range(0, piv_len):
            curr_str =""
            idx_a=random.randint(0, len(txt)-substring_len) # Avoiding index out of range
            curr_lst=txt[idx_a:idx_a+substring_len]
            curr_str=" ".join([str(item) for item in curr_lst])
            string_a.append(curr_str)
        
        return string_a



def check_prime():
  '''
    Checking function to validate ccc file is configured properly
  '''
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


def create_exepected_result(file_name, corpus, string_target, string_a, string_b=None):

    '''
        between and point_to require a unique preparation to create an expected list of strings.
        The list is compared with the content in a Secret Stack in the reconcile_secretstack function.
    '''
    if not isinstance(corpus, list):
        corpus = corpus.split()

    expected=[word_to_integer(x) for x in string_target] 
    corpus_int=[word_to_integer(_str) for _str in corpus]
    

    if file_name=='after_all' or file_name=='after_all_multi':

        pass # after_all statement returns this original expected list
    

    elif file_name=='between':
        
        int_a = word_to_integer(string_a)
        expected.insert(0, int_a)


    elif file_name=='between_multi':
        int_a_lst = [word_to_integer(x) for x in string_a] 
        expected=int_a_lst+expected


    elif file_name=='point_to':

        int_a = word_to_integer(string_a)


    elif file_name=='point_to_multi':

        int_a_lst = [word_to_integer(x) for x in string_a]
        expected=expected+int_a_lst

    return expected


def reconcile_secretstack(expected, secretstack):

    '''
        between and point_to require a unique preparation to create an expected list of strings.
        The list is compared with the content in a Secret Stack in the reconcile_secretstack function.
    '''

    test_flag = True # Used only for testing

    for idx in range(0,len(expected)):
        
        curr_str=secretstack.cond_pop(len(secretstack.val) > 0)
        expected_val = expected[-idx-1]
        assert0(expected_val - curr_str)

        # The following control flow is just for the sake of testing
        if expected_val - val_of(curr_str)!=0:
            test_flag=False
        
    return test_flag
