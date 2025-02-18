import unittest
import sys
sys.path.append("/usr/src/app/examples/substring_search/common")
import util


class TestGenerateTarget(unittest.TestCase):
    def test_generate_target_after_all(self):

        type = "after_all"

        # Test case 1: Check if the target is correct when substring_len = 1
        txt = "Hello World"
        substring_len = 1
        string_a, string_target = util.generate_target(txt, type, substring_len)
        self.assertEqual(string_a, "Hello")
        self.assertEqual(string_target, ["World"])


        # Test case 2: Check if the target is correct when substring_len > 1
        txt = "Hello New World"
        substring_len = 2
        string_a, string_target = util.generate_target(txt, type, substring_len)
        self.assertEqual(string_a, "Hello")
        self.assertEqual(string_target, ["New", "World"])


        # Test case 3: Check if the correct message is printed when substring_len > len(txt)-1
        txt = "Hello New World"
        substring_len = 12
        string_a, string_target = util.generate_target(txt, type, substring_len)
        self.assertEqual(string_a, "Hello")
        self.assertEqual(string_target, ["New", "World"])


        # Test case 4: Check if substring_len is adjusted correctly when substring_len <= 0
        txt = "Hello New World"
        substring_len = -1
        string_a, string_target = util.generate_target(txt, type, substring_len)
        self.assertEqual(string_a, "New")
        self.assertEqual(string_target, ["World"])



    def test_generate_target_after_all_multi(self):

        type = "after_all_multi"

        # Test case 1: Check if the base works
        txt = "one two three four"
        substring_len = 2
        piv_len=2
        string_a, string_target = util.generate_target(txt, type, substring_len, piv_len)
        self.assertTrue(isinstance(string_target, list))
        self.assertTrue(isinstance(string_a, list))
        self.assertEqual(string_a, ["one", "two"])
        self.assertEqual(string_target, [ "three", "four"])


        # Test case 2: Check if substring_len and piv_len correctly adjusted when substring_len > len(txt)-1
        txt = "one two three four"
        substring_len = 12
        piv_len=2
        string_a, string_target = util.generate_target(txt, type, substring_len, piv_len)
        self.assertEqual(string_a, ["one"])
        self.assertEqual(string_target, ["two", "three", "four"])


        # Test case 5: Check if substring_len and piv_len correctly adjusted when substring_len<0 and piv_len<0
        txt = "one two three four"
        substring_len = -1
        piv_len=-1
        string_a, string_target = util.generate_target(txt, type, substring_len, piv_len)
        self.assertEqual(string_a, ["three"])
        self.assertEqual(string_target, ["four"])



    def test_generate_target_after(self):

        type = "after"

        # Test case 1: Check if the base works, no substring_len value given
        txt = "Hello World"
        string_a, string_target = util.generate_target(txt, type)
        self.assertTrue(isinstance(string_target, str))
        self.assertTrue(isinstance(string_a, str))
        self.assertEqual(string_a, "Hello")
        self.assertEqual(string_target, "World")


        # Test case 2: Check if substring_len value has no influence
        txt = "Hello World"
        substring_len = 2
        string_a, string_target = util.generate_target(txt, type, substring_len)
        self.assertTrue(isinstance(string_target, str))
        self.assertTrue(isinstance(string_a, str))
        self.assertTrue((string_a=="Hello" and string_target== "World") or 
                        (string_a=="World" and string_target== ""))



    def test_generate_target_after_multi(self):

        type = "after_multi"

        # Test case 1: Check if the base works
        txt = "one two three four"
        substring_len = 2
        piv_len=2
        string_a, string_target = util.generate_target(txt, type, substring_len, piv_len)
        self.assertTrue(isinstance(string_target, list))
        self.assertTrue(isinstance(string_a, list))
        self.assertEqual(string_a, ["one", "two"])
        self.assertEqual(string_target, [ "three", "four"])


        # Test case 2: Check if substring_len and piv_len correctly adjusted when substring_len > len(txt)-1
        txt = "one two three four"
        substring_len = 12
        piv_len=2
        string_a, string_target = util.generate_target(txt, type, substring_len, piv_len)
        self.assertEqual(string_a, ["one"])
        self.assertEqual(string_target, ["two", "three", "four"])


        # Test case 3: Check if substring_len and piv_len correctly adjusted when substring_len<0 and piv_len<0
        txt = "one two three four"
        substring_len = -1
        piv_len=-1
        string_a, string_target = util.generate_target(txt, type, substring_len, piv_len)
        self.assertTrue((string_a==["one"] and string_target== ["two"]) or 
                        (string_a==["two"] and string_target== ["three"]) or 
                        (string_a==["three"] and string_target== ["four"]))



    def test_generate_target_begins(self):

        type = "begins"

        # Test case 1: Check if the base works, no substring_len value given
        txt = "Hello World"
        string_a = util.generate_target(txt, type)
        self.assertEqual(string_a, "Hello")


        # Test case 2: Check if substring_len value has no influence
        txt = "Hello World"
        substring_len = 2
        string_a = util.generate_target(txt, type, substring_len)
        self.assertEqual(string_a, "Hello")



    def test_generate_target_begins_multi(self):

        type = "begins_multi"

        # Test case 1: Check if the base works, no substring_len value given
        txt = "Hello World"
        string_a = util.generate_target(txt, type)
        self.assertEqual(string_a, ["Hello"])


        # Test case 2: Check if substring_len value has no influence
        txt = "Hello World"
        piv_len = 2
        string_a = util.generate_target(txt, type, piv_len=piv_len)
        self.assertEqual(string_a, ["Hello", "World"])



    def test_generate_target_between(self):

        type = "between"

        # Test case 1: Check if the base works, no substring_len value given
        txt = "Hello New World"
        string_a, string_target, string_b = util.generate_target(txt, type)
        self.assertTrue(isinstance(string_target, list))
        self.assertTrue(string_a == "Hello" and string_target == ["New"] and string_b== "World")


        # Test case 2: Check if the target is correct when substring_len > 1
        txt = "Hello New World Yes"
        substring_len = 2
        string_a, string_target, string_b = util.generate_target(txt, type, substring_len)
        self.assertTrue(isinstance(string_target, list))
        self.assertTrue(string_a == "Hello" and string_target == ["New", "World"] and string_b== "Yes")


        # Test case 3: Check if substring_len correctly adjusted when lsubstring_len > len(txt)-1
        txt = "Hello New World Yes"
        substring_len = 10
        string_a, string_target, string_b = util.generate_target(txt, type, substring_len)
        self.assertTrue(isinstance(string_target, list))
        self.assertTrue(string_a == "Hello" and string_target == ["New", "World"] and string_b== "Yes")


        # Test case 4: Check if substring_len correctly adjusted when substring_len <= 0
        txt = "Hello New World"
        substring_len = -1
        string_a, string_target, string_b = util.generate_target(txt, type, substring_len)
        self.assertTrue(isinstance(string_target, list))
        self.assertTrue(string_a == "Hello" and string_target == ["New"] and string_b== "World")



    def test_generate_target_between_multi(self):

        type = "between_multi"

        # Test case 1: Check if the base works, no substring_len value given
        txt = "Hello New World"
        string_a, string_target, string_b = util.generate_target(txt, type)
        self.assertTrue(isinstance(string_a, list))
        self.assertTrue(isinstance(string_target, list))
        self.assertTrue(isinstance(string_b, list))
        self.assertTrue(string_a == ["Hello"] and string_target == ["New"] and string_b== ["World"])


        # Test case 2: Check if the target is correct when substring_len > 1
        txt = "Hello Beautiful New World"
        substring_len = 2
        string_a, string_target, string_b = util.generate_target(txt, type, substring_len)
        self.assertEqual(string_a, ["Hello"])
        self.assertEqual(string_target, ["Beautiful", "New"])
        self.assertEqual(string_b, ["World"])


        # Test case 3: Check if the correct message is printed when substring_len and piv_len are both > 1
        txt = "one two three four five six"
        substring_len = 2
        piv_len=2
        string_a, string_target, string_b = util.generate_target(txt, type, substring_len, piv_len)
        self.assertEqual(string_a, ["one", "two"])
        self.assertEqual(string_target, ["three", "four"])
        self.assertEqual(string_b, ["five", "six"])


        # Test case 4: Check if substring_len and piv_len correctly adjusted when substring_len >= len(txt) and when substring_len + piv_len > len(txt) after the adjustment
        txt = "one two three four five six"
        substring_len = 6
        piv_len=2
        string_a, string_target, string_b = util.generate_target(txt, type, substring_len, piv_len)
        self.assertEqual(string_a, ["one"])
        self.assertEqual(string_target, ["two", "three", "four", "five"])
        self.assertEqual(string_b, ["six"])

        # Test case 4: Check if substring_len and piv_len correctly adjusted when substring_len <= 0
        txt = "Hello New World"
        substring_len = -1
        piv_len=-1
        string_a, string_target, string_b = util.generate_target(txt, type, substring_len, piv_len)
        self.assertTrue(string_a == ["Hello"] and string_target == ["New"] and string_b== ["World"])



    def test_generate_target_point_to(self):

        type = "point_to"
        
        # Test case 1: Check if the target is correct when substring_len = 1
        txt = "Hello New World"
        substring_len = 1
        string_a, string_target = util.generate_target(txt, type, substring_len)
        self.assertTrue(isinstance(string_target, list))
        self.assertEqual(string_a, "New")
        self.assertEqual(string_target, ["Hello"])


        # Test case 2: Check if the target is correct when substring_len > 1
        txt = "Hello New World"
        substring_len = 2
        string_a, string_target = util.generate_target(txt, type, substring_len)
        self.assertEqual(string_a, "World")
        self.assertEqual(string_target, ["Hello", "New"])


        # Test case 3: Check if substring_len and piv_len correctly adjusted when substring_len > len(txt)
        txt = "Hello New World"
        substring_len = 12
        string_a, string_target = util.generate_target(txt, type, substring_len)
        self.assertEqual(string_a, "World")
        self.assertEqual(string_target, ["Hello", "New"])


        # Test case 4: Check if substring_len and piv_len correctly adjusted when substring_len <= 0
        txt = "Hello New World"
        substring_len = -1
        string_a, string_target = util.generate_target(txt, type, substring_len)
        self.assertEqual(string_a, "New")
        self.assertEqual(string_target, ["Hello"])



    def test_generate_target_point_to_multi(self):

        type = "point_to_multi"
        
        # Test case 1: Check if the target is correct when substring_len = 1
        txt = "Hello New World"
        substring_len = 1
        piv_len=1
        string_a, string_target = util.generate_target(txt, type, substring_len, piv_len)
        self.assertTrue(isinstance(string_target, list))
        self.assertEqual(string_a, ["New"])
        self.assertEqual(string_target, ["Hello"])


        # Test case 2: Check if the target is correct when substring_len > 1 and piv_len > 1
        txt = "one two three four five six"
        substring_len = 2
        piv_len=2
        string_a, string_target = util.generate_target(txt, type, substring_len, piv_len)
        self.assertEqual(string_a, ["three", "four"])
        self.assertEqual(string_target, ["one", "two"])


        # Test case 3: Check if substring_len and piv_len correctly adjusted when substring_len > len(txt)
        txt = "one two three four five six"
        substring_len = 12
        piv_len=2
        string_a, string_target = util.generate_target(txt, type, substring_len, piv_len)
        self.assertEqual(string_a, ["six"])
        self.assertEqual(string_target, ["one", "two", "three", "four", "five"])


        # Test case 4: Check if substring_len correctly adjusted when substring_len <= 0
        txt = "Hello New World"
        substring_len = -1
        piv_len=2
        string_a, string_target = util.generate_target(txt, type, substring_len, piv_len)
        self.assertEqual(string_a, ["New", "World"])
        self.assertEqual(string_target, ["Hello"])



    def test_generate_target_string_search(self):

        type = "string_search"

        # Test case 1: Check if the base case works, no substring_len value given
        txt = "Hello World"
        string_target = util.generate_target(txt, type)
        self.assertTrue(isinstance(string_target, str))
        self.assertTrue(string_target == "Hello" or string_target == "World")


        # Test case 2: Check if substring_len value has no influence
        txt = "Hello World"
        substring_len = 10
        string_target = util.generate_target(txt, type, substring_len)
        self.assertTrue(isinstance(string_target, str))
        self.assertTrue(string_target == "Hello" or string_target == "World")


    def test_generate_target_stringlist_search(self):

        type = "stringlist_search"

        # Test case 1: Check if the base case works with substring_len=1 and piv_len=1
        txt = "Hello New World"
        substring_len = 1
        string_target = util.generate_target(txt, type, substring_len)
        self.assertTrue(isinstance(string_target, list))
        self.assertTrue(string_target == ["Hello"] or string_target == ["New"] or string_target == ["World"])


        # Test case 2: Check if the target is correct when substring_len > 1
        txt = "Hello New World"
        substring_len = 2
        string_target = util.generate_target(txt, type, substring_len)
        self.assertTrue(isinstance(string_target, list))
        self.assertTrue(string_target == ["Hello New"] or string_target == ["New World"])


        # Test case 3: Check if the target is correct when substring_len > len(txt)
        txt = "Hello New World"
        substring_len = 4
        string_target = util.generate_target(txt, type, substring_len)
        self.assertTrue(isinstance(string_target, list))
        self.assertTrue(string_target == ["Hello New World"])


        # Test case 4: Check if the target is correct when substring_len * piv_len > len(txt)
        txt = "Hello New World"
        substring_len = 2
        string_target = util.generate_target(txt, type, substring_len)
        self.assertTrue(isinstance(string_target, list))
        self.assertTrue(string_target == ["Hello New"] or string_target == ["New World"])


        # Test case 5: Check if the target is correct when substring_len and piv_len are negative values
        txt = "Hello New World"
        substring_len = -1
        string_target = util.generate_target(txt, type, substring_len)
        self.assertTrue(string_target == ["Hello"] or string_target == ["New"] or string_target == ["World"])


if __name__ == '__main__':
    unittest.main()

