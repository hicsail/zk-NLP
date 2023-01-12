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



class TestGenerateTarget(unittest.TestCase):
    def test_generate_target_after_all(self):

        type = "after_all"

        # Test case 1: Check if the target is correct when length = 1
        txt = "Hello World"
        length = 1
        string_a, string_target = util.generate_target(txt, type, length)
        self.assertEqual(string_a, "Hello")
        self.assertEqual(string_target, ["World"])


        # Test case 2: Check if the target is correct when length > 1
        txt = "Hello New World"
        length = 2
        string_a, string_target = util.generate_target(txt, type, length)
        self.assertEqual(string_a, "Hello")
        self.assertEqual(string_target, ["New", "World"])


        # Test case 3: Check if the correct message is printed when length > len(txt)-1
        txt = "Hello New World"
        length = 12
        string_a, string_target = util.generate_target(txt, type, length)
        self.assertEqual(string_a, "Hello")
        self.assertEqual(string_target, ["New", "World"])


        # Test case 4: Check if the correct message is printed when length <= 0
        txt = "Hello New World"
        length = -1
        string_a, string_target = util.generate_target(txt, type, length)
        self.assertEqual(string_a, "New")
        self.assertEqual(string_target, ["World"])



    def test_generate_target_after(self):

        type = "after"

        # Test case 1: Check if the base works, no length value given
        txt = "Hello World"
        string_a, string_target = util.generate_target(txt, type)
        self.assertTrue(isinstance(string_target, str))
        self.assertTrue(isinstance(string_a, str))


        # Test case 2: Check if length value has no influence
        txt = "Hello World"
        length = 2
        string_a, string_target = util.generate_target(txt, type, length)
        self.assertTrue(isinstance(string_target, str))
        self.assertTrue(isinstance(string_a, str))
        self.assertTrue((string_a=="Hello" and string_target== "World") or 
                        (string_a=="World" and string_target== ""))



    def test_generate_target_begins(self):

        type = "begins"

        # Test case 1: Check if the base works, no length value given
        txt = "Hello World"
        string_a = util.generate_target(txt, type)
        self.assertEqual(string_a, "Hello")


        # Test case 2: Check if length value has no influence
        txt = "Hello World"
        length = 2
        string_a = util.generate_target(txt, type, length)
        self.assertEqual(string_a, "Hello")



    def test_generate_target_between(self):

        type = "between"

        # Test case 1: Check if the base works, no length value given
        txt = "Hello New World"
        string_a, string_target, string_b = util.generate_target(txt, type)
        self.assertTrue(isinstance(string_target, list))
        self.assertTrue((string_a == "Hello" and string_target == ["New"] and string_b== "World") or
        (string_a == "New" and string_target == ["World"] and string_b== ""))


        # Test case 2: Check if the target is correct when length > 1
        txt = "Hello New World"
        length = 2
        string_a, string_target, string_b = util.generate_target(txt, type, length)
        self.assertTrue(isinstance(string_target, list))
        self.assertEqual(string_a, "Hello")
        self.assertEqual(string_target, ["New", "World"])


        # Test case 3: Check if the correct message is printed when length > len(txt)-1
        txt = "Hello New World"
        length = 10
        string_a, string_target, string_b = util.generate_target(txt, type, length)
        self.assertTrue(isinstance(string_target, list))
        self.assertEqual(string_a, "Hello")
        self.assertEqual(string_target, ["New", "World"])


        # Test case 4: Check if the correct message is printed when length <= 0
        txt = "Hello New World"
        length = -1
        string_a, string_target, string_b = util.generate_target(txt, type, length)
        self.assertTrue(isinstance(string_target, list))
        self.assertTrue((string_a == "Hello" and string_target == ["New"] and string_b== "World") or
        (string_a == "New" and string_target == ["World"] and string_b== ""))



    def test_generate_target_point_to(self):

        type = "point_to"
        
        # Test case 1: Check if the target is correct when length = 1
        txt = "Hello New World"
        length = 1
        string_a, string_target = util.generate_target(txt, type, length)
        self.assertTrue(isinstance(string_target, list))
        self.assertEqual(string_a, "New")
        self.assertEqual(string_target, ["Hello"])


        # Test case 2: Check if the target is correct when length > 1
        txt = "Hello New World"
        length = 2
        string_a, string_target = util.generate_target(txt, type, length)
        self.assertEqual(string_a, "World")
        self.assertEqual(string_target, ["Hello", "New"])


        # Test case 3: Check if the correct message is printed when length > len(txt)
        txt = "Hello New World"
        length = 12
        string_a, string_target = util.generate_target(txt, type, length)
        self.assertEqual(string_a, "")
        self.assertEqual(string_target, ["Hello", "New", "World"])


        # Test case 4: Check if the correct message is printed when length <= 0
        txt = "Hello New World"
        length = -1
        string_a, string_target = util.generate_target(txt, type, length)
        self.assertEqual(string_a, "New")
        self.assertEqual(string_target, ["Hello"])



    def test_generate_target_string_search(self):

        type = "string_search"

        # Test case 1: Check if the base case works, no length value given
        txt = "Hello World"
        string_target = util.generate_target(txt, type)
        self.assertTrue(isinstance(string_target, str))
        self.assertTrue(string_target == "Hello" or string_target == "World")


        # Test case 2: Check if length value has no influence
        txt = "Hello World"
        length = 10
        string_target = util.generate_target(txt, type, length)
        self.assertTrue(isinstance(string_target, str))
        self.assertTrue(string_target == "Hello" or string_target == "World")


    def test_generate_target_stringlist_search(self):

        type = "stringlist_search"

        # Test case 1: Check if the base case works with length=1 and n_string=1
        txt = "Hello New World"
        length = 1
        n_string = 1
        string_target = util.generate_target(txt, type, length, n_string)
        self.assertTrue(isinstance(string_target, list))
        self.assertTrue(string_target == ["Hello"] or string_target == ["New"] or string_target == ["World"])


        # Test case 2: Check if the target is correct when length > 1
        txt = "Hello New World"
        length = 2
        n_string = 1
        string_target = util.generate_target(txt, type, length)
        self.assertTrue(isinstance(string_target, list))
        self.assertTrue(string_target == ["Hello New"] or string_target == ["New World"])


        # Test case 3: Check if the target is correct when length > len(txt)
        txt = "Hello New World"
        length = 4
        n_string = 1
        string_target = util.generate_target(txt, type, length)
        self.assertTrue(isinstance(string_target, list))
        self.assertTrue(string_target == ["Hello New World"])


        # Test case 4: Check if the target is correct when length * n_string > len(txt)
        txt = "Hello New World"
        length = 2
        n_string = 2
        string_target = util.generate_target(txt, type, length)
        self.assertTrue(isinstance(string_target, list))
        self.assertTrue(string_target == ["Hello New"] or string_target == ["New World"])


        # Test case 5: Check if the target is correct when length and n_string are negative values
        txt = "Hello New World"
        length = -1
        n_string = -1
        string_target = util.generate_target(txt, type, length)
        self.assertTrue(string_target == ["Hello"] or string_target == ["New"] or string_target == ["World"])

if __name__ == '__main__':
    unittest.main()

