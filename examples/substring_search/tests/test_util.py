import unittest
import sys
sys.path.append("/usr/src/app/examples/substring_search/common")
import util


class TestUtil(unittest.TestCase):
    def test_is_in_found_states(self):
        initial_state = 5
        found_states = [3, 4, 5, 6]
        self.assertTrue(util.is_in_found_states(initial_state, found_states))
        
        initial_state = 7
        self.assertFalse(util.is_in_found_states(initial_state, found_states))
        
        found_states = []
        self.assertFalse(util.is_in_found_states(initial_state, found_states))


if __name__ == '__main__':
    unittest.main()

