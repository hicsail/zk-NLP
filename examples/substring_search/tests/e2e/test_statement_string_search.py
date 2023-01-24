import sys
import unittest
from unittest.mock import patch
from miniwizpl import *
from miniwizpl.expr import *

sys.path.append("/usr/src/app/examples/substring_search/IR0")
import string_search as statement

class TestStatement(unittest.TestCase):
    
    def test_base(self):

        '''
            A base case to pass, target strings at the beginning of the corpus 
            No trickiness involved
        '''

        string_target =  'one'
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        file_string = SecretList([ord(c) for c in corpus])

        accept_state = 1000000

        dfa = statement.dfa_from_string(string_target, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, accept_state)
        self.assertEqual(val_of(latest_state), accept_state)
        self.assertNotEqual(val_of(latest_state), 0)


    def test_intermediate(self):

        '''
            An intermediate case to pass, target strings in the middle of the corpus 
        '''

        string_target =  'eight'
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        file_string = SecretList([ord(c) for c in corpus])

        accept_state = 1000000

        dfa = statement.dfa_from_string(string_target, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, accept_state)
        self.assertEqual(val_of(latest_state), accept_state)
        self.assertNotEqual(val_of(latest_state), 0)


    def test_intermediate(self):

        '''
            An intermediate case to pass, target strings at the end of the corpus 
        '''

        string_target =  'fifteen'
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        file_string = SecretList([ord(c) for c in corpus])

        accept_state = 1000000

        dfa = statement.dfa_from_string(string_target, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, accept_state)
        self.assertEqual(val_of(latest_state), accept_state)
        self.assertNotEqual(val_of(latest_state), 0)


    def test_fail(self):

        '''
            A base case to fail, non-existing target string at the beginning of the corpus 
        '''

        string_target =  'NotHere'
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        file_string = SecretList([ord(c) for c in corpus])

        accept_state = 1000000

        dfa = statement.dfa_from_string(string_target, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, accept_state)
        self.assertEqual(val_of(latest_state), 0)
        self.assertNotEqual(val_of(latest_state), accept_state)


if __name__ == '__main__':
    unittest.main()

