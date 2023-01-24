import unittest
import sys
from miniwizpl import *
from miniwizpl.expr import *
sys.path.append("/usr/src/app/examples/substring_search/common")
import util


class TestUtil(unittest.TestCase):

    def test_is_in_target_states(self):
        initial_state = 5
        target_states = [3, 4, 5, 6]
        self.assertTrue(util.is_in_target_states(initial_state, target_states))
        
        initial_state = 7
        self.assertFalse(util.is_in_target_states(initial_state, target_states))
        
        target_states = []
        self.assertFalse(util.is_in_target_states(initial_state, target_states))
    

    def test_reconcile_secretstack_base(self):
        '''
            A base case to pass, four same elements in both stack
        '''

        expected = [0, 1, 2, 3]

        SecretStack_ = SecretStack([])
        SecretStack_.push(0)
        SecretStack_.push(1)
        SecretStack_.push(2)
        SecretStack_.push(3)

        test_flag = util.reconcile_secretstack(expected, SecretStack_)
        self.assertTrue(test_flag)


    def test_reconcile_secretstack_intermediate(self):
        '''
            An intermediate case to pass, nothing in both list and stack
        '''
        expected = []

        SecretStack_ = SecretStack([])

        test_flag = util.reconcile_secretstack(expected, SecretStack_)
        self.assertTrue(test_flag)


    def test_fail_reconcile_secretstack_base(self):
        '''
            A base case to fail, the fourth element being different
        '''

        expected = [0, 1, 2, 3]

        SecretStack_ = SecretStack([])
        SecretStack_.push(0)
        SecretStack_.push(1)
        SecretStack_.push(2)
        SecretStack_.push(4)

        test_flag = util.reconcile_secretstack(expected, SecretStack_)
        self.assertFalse(test_flag)


    def test_fail_reconcile_secretstack_base2(self):
        '''
            An base case to pass, elements in reverse order
        '''
        expected = [0, 1, 2, 3]

        SecretStack_ = SecretStack([])
        SecretStack_.push(3)
        SecretStack_.push(2)
        SecretStack_.push(1)
        SecretStack_.push(0)

        test_flag = util.reconcile_secretstack(expected, SecretStack_)
        self.assertFalse(test_flag)


    def test_fail_reconcile_secretstack_intermediate(self):
        '''
            An intermediate case to fail, last element missing in stack
        '''
        expected = [0, 1, 2, 3]

        SecretStack_ = SecretStack([])
        SecretStack_.push(0)
        SecretStack_.push(1)
        SecretStack_.push(2)

        test_flag = util.reconcile_secretstack(expected, SecretStack_)
        self.assertFalse(test_flag)


    def test_fail_reconcile_secretstack_intermediate2(self):
        '''
            An intermediate case to fail, last element missing in stack
        '''
        expected = [0, 1, 2]

        SecretStack_ = SecretStack([])
        SecretStack_.push(0)
        SecretStack_.push(1)
        SecretStack_.push(2)
        SecretStack_.push(3)

        test_flag = util.reconcile_secretstack(expected, SecretStack_)
        self.assertFalse(test_flag)


    def test_after_all_create_exepected_result_base(self):

        '''
            A base case after_all to pass, the target and string being at the end of the corpus
        '''

        file_name='after_all'
        string_a = 'thirteen'
        string_target =  ['fourteen', 'fifteen']
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'

        expected=util.create_exepected_result(file_name, corpus, string_target, string_a)
        
        res=[2138864142, 1647430463]
        self.assertEqual(expected, res)

        res=[1332101368, 2138864142, 1647430463]
        self.assertNotEqual(expected, res)
        

    def test_after_all_fail_create_exepected_result_base(self):

        '''
            A base case after to fail, the target and string being at the end of the corpus, excluding the last string
        '''

        file_name='after_all'
        string_a = 'twelve'
        string_target =  ['thirteen', 'fourteen']
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'

        expected=util.create_exepected_result(file_name, corpus, string_target, string_a)
        
        res=[1758700758, 1332101368, 2138864142]
        self.assertNotEqual(expected, res)


    def test_between_create_exepected_result_base(self):

        '''
            A base case between to pass
        '''

        file_name='between'
        string_a = 'two'
        string_target =  ['three', 'four']
        string_b = 'five'
        corpus = 'one two three four five'

        expected=util.create_exepected_result(file_name, corpus, string_target, string_a, string_b)
        
        res=[534931071, 1169018584, 41408388]
        self.assertEqual(expected, res)

        res=[534931071, 1169018584, 41408388, 286623210]
        self.assertNotEqual(expected, res)


    def test_between_create_exepected_result_intermediate(self):

        '''
            An intermediate case between to pass, the string_b being absent
        '''

        file_name='between'
        string_a = 'two'
        string_target =  ['three', 'four']
        string_b = ''
        corpus = 'one two three four five'

        expected=util.create_exepected_result(file_name, corpus, string_target, string_a, string_b)
        
        res=[534931071, 1169018584, 41408388]
        self.assertEqual(expected, res)

        res=[534931071, 1169018584, 41408388, 286623210]
        self.assertNotEqual(expected, res)


    def test_point_to_create_exepected_result_base(self):

        '''
            A base case point_to to pass
        '''

        file_name='point_to'
        string_a = 'four'
        string_target =  ['one', 'two', 'three']
        corpus = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen'

        expected=util.create_exepected_result(file_name, corpus, string_target, string_a)
        
        res=[994664918, 534931071, 1169018584]
        self.assertEqual(expected, res)


    def test_point_to_create_exepected_result_intermediate(self):

        '''
            An intermediate case point_to to pass, the string_a being absent
        '''

        file_name='point_to'
        string_a = 'four'
        string_target =  ['one', 'two', 'three']
        corpus = 'one two three'

        expected=util.create_exepected_result(file_name, corpus, string_target, string_a)
        
        res=[994664918, 534931071, 1169018584]
        self.assertEqual(expected, res)


if __name__ == '__main__':
    unittest.main()

