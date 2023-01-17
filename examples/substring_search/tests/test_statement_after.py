import sys
import unittest
from unittest.mock import patch
from miniwizpl import *
from miniwizpl.expr import *

sys.path.append("/usr/src/app/examples/substring_search/IR0")
import after as statement

sys.path.append("/usr/src/app/examples/substring_search/common")
import util

class TestStatement(unittest.TestCase):
    
    def test_base(self):

        '''
            A base case to pass, target strings being at the beginning of the corpus 
            No trickiness involved
        '''

        string_a = 'one'
        string_target =  'two'
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_state = 0
        found_state=1 
        accept_state=100
        error_state=101

        dfa = statement.dfa_from_string(string_a, string_target, zero_state, found_state, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_state, accept_state, error_state)
        self.assertEqual(val_of(latest_state), accept_state)


    def test_fail(self):

        '''
            A base case to fail, target strings being at the beginning of the corpus 
            'three' comes immediately after 'one' in string_target, skipping 'two'
        '''

        string_a = 'one'
        string_target =  'three'
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_state = 0
        found_state=1 
        accept_state=100
        error_state=101

        dfa = statement.dfa_from_string(string_a, string_target, zero_state, found_state, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_state, accept_state, error_state)
        self.assertNotEqual(val_of(latest_state), accept_state)


    def test_fail_intermediate(self):

        '''
            An intermediate case to fail, string_a does not exist in the corpus 
            'three' comes immediately after 'one' in string_target, skipping 'two'
        '''

        string_a = 'xxx'
        string_target =  'one'
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_state = 0
        found_state=1 
        accept_state=100
        error_state=101

        dfa = statement.dfa_from_string(string_a, string_target, zero_state, found_state, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_state, accept_state, error_state)
        self.assertNotEqual(val_of(latest_state), accept_state)


if __name__ == '__main__':
    unittest.main()

