import sys
import unittest
from unittest.mock import patch
from miniwizpl import *
from miniwizpl.expr import *

sys.path.append("/usr/src/app/examples/substring_search/IR0")
import after_all_multi as statement

sys.path.append("/usr/src/app/examples/substring_search/common")
import util

class TestStatement(unittest.TestCase):
    
    def test_base(self):

        '''
            A base case to pass, target strings being at the end of the corpus 
            No trickiness involved
        '''

        string_a = ['fourteen']
        string_target =  ['fifteen']
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_states = [i for i in range(0,len(string_a))]
        found_states=[i for i in range(zero_states[-1]+1,zero_states[-1]+len(string_target)+1)]
        accept_state = found_states[-1]*10
        error_state = found_states[-1]*100

        Secret_str_after_all = SecretStack([])
        
        # Testing final state
        dfa = statement.dfa_from_string(string_a, string_target, zero_states, found_states, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_states, found_states, accept_state, error_state, Secret_str_after_all)
        self.assertEqual(val_of(latest_state), accept_state)
        self.assertFalse(val_of(latest_state) in found_states)
        self.assertNotEqual(val_of(latest_state), zero_states)
        self.assertNotEqual(val_of(latest_state), error_state)

        # Testing SecretStack
        file_name="after_all_multi"
        expected = util.create_exepected_result(file_name, corpus, string_target, string_a)
        test_flag = util.reconcile_secretstack(expected, Secret_str_after_all)
        self.assertTrue(test_flag)


    def test_intermediate(self):

        '''
            An intermediate case to pass, string_a and target strings being multiple strings
        '''

        string_a = ['twelve','thirteen']
        string_target =  ['fourteen', 'fifteen']
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_states = [i for i in range(0,len(string_a))]
        found_states=[i for i in range(zero_states[-1]+1,zero_states[-1]+len(string_target)+1)]
        accept_state = found_states[-1]*10
        error_state = found_states[-1]*100

        Secret_str_after_all = SecretStack([])

        # Testing final state
        dfa = statement.dfa_from_string(string_a, string_target, zero_states, found_states, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_states, found_states, accept_state, error_state, Secret_str_after_all)
        self.assertEqual(val_of(latest_state), accept_state)
        self.assertFalse(val_of(latest_state) in found_states)
        self.assertNotEqual(val_of(latest_state), zero_states)
        self.assertNotEqual(val_of(latest_state), error_state)

        # Testing SecretStack
        file_name="after_all_multi"
        expected = util.create_exepected_result(file_name, corpus, string_target, string_a)
        test_flag = util.reconcile_secretstack(expected, Secret_str_after_all)
        self.assertTrue(test_flag)


    def test_fail(self):

        '''
            A base case to fail, target strings being at the end of the corpus 
            'fourteen' comes immediately after 'twelve' in string_target, skipping 'thirteen'
        '''

        string_a = ['twelve']
        string_target =  ['fourteen', 'fifteen']
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_states = [i for i in range(0,len(string_a))]
        found_states=[i for i in range(zero_states[-1]+1,zero_states[-1]+len(string_target)+1)]
        accept_state = found_states[-1]*10
        error_state = found_states[-1]*100

        
        Secret_str_after_all = SecretStack([])
        
        # Testing final state
        dfa = statement.dfa_from_string(string_a, string_target, zero_states, found_states, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_states, found_states, accept_state, error_state, Secret_str_after_all)
        self.assertNotEqual(val_of(latest_state), accept_state)
        self.assertNotEqual(val_of(latest_state), zero_states)
        self.assertFalse(val_of(latest_state) in found_states)
        self.assertEqual(val_of(latest_state), error_state)

        # Testing SecretStack & Converting strings, target, and corpus into integers, and creating expected list to reconcile the result
        file_name="after_all_multi"
        expected = util.create_exepected_result(file_name, corpus, string_target, string_a)
        test_flag = util.reconcile_secretstack(expected, Secret_str_after_all)
        self.assertFalse(test_flag)


if __name__ == '__main__':
    unittest.main()

