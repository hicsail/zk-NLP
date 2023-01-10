import unittest
import util

class TestUtil(unittest.TestCase):
    def test_generate_text(self):
        # Test with scale=0
        output = util.generate_text(scale=0)
        self.assertIsInstance(output, list)
        self.assertEqual(len(output), 10)

        # Test with scale=1
        output = util.generate_text(scale=1)
        self.assertIsInstance(output, list)
        self.assertEqual(len(output), 20)
        
        # Test with scale=2
        output = util.generate_text(scale=2)
        self.assertIsInstance(output, list)
        self.assertEqual(len(output), 40)
        
        # Test with scale=3
        output = util.generate_text(scale=3)
        self.assertIsInstance(output, list)
        self.assertEqual(len(output), 80)
        
        # Test with negative scale
        self.assertRaises(ValueError, util.generate_text, scale=-1)
        
        # Test with non integer scale
        self.assertRaises(TypeError, util.generate_text, scale='string')


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
    
