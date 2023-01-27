import sys
import unittest
from unittest.mock import patch
from miniwizpl import *
from miniwizpl.expr import *

sys.path.append("/usr/src/app/examples/substring_search/IR0")
import between_multi as statement

sys.path.append("/usr/src/app/examples/substring_search/common")
import util

class TestStatement(unittest.TestCase):
    
    def test_base(self):

        '''
            A base case to pass, target strings being at the beginning of the corpus 
            No trickiness involved
        '''

        string_a = ['one','two']
        string_target =  ['three', 'four']
        string_b = ['five']
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_states = [i for i in range(0,len(string_a))]
        found_states=[i for i in range(zero_states[-1]+1,zero_states[-1]+len(string_target)+1)]
        appendedAll_state=found_states[-1]*10
        closing_states=[i for i in range(appendedAll_state+1, appendedAll_state+len(string_b)+1)]
        accept_state = found_states[-1]*100
        error_state = found_states[-1]*100+1

        Secret_str_between = SecretStack([], max_size=50)

        # Testing final state
        dfa = statement.dfa_from_string(string_a, string_target, string_b, zero_states, found_states, appendedAll_state,closing_states, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_states, found_states, appendedAll_state, closing_states, accept_state, error_state, Secret_str_between)
        self.assertEqual(val_of(latest_state), accept_state)
        self.assertFalse(val_of(latest_state) in found_states)
        self.assertNotEqual(val_of(latest_state), zero_states[0])
        self.assertNotEqual(val_of(latest_state), error_state)
        self.assertFalse(val_of(latest_state) in closing_states)

        # Converting strings, target, and corpus into integers, and creating expected list to reconcile the result
        file_name="between_multi"
        expected=util.create_exepected_result(file_name, corpus, string_target, string_a, string_b)
        test_flag = util.reconcile_secretstack(expected, Secret_str_between)
        self.assertTrue(test_flag)


    def test_intermediate(self):

        '''
            An intermediate case to pass, target strings being at the end of the corpus 
        '''
        
        string_a = ['twelve', 'thirteen']
        string_target =  ['fourteen']
        string_b = ['fifteen']
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_states = [i for i in range(0,len(string_a))]
        found_states=[i for i in range(zero_states[-1]+1,zero_states[-1]+len(string_target)+1)]
        appendedAll_state=found_states[-1]*10
        closing_states=[i for i in range(appendedAll_state+1, appendedAll_state+len(string_b)+1)]
        accept_state = found_states[-1]*100
        error_state = found_states[-1]*100+1

        Secret_str_between = SecretStack([], max_size=50)

        # Testing final state
        dfa = statement.dfa_from_string(string_a, string_target, string_b, zero_states, found_states, appendedAll_state,closing_states, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_states, found_states, appendedAll_state, closing_states, accept_state, error_state, Secret_str_between)
        self.assertEqual(val_of(latest_state), accept_state)
        self.assertFalse(val_of(latest_state) in found_states)
        self.assertNotEqual(val_of(latest_state), zero_states[0])
        self.assertNotEqual(val_of(latest_state), error_state)
        self.assertFalse(val_of(latest_state) in closing_states)

        # Converting strings, target, and corpus into integers, and creating expected list to reconcile the result
        file_name="between_multi"
        expected=util.create_exepected_result(file_name, corpus, string_target, string_a, string_b)
        test_flag = util.reconcile_secretstack(expected, Secret_str_between)
        self.assertTrue(test_flag)


    def test_advanced(self):

        '''
            An advanced case to pass, one of string_a appears twice and the first should be ignored
        '''
        
        string_a = ['twelve', 'thirteen']
        string_target =  ['fourteen']
        string_b = ['fifteen']
        corpus = 'one two twelve four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_states = [i for i in range(0,len(string_a))]
        found_states=[i for i in range(zero_states[-1]+1,zero_states[-1]+len(string_target)+1)]
        appendedAll_state=found_states[-1]*10
        closing_states=[i for i in range(appendedAll_state+1, appendedAll_state+len(string_b)+1)]
        accept_state = found_states[-1]*100
        error_state = found_states[-1]*100+1

        Secret_str_between = SecretStack([], max_size=50)

        # Testing final state
        dfa = statement.dfa_from_string(string_a, string_target, string_b, zero_states, found_states, appendedAll_state,closing_states, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_states, found_states, appendedAll_state, closing_states, accept_state, error_state, Secret_str_between)
        self.assertEqual(val_of(latest_state), accept_state)
        self.assertFalse(val_of(latest_state) in found_states)
        self.assertNotEqual(val_of(latest_state), zero_states[0])
        self.assertNotEqual(val_of(latest_state), error_state)
        self.assertFalse(val_of(latest_state) in closing_states)

        # Converting strings, target, and corpus into integers, and creating expected list to reconcile the result
        file_name="between_multi"
        expected=util.create_exepected_result(file_name, corpus, string_target, string_a, string_b)
        test_flag = util.reconcile_secretstack(expected, Secret_str_between)
        self.assertTrue(test_flag)

    def test_fail(self):

        '''
            A base case to fail, target strings being at the beginning of the corpus 
            'three' comes immediately after 'one' in string_target, skipping 'two'
        '''

        string_a = ['one']
        string_target =  ['three']
        string_b = ['four']
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_states = [i for i in range(0,len(string_a))]
        found_states=[i for i in range(zero_states[-1]+1,zero_states[-1]+len(string_target)+1)]
        appendedAll_state=found_states[-1]*10
        closing_states=[i for i in range(appendedAll_state+1, appendedAll_state+len(string_b)+1)]
        accept_state = found_states[-1]*100
        error_state = found_states[-1]*100+1

        Secret_str_between = SecretStack([], max_size=50)

        # Testing final state
        dfa = statement.dfa_from_string(string_a, string_target, string_b, zero_states, found_states, appendedAll_state,closing_states, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_states, found_states, appendedAll_state, closing_states, accept_state, error_state, Secret_str_between)
        
        self.assertEqual(val_of(latest_state), error_state)
        self.assertNotEqual(val_of(latest_state), accept_state)
        self.assertNotEqual(val_of(latest_state), appendedAll_state)
        self.assertFalse(val_of(latest_state) in found_states)
        self.assertNotEqual(val_of(latest_state), zero_states[0])
        

        # Converting strings, target, and corpus into integers, and creating expected list to reconcile the result
        file_name="between_multi"
        expected=util.create_exepected_result(file_name, corpus, string_target, string_a, string_b)
        test_flag = util.reconcile_secretstack(expected, Secret_str_between)
        self.assertFalse(test_flag)


    def test_fail_intermediate(self):

        '''
            An intermediate case to fail, one of the
            'five' missing in string_b
        '''

        string_a = ['one', 'two']
        string_target =  ['three']
        string_b = ['four', 'six']
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_states = [i for i in range(0,len(string_a))]
        found_states=[i for i in range(zero_states[-1]+1,zero_states[-1]+len(string_target)+1)]
        appendedAll_state=found_states[-1]*10
        closing_states=[i for i in range(appendedAll_state+1, appendedAll_state+len(string_b)+1)]
        accept_state = found_states[-1]*100
        error_state = found_states[-1]*100+1

        Secret_str_between = SecretStack([], max_size=50)

        # Testing final state
        dfa = statement.dfa_from_string(string_a, string_target, string_b, zero_states, found_states, appendedAll_state,closing_states, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_states, found_states, appendedAll_state, closing_states, accept_state, error_state, Secret_str_between)
        
        self.assertEqual(val_of(latest_state), error_state)
        self.assertNotEqual(val_of(latest_state), accept_state)
        self.assertNotEqual(val_of(latest_state), appendedAll_state)
        self.assertFalse(val_of(latest_state) in found_states)
        self.assertNotEqual(val_of(latest_state), zero_states[0])
        self.assertFalse(val_of(latest_state) in closing_states)
        

        # Converting strings, target, and corpus into integers, and creating expected list to reconcile the result
        file_name="between_multi"
        expected=util.create_exepected_result(file_name, corpus, string_target, string_a, string_b)
        test_flag = util.reconcile_secretstack(expected, Secret_str_between)
        self.assertFalse(test_flag)


if __name__ == '__main__':
    unittest.main()

