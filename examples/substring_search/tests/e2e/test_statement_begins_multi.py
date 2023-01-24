import sys
import unittest
from unittest.mock import patch
from miniwizpl import *
from miniwizpl.expr import *

sys.path.append("/usr/src/app/examples/substring_search/IR0")
import begins_multi as statement

sys.path.append("/usr/src/app/examples/substring_search/common")
import util

class TestStatement(unittest.TestCase):
    
    def test_base(self):

        '''
            A base case to pass, target strings being 'one' and 'two'
        '''

        target_strings =  ['one', 'two']
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_states = [i for i in range(0,len(target_strings))]
        accept_state=100
        error_state=101

        dfa = statement.dfa_from_string(target_strings, zero_states, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_states, error_state)
        self.assertEqual(val_of(latest_state), accept_state)
        self.assertTrue(val_of(latest_state) not in zero_states)
        self.assertNotEqual(val_of(latest_state), error_state)


    def test_fail(self):

        '''
            A base case to fail, target strings being 'two'
        '''

        target_strings =  ['two']
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'
        corpus = corpus.split()
        file_string = SecretList([util.word_to_integer(_str) for _str in corpus])

        zero_states = [i for i in range(0,len(target_strings))]
        accept_state=100
        error_state=101

        dfa = statement.dfa_from_string(target_strings, zero_states, accept_state)
        latest_state = statement.run_dfa(dfa, file_string, zero_states, error_state)
        self.assertNotEqual(val_of(latest_state), accept_state)
        self.assertEqual(val_of(latest_state), error_state)
        self.assertTrue(val_of(latest_state) not in zero_states)

if __name__ == '__main__':
    unittest.main()

