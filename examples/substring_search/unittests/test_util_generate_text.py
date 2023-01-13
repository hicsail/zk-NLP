import unittest
import sys
sys.path.append("/usr/src/app/examples/substring_search/common")
import util


class TestGenerateText(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()

