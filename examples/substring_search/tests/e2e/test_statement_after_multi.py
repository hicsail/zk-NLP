import sys
import unittest
from unittest.mock import patch
from miniwizpl import *
from miniwizpl.expr import *

sys.path.append("/usr/src/app/examples/substring_search/IR0")
import after_multi as statement

sys.path.append("/usr/src/app/examples/substring_search/common")
import util

class TestStatement(unittest.TestCase):
    
    def test_base(self):

        '''
            A base case to pass, target strings being at the beginning of the corpus - No trickiness involved
        '''

        string_a = ['two','three']
        string_target =  ['four', 'five']
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_states = [i for i in range(0,len(string_a))]
        found_states=[i for i in range(zero_states[-1]+1,zero_states[-1]+len(string_target)+1)]
        accept_state = found_states[-1]*10
        error_state = found_states[-1]*100
        
        dfa = statement.dfa_from_string(string_a, string_target, zero_states, found_states, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_states, accept_state, error_state)
        self.assertEqual(val_of(latest_state), accept_state)
        self.assertTrue(val_of(latest_state) not in zero_states)
        self.assertNotEqual(val_of(latest_state), error_state)


    def test_fail(self):

        '''
            A base case to fail, target strings being at the beginning of the corpus 
            'four' and 'five' comes immediately after 'one two' in string_target, skipping 'two'
        '''

        string_a = ['one','two']
        string_target =  ['four', 'five']
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_states = [i for i in range(0,len(string_a))]
        found_states=[i for i in range(zero_states[-1]+1,zero_states[-1]+len(string_target)+1)]
        accept_state = found_states[-1]*10
        error_state = found_states[-1]*100

        dfa = statement.dfa_from_string(string_a, string_target, zero_states, found_states, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_states, accept_state, error_state)
        self.assertEqual(val_of(latest_state), error_state)
        self.assertTrue(val_of(latest_state) not in zero_states)
        self.assertNotEqual(val_of(latest_state), accept_state)


    def test_fail_intermediate(self):

        '''
            An intermediate case to fail, string_a does not exist in the corpus 
        '''

        string_a = ['hundred','thousand']
        string_target =  ['four', 'five']
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_states = [i for i in range(0,len(string_a))]
        found_states=[i for i in range(zero_states[-1]+1,zero_states[-1]+len(string_target)+1)]
        accept_state = found_states[-1]*10
        error_state = found_states[-1]*100

        dfa = statement.dfa_from_string(string_a, string_target, zero_states, found_states, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_states, accept_state, error_state)
        self.assertEqual(val_of(latest_state), 0)
        self.assertNotEqual(val_of(latest_state), error_state)
        self.assertNotEqual(val_of(latest_state), accept_state)


if __name__ == '__main__':
    unittest.main()

