import sys
import unittest
from unittest.mock import patch
from miniwizpl import *
from miniwizpl.expr import *

sys.path.append("/usr/src/app/examples/substring_search")
import IR0_stringlist_search_begins as statement

sys.path.append("/usr/src/app/examples/substring_search/common")
import util

class TestStatement(unittest.TestCase):
    
    def test_base(self):

        '''
            A base case to pass, target strings being 'one'
        '''

        string_target =  'one'
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_state = 0
        accept_state=100
        error_state=101

        dfa = statement.dfa_from_string(string_target, zero_state, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_state, error_state)
        self.assertEqual(val_of(latest_state), accept_state)


    def test_fail(self):

        '''
            A base case to fail, target strings being 'two'
        '''

        string_target =  'two'
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_state = 0
        accept_state=100
        error_state=101

        dfa = statement.dfa_from_string(string_target, zero_state, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_state, error_state)
        self.assertNotEqual(val_of(latest_state), accept_state)

if __name__ == '__main__':
    unittest.main()

