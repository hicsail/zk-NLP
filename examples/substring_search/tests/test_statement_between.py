import sys
import unittest
from unittest.mock import patch
from miniwizpl import *
from miniwizpl.expr import *

sys.path.append("/usr/src/app/examples/substring_search/IR0")
import between as statement

sys.path.append("/usr/src/app/examples/substring_search/common")
import util

class TestStatement(unittest.TestCase):
    
    def test_base(self):

        '''
            A base case to pass, target strings being at the beginning of the corpus 
            No trickiness involved
        '''

        string_a = 'one'
        string_target =  ['two']
        string_b = 'three'
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_state = 0
        found_states=[i for i in range(1,len(string_target)+1)]
        
        appendedAll_state=found_states[-1]*10
        accept_state = found_states[-1]*100
        error_state = found_states[-1]*100+1

        Secret_str_between = SecretStack([])

        dfa = statement.dfa_from_string(string_a, string_target, string_b, zero_state, found_states, appendedAll_state, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_state, found_states, appendedAll_state, accept_state, error_state, Secret_str_between)
        self.assertEqual(val_of(latest_state), accept_state)

        # Converting strings, target, and corpus into integers, and creating expected list to reconcile the result

        expected=util.create_exepected_result('between', corpus, string_target, string_a, string_b)
        self.assertEqual(val_of(Secret_str_between), expected)


    def test_intermediate(self):

        '''
            An intermediate case to pass, target strings being at the end of the corpus 
        '''
        
        string_a = 'thirteen'
        string_target =  ['fourteen']
        string_b = 'fifteen'
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_state = 0
        found_states=[i for i in range(1,len(string_target)+1)]
        
        appendedAll_state=found_states[-1]*10
        accept_state = found_states[-1]*100
        error_state = found_states[-1]*100+1

        Secret_str_between = SecretStack([])

        dfa = statement.dfa_from_string(string_a, string_target, string_b, zero_state, found_states, appendedAll_state, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_state, found_states, appendedAll_state, accept_state, error_state, Secret_str_between)
        self.assertEqual(val_of(latest_state), accept_state)

        # Converting strings, target, and corpus into integers, and creating expected list to reconcile the result

        expected=util.create_exepected_result('between', corpus, string_target, string_a, string_b)
        self.assertEqual(val_of(Secret_str_between), expected)


    def test_advanced(self):
        
        '''
            An advanced case to pass, target strings at the end of the corpus and string_b does not exist
        '''

        string_a = 'fourteen'
        string_target =  ['fifteen']
        string_b = ''
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_state = 0
        found_states=[i for i in range(1,len(string_target)+1)]
        
        appendedAll_state=found_states[-1]*10
        accept_state = found_states[-1]*100
        error_state = found_states[-1]*100+1

        Secret_str_between = SecretStack([])

        dfa = statement.dfa_from_string(string_a, string_target, string_b, zero_state, found_states, appendedAll_state, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_state, found_states, appendedAll_state, accept_state, error_state, Secret_str_between)
        self.assertEqual(val_of(latest_state), appendedAll_state)
        
        # Converting strings, target, and corpus into integers, and creating expected list to reconcile the result

        expected=util.create_exepected_result('between', corpus, string_target, string_a, string_b)
        self.assertEqual(val_of(Secret_str_between), expected)


    def test_fail(self):

        '''
            A base case to fail, target strings being at the beginning of the corpus 
            'three' comes immediately after 'one' in string_target, skipping 'two'
        '''

        string_a = 'one'
        string_target =  ['three']
        string_b = 'four'
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_state = 0
        found_states=[i for i in range(1,len(string_target)+1)]
        
        appendedAll_state=found_states[-1]*10
        accept_state = found_states[-1]*100
        error_state = found_states[-1]*100+1

        Secret_str_between = SecretStack([])

        dfa = statement.dfa_from_string(string_a, string_target, string_b, zero_state, found_states, appendedAll_state, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_state, found_states, appendedAll_state, accept_state, error_state, Secret_str_between)
        self.assertNotEqual(val_of(latest_state), accept_state)
        self.assertNotEqual(val_of(latest_state), appendedAll_state)
        
        # Converting strings, target, and corpus into integers, and creating expected list to reconcile the result
        
        expected=util.create_exepected_result('between', corpus, string_target, string_a, string_b)
        self.assertNotEqual(val_of(Secret_str_between), expected)


if __name__ == '__main__':
    unittest.main()

