import sys
import unittest
from unittest.mock import patch
from miniwizpl import *
from miniwizpl.expr import *

sys.path.append("/usr/src/app/examples/substring_search/IR0")
import point_to_multi as statement

sys.path.append("/usr/src/app/examples/substring_search/common")
import util

class TestStatement(unittest.TestCase):
    
    def test_base(self):

        '''
            A base case to pass
            No trickiness involved
        '''

        string_target =  ['one', 'two'] 
        string_a = ['three','four', 'five']
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_states = [i for i in range(0,len(string_target))]
        found_states=[i for i in range(zero_states[-1]+1,zero_states[-1]+len(string_a)+1)]

        appendedAll_state=found_states[-1]*10
        accept_state = found_states[-1]*100
        error_state = found_states[-1]*101

        Secret_str_before = SecretStack([])

        # Testing final state
        dfa = statement.dfa_from_string(string_a, string_target, zero_states, found_states, appendedAll_state, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_states, found_states, appendedAll_state, accept_state, error_state, Secret_str_before)
        self.assertEqual(val_of(latest_state), accept_state)
        self.assertNotEqual(val_of(latest_state), appendedAll_state)
        self.assertFalse(val_of(latest_state) in found_states)
        self.assertFalse(val_of(latest_state) in zero_states)
        self.assertNotEqual(val_of(latest_state), error_state)

        # Converting strings, target, and corpus into integers, and creating expected list to reconcile the result
        file_name="point_to_multi"
        expected=util.create_exepected_result(file_name, corpus, string_target, string_a)
        test_flag = util.reconcile_secretstack(expected, Secret_str_before)
        self.assertTrue(test_flag)


    def test_intermediate(self):

        '''
            An intermediate case to pass
            string_a does not exist, threfore the latest state shall be appendedAll_state
        '''

        string_target =  ['one', 'two','three','four', 'five'] 
        string_a = ['']
        corpus = 'one two three four five'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_states = [i for i in range(0,len(string_target))]
        found_states=[i for i in range(zero_states[-1]+1,zero_states[-1]+len(string_a)+1)]

        appendedAll_state=found_states[-1]*10
        accept_state = found_states[-1]*100
        error_state = found_states[-1]*101

        Secret_str_before = SecretStack([])

        # Testing final state
        dfa = statement.dfa_from_string(string_a, string_target, zero_states, found_states, appendedAll_state, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_states, found_states, appendedAll_state, accept_state, error_state, Secret_str_before)
        self.assertEqual(val_of(latest_state), appendedAll_state)
        self.assertNotEqual(val_of(latest_state), accept_state)
        self.assertFalse(val_of(latest_state) in found_states)
        self.assertFalse(val_of(latest_state) in zero_states)
        self.assertNotEqual(val_of(latest_state), error_state)

        # Converting strings, target, and corpus into integers, and creating expected list to reconcile the result
        file_name="point_to_multi"
        expected=util.create_exepected_result(file_name, corpus, string_target, string_a)
        test_flag = util.reconcile_secretstack(expected, Secret_str_before)
        self.assertFalse(test_flag)

    def test_fail(self):

        '''
            A base case to fail
            'three' comes immediately after 'one' again in string_target
        '''

        string_target =  ['one'] 
        string_a = ['three']
        corpus = 'one two three four five'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_states = [i for i in range(0,len(string_target))]
        found_states=[i for i in range(zero_states[-1]+1,zero_states[-1]+len(string_a)+1)]

        appendedAll_state=found_states[-1]*10
        accept_state = found_states[-1]*100
        error_state = found_states[-1]*101

        Secret_str_before = SecretStack([])

        # Testing final state
        dfa = statement.dfa_from_string(string_a, string_target, zero_states, found_states, appendedAll_state, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_states, found_states, appendedAll_state, accept_state, error_state, Secret_str_before)
        self.assertEqual(val_of(latest_state), error_state)
        self.assertNotEqual(val_of(latest_state), appendedAll_state)
        self.assertFalse(val_of(latest_state) in found_states)
        self.assertFalse(val_of(latest_state) in zero_states)
        self.assertNotEqual(val_of(latest_state), accept_state)

        # Converting strings, target, and corpus into integers, and creating expected list to reconcile the result
        file_name="point_to_multi"
        expected=util.create_exepected_result(file_name, corpus, string_target, string_a)
        test_flag = util.reconcile_secretstack(expected, Secret_str_before)
        self.assertFalse(test_flag)


    def test_fail_intermediate(self):

        '''
            An intermediate case to fail
            'three', which exists, comes immediately after 'one' in string_target, skipping 'two'
        '''

        string_target =  ['one', 'three'] 
        string_a = ['four', 'five']
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_states = [i for i in range(0,len(string_target))]
        found_states=[i for i in range(zero_states[-1]+1,zero_states[-1]+len(string_a)+1)]

        appendedAll_state=found_states[-1]*10
        accept_state = found_states[-1]*100
        error_state = found_states[-1]*101

        Secret_str_before = SecretStack([])

        # Testing final state
        dfa = statement.dfa_from_string(string_a, string_target, zero_states, found_states, appendedAll_state, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_states, found_states, appendedAll_state, accept_state, error_state, Secret_str_before)
        self.assertEqual(val_of(latest_state), error_state)
        self.assertNotEqual(val_of(latest_state), appendedAll_state)
        self.assertFalse(val_of(latest_state) in found_states)
        self.assertFalse(val_of(latest_state) in zero_states)
        self.assertNotEqual(val_of(latest_state), accept_state)

        # Converting strings, target, and corpus into integers, and creating expected list to reconcile the result
        file_name="point_to_multi"
        expected=util.create_exepected_result(file_name, corpus, string_target, string_a)
        test_flag = util.reconcile_secretstack(expected, Secret_str_before)
        self.assertFalse(test_flag)


if __name__ == '__main__':
    unittest.main()

