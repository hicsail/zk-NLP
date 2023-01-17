import sys
import unittest
from unittest.mock import patch
from miniwizpl import *
from miniwizpl.expr import *

sys.path.append("/usr/src/app/examples/substring_search/IR0")
import point_to as statement

sys.path.append("/usr/src/app/examples/substring_search/common")
import util

class TestStatement(unittest.TestCase):
    
    def test_base(self):

        '''
            A base case to pass
            No trickiness involved
        '''

        string_target =  ['one', 'two'] 
        string_a = 'three'
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_state = 0
        found_states=[i for i in range(1,len(string_target))]

        appendedAll_state=found_states[-1]*10
        accept_state = found_states[-1]*100
        error_state = found_states[-1]*101

        Secret_str_before = SecretStack([])

        dfa = statement.dfa_from_string(string_a, string_target, zero_state, found_states, appendedAll_state, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_state, found_states, appendedAll_state, accept_state, error_state, Secret_str_before)
        self.assertEqual(val_of(latest_state), accept_state)


    def test_intermediate(self):

        '''
            An intermediate case to pass
            string_a does not exist, threfore the latest state shall be appendedAll_state
        '''

        string_target =  ['one', 'two', 'three']
        string_a = 'four'
        corpus = 'one two three'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_state = 0
        found_states=[i for i in range(1,len(string_target))]

        appendedAll_state=found_states[-1]*10
        accept_state = found_states[-1]*100
        error_state = found_states[-1]*101

        Secret_str_before = SecretStack([])

        dfa = statement.dfa_from_string(string_a, string_target, zero_state, found_states, appendedAll_state, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_state, found_states, appendedAll_state, accept_state, error_state, Secret_str_before)
        self.assertEqual(val_of(latest_state), appendedAll_state)


    def test_fail(self):

        '''
            A base case to fail
            'one' comes immediately after 'one' again in string_target
        '''

        string_target =  ['one', 'one'] 
        string_a = 'three'
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_state = 0
        found_states=[i for i in range(1,len(string_target))]

        appendedAll_state=found_states[-1]*10
        accept_state = found_states[-1]*100
        error_state = found_states[-1]*101

        Secret_str_before = SecretStack([])

        dfa = statement.dfa_from_string(string_a, string_target, zero_state, found_states, appendedAll_state, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_state, found_states, appendedAll_state, accept_state, error_state, Secret_str_before)
        self.assertNotEqual(val_of(latest_state), accept_state)


    def test_fail_intermediate(self):

        '''
            An intermediate case to fail
            'three', which exists, comes immediately after 'one' in string_target, skipping 'two'
        '''

        string_target =  ['one', 'three'] 
        string_a = 'four'
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_state = 0
        found_states=[i for i in range(1,len(string_target))]

        appendedAll_state=found_states[-1]*10
        accept_state = found_states[-1]*100
        error_state = found_states[-1]*101

        Secret_str_before = SecretStack([])

        dfa = statement.dfa_from_string(string_a, string_target, zero_state, found_states, appendedAll_state, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_state, found_states, appendedAll_state, accept_state, error_state, Secret_str_before)
        self.assertNotEqual(val_of(latest_state), accept_state)


    def test_fail_intermediate(self):

        '''
            An intermediate case to fail
            string_a does not exist
        '''

        string_target =  ['one', 'three'] 
        string_a = 'hundred'
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_state = 0
        found_states=[i for i in range(1,len(string_target))]

        appendedAll_state=found_states[-1]*10
        accept_state = found_states[-1]*100
        error_state = found_states[-1]*101

        Secret_str_before = SecretStack([])

        dfa = statement.dfa_from_string(string_a, string_target, zero_state, found_states, appendedAll_state, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_state, found_states, appendedAll_state, accept_state, error_state, Secret_str_before)
        self.assertNotEqual(val_of(latest_state), accept_state)

if __name__ == '__main__':
    unittest.main()

