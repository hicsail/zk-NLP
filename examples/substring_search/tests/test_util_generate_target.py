import unittest
import sys
sys.path.append("/usr/src/app/examples/substring_search/common")
import util


class TestGenerateTarget(unittest.TestCase):
#     def test_generate_target_after_all(self):

#         type = "after_all"

#         # Test case 1: Check if the target is correct when length = 1
#         txt = "Hello World"
#         length = 1
#         string_a, string_target = util.generate_target(txt, type, length)
#         self.assertEqual(string_a, "Hello")
#         self.assertEqual(string_target, ["World"])


#         # Test case 2: Check if the target is correct when length > 1
#         txt = "Hello New World"
#         length = 2
#         string_a, string_target = util.generate_target(txt, type, length)
#         self.assertEqual(string_a, "Hello")
#         self.assertEqual(string_target, ["New", "World"])


#         # Test case 3: Check if the correct message is printed when length > len(txt)-1
#         txt = "Hello New World"
#         length = 12
#         string_a, string_target = util.generate_target(txt, type, length)
#         self.assertEqual(string_a, "Hello")
#         self.assertEqual(string_target, ["New", "World"])


#         # Test case 4: Check if the correct message is printed when length <= 0
#         txt = "Hello New World"
#         length = -1
#         string_a, string_target = util.generate_target(txt, type, length)
#         self.assertEqual(string_a, "New")
#         self.assertEqual(string_target, ["World"])



#     def test_generate_target_after(self):

#         type = "after"

#         # Test case 1: Check if the base works, no length value given
#         txt = "Hello World"
#         string_a, string_target = util.generate_target(txt, type)
#         self.assertTrue(isinstance(string_target, str))
#         self.assertTrue(isinstance(string_a, str))


#         # Test case 2: Check if length value has no influence
#         txt = "Hello World"
#         length = 2
#         string_a, string_target = util.generate_target(txt, type, length)
#         self.assertTrue(isinstance(string_target, str))
#         self.assertTrue(isinstance(string_a, str))
#         self.assertTrue((string_a=="Hello" and string_target== "World") or 
#                         (string_a=="World" and string_target== ""))



#     def test_generate_target_begins(self):

#         type = "begins"

#         # Test case 1: Check if the base works, no length value given
#         txt = "Hello World"
#         string_a = util.generate_target(txt, type)
#         self.assertEqual(string_a, "Hello")


#         # Test case 2: Check if length value has no influence
#         txt = "Hello World"
#         length = 2
#         string_a = util.generate_target(txt, type, length)
#         self.assertEqual(string_a, "Hello")



#     def test_generate_target_between(self):

#         type = "between"

#         # Test case 1: Check if the base works, no length value given
#         txt = "Hello New World"
#         string_a, string_target, string_b = util.generate_target(txt, type)
#         self.assertTrue(isinstance(string_target, list))
#         self.assertTrue((string_a == "Hello" and string_target == ["New"] and string_b== "World") or
#         (string_a == "New" and string_target == ["World"] and string_b== ""))


#         # Test case 2: Check if the target is correct when length > 1
#         txt = "Hello New World"
#         length = 2
#         string_a, string_target, string_b = util.generate_target(txt, type, length)
#         self.assertTrue(isinstance(string_target, list))
#         self.assertEqual(string_a, "Hello")
#         self.assertEqual(string_target, ["New", "World"])


#         # Test case 3: Check if the correct message is printed when length > len(txt)-1
#         txt = "Hello New World"
#         length = 10
#         string_a, string_target, string_b = util.generate_target(txt, type, length)
#         self.assertTrue(isinstance(string_target, list))
#         self.assertEqual(string_a, "Hello")
#         self.assertEqual(string_target, ["New", "World"])


#         # Test case 4: Check if the correct message is printed when length <= 0
#         txt = "Hello New World"
#         length = -1
#         string_a, string_target, string_b = util.generate_target(txt, type, length)
#         self.assertTrue(isinstance(string_target, list))
#         self.assertTrue((string_a == "Hello" and string_target == ["New"] and string_b== "World") or
#         (string_a == "New" and string_target == ["World"] and string_b== ""))



#     def test_generate_target_point_to(self):

#         type = "point_to"
        
#         # Test case 1: Check if the target is correct when length = 1
#         txt = "Hello New World"
#         length = 1
#         string_a, string_target = util.generate_target(txt, type, length)
#         self.assertTrue(isinstance(string_target, list))
#         self.assertEqual(string_a, "New")
#         self.assertEqual(string_target, ["Hello"])


#         # Test case 2: Check if the target is correct when length > 1
#         txt = "Hello New World"
#         length = 2
#         string_a, string_target = util.generate_target(txt, type, length)
#         self.assertEqual(string_a, "World")
#         self.assertEqual(string_target, ["Hello", "New"])


#         # Test case 3: Check if the correct message is printed when length > len(txt)
#         txt = "Hello New World"
#         length = 12
#         string_a, string_target = util.generate_target(txt, type, length)
#         self.assertEqual(string_a, "")
#         self.assertEqual(string_target, ["Hello", "New", "World"])


#         # Test case 4: Check if the correct message is printed when length <= 0
#         txt = "Hello New World"
#         length = -1
#         string_a, string_target = util.generate_target(txt, type, length)
#         self.assertEqual(string_a, "New")
#         self.assertEqual(string_target, ["Hello"])



#     def test_generate_target_string_search(self):

#         type = "string_search"

#         # Test case 1: Check if the base case works, no length value given
#         txt = "Hello World"
#         string_target = util.generate_target(txt, type)
#         self.assertTrue(isinstance(string_target, str))
#         self.assertTrue(string_target == "Hello" or string_target == "World")


#         # Test case 2: Check if length value has no influence
#         txt = "Hello World"
#         length = 10
#         string_target = util.generate_target(txt, type, length)
#         self.assertTrue(isinstance(string_target, str))
#         self.assertTrue(string_target == "Hello" or string_target == "World")


#     def test_generate_target_stringlist_search(self):

#         type = "stringlist_search"

#         # Test case 1: Check if the base case works with length=1 and n_string=1
#         txt = "Hello New World"
#         length = 1
#         n_string = 1
#         string_target = util.generate_target(txt, type, length, n_string)
#         self.assertTrue(isinstance(string_target, list))
#         self.assertTrue(string_target == ["Hello"] or string_target == ["New"] or string_target == ["World"])


#         # Test case 2: Check if the target is correct when length > 1
#         txt = "Hello New World"
#         length = 2
#         n_string = 1
#         string_target = util.generate_target(txt, type, length)
#         self.assertTrue(isinstance(string_target, list))
#         self.assertTrue(string_target == ["Hello New"] or string_target == ["New World"])


#         # Test case 3: Check if the target is correct when length > len(txt)
#         txt = "Hello New World"
#         length = 4
#         n_string = 1
#         string_target = util.generate_target(txt, type, length)
#         self.assertTrue(isinstance(string_target, list))
#         self.assertTrue(string_target == ["Hello New World"])


#         # Test case 4: Check if the target is correct when length * n_string > len(txt)
#         txt = "Hello New World"
#         length = 2
#         n_string = 2
#         string_target = util.generate_target(txt, type, length)
#         self.assertTrue(isinstance(string_target, list))
#         self.assertTrue(string_target == ["Hello New"] or string_target == ["New World"])


#         # Test case 5: Check if the target is correct when length and n_string are negative values
#         txt = "Hello New World"
#         length = -1
#         n_string = -1
#         string_target = util.generate_target(txt, type, length)
#         self.assertTrue(string_target == ["Hello"] or string_target == ["New"] or string_target == ["World"])


    def test_generate_target_after_all_multi(self):

            type = "after_all_multi"

            # Test case 1: Check if the target is correct when length = 2 and n_string=2
            txt = "one two three four"
            length = 2
            n_string=2
            string_a, string_target = util.generate_target(txt, type, length, n_string)
            self.assertEqual(string_a, ["one", "two"])
            self.assertEqual(string_target, ["three", "four"])


            # Test case 2: Check if the correct message is printed when length > len(txt)-1
            txt = "one two three four"
            length = 12
            n_string=2
            string_a, string_target = util.generate_target(txt, type, length, n_string)
            self.assertEqual(string_a, ["one"])
            self.assertEqual(string_target, ["two", "three", "four"])

            # Test case 3: Check if the correct message is printed when length + n_string> len(txt)-1
            txt = "one two three four"
            length = 2
            n_string=3
            string_a, string_target = util.generate_target(txt, type, length, n_string)
            self.assertEqual(string_a, ["one", "two"])
            self.assertEqual(string_target, ["three", "four"])


            # Test case 3: Check if the correct message is printed when length<0 and n_string<0
            txt = "one two three four"
            length = -1
            n_string=-1
            string_a, string_target = util.generate_target(txt, type, length, n_string)
            self.assertEqual(string_a, ["three"])
            self.assertEqual(string_target, ["four"])



    def test_generate_target_after_multi(self):

        type = "after_multi"

        # Test case 1: Check if the base works, no length value given
        txt = "one two three four"
        length = 2
        n_string=2
        string_a, string_target = util.generate_target(txt, type, length, n_string)
        self.assertTrue(isinstance(string_target, list))
        self.assertTrue(isinstance(string_a, list))


        # Test case 2: Check if length value has no influence
        txt = "one two three four"
        length = 2
        n_string=2
        string_a, string_target = util.generate_target(txt, type, length, n_string)
        self.assertEqual(string_a, ["one", "two"])
        self.assertEqual(string_target, [ "three", "four"])


        # Test case 3: Check if the correct message is printed when length > len(txt)-1
        txt = "one two three four"
        length = 12
        n_string=2
        string_a, string_target = util.generate_target(txt, type, length, n_string)
        self.assertEqual(string_a, ["one","two", "three"])
        self.assertEqual(string_target, ["four"])

        # Test case 4: Check if the correct message is printed when length + n_string> len(txt)-1
        txt = "one two three four"
        length = 2
        n_string=3
        string_a, string_target = util.generate_target(txt, type, length, n_string)
        self.assertEqual(string_a, ["one", "two"])
        self.assertEqual(string_target, ["three", "four"])


        # Test case 5: Check if the correct message is printed when length<0 and n_string<0
        txt = "one two three four"
        length = -1
        n_string=-1
        string_a, string_target = util.generate_target(txt, type, length, n_string)
        self.assertEqual(string_a, ["one","three"])
        self.assertEqual(string_target, ["two"])

    # def test_generate_target_begins_multi(self):

    #     type = "begins_multi"

    #     # Test case 1: Check if the base works, no length value given
    #     txt = "Hello World"
    #     string_a = util.generate_target(txt, type)
    #     self.assertEqual(string_a, "Hello")


    #     # Test case 2: Check if length value has no influence
    #     txt = "Hello World"
    #     length = 2
    #     string_a = util.generate_target(txt, type, length)
    #     self.assertEqual(string_a, "Hello")



    # def test_generate_target_between_multi(self):

    #     type = "between_multi"

    #     # Test case 1: Check if the base works, no length value given
    #     txt = "Hello New World"
    #     string_a, string_target, string_b = util.generate_target(txt, type)
    #     self.assertTrue(isinstance(string_target, list))
    #     self.assertTrue((string_a == "Hello" and string_target == ["New"] and string_b== "World") or
    #     (string_a == "New" and string_target == ["World"] and string_b== ""))


    #     # Test case 2: Check if the target is correct when length > 1
    #     txt = "Hello New World"
    #     length = 2
    #     string_a, string_target, string_b = util.generate_target(txt, type, length)
    #     self.assertTrue(isinstance(string_target, list))
    #     self.assertEqual(string_a, "Hello")
    #     self.assertEqual(string_target, ["New", "World"])


    #     # Test case 3: Check if the correct message is printed when length > len(txt)-1
    #     txt = "Hello New World"
    #     length = 10
    #     string_a, string_target, string_b = util.generate_target(txt, type, length)
    #     self.assertTrue(isinstance(string_target, list))
    #     self.assertEqual(string_a, "Hello")
    #     self.assertEqual(string_target, ["New", "World"])


    #     # Test case 4: Check if the correct message is printed when length <= 0
    #     txt = "Hello New World"
    #     length = -1
    #     string_a, string_target, string_b = util.generate_target(txt, type, length)
    #     self.assertTrue(isinstance(string_target, list))
    #     self.assertTrue((string_a == "Hello" and string_target == ["New"] and string_b== "World") or
    #     (string_a == "New" and string_target == ["World"] and string_b== ""))



    # def test_generate_target_point_to_multi(self):

    #     type = "point_to_multi"
        
    #     # Test case 1: Check if the target is correct when length = 1
    #     txt = "Hello New World"
    #     length = 1
    #     string_a, string_target = util.generate_target(txt, type, length)
    #     self.assertTrue(isinstance(string_target, list))
    #     self.assertEqual(string_a, "New")
    #     self.assertEqual(string_target, ["Hello"])


    #     # Test case 2: Check if the target is correct when length > 1
    #     txt = "Hello New World"
    #     length = 2
    #     string_a, string_target = util.generate_target(txt, type, length)
    #     self.assertEqual(string_a, "World")
    #     self.assertEqual(string_target, ["Hello", "New"])


    #     # Test case 3: Check if the correct message is printed when length > len(txt)
    #     txt = "Hello New World"
    #     length = 12
    #     string_a, string_target = util.generate_target(txt, type, length)
    #     self.assertEqual(string_a, "")
    #     self.assertEqual(string_target, ["Hello", "New", "World"])


    #     # Test case 4: Check if the correct message is printed when length <= 0
    #     txt = "Hello New World"
    #     length = -1
    #     string_a, string_target = util.generate_target(txt, type, length)
    #     self.assertEqual(string_a, "New")
    #     self.assertEqual(string_target, ["Hello"])


if __name__ == '__main__':
    unittest.main()

