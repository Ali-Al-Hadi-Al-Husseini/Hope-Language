import unittest

from .lang import *
from .lang import List,String,Number

from .pythonfy import convert_from_hope_to_python_objects


class TestOperators(unittest.TestCase):

    def test_operator(self):
        test_cases_success = [
            ("1 > 0",[True],None),
            ("1 > 2",[False],None),
            ("1 >= 1",[True],None),
            ("1 > 1",[False],None),
            ("10 < 100",[True],None),
            ("100 < 10 ",[False],None),
            ("7 > -7",[True],None),
            ("17.5 > 17.1",[True],None),
            ("1 > 0 ",[True],None),
            ("19 <= 20",[True],None),
            ("20 <= 10 ",[False],None),
            ("7 >= -7",[True],None),
            ("17.5 >= 17.1",[True],None),
            ("-1 >= -1 ",[True],None),
            ("not 2 > 1  ",[False],None),
            ("not not -1 >= -1 ",[True],None),
            ("not 1",[False],None),
            ("not 0",[True],None),
            ("not not not not not 1",[False],None),
            ("not not not 0",[True],None),
            ("true and false",[False],None),
            ("true and true",[True],None),
            ("false and false",[False],None),
            ("true or false",[True],None),
            ("true or true",[True],None),
            ("false or false",[False],None),
            ("3 > 2 and 2 > 1",[True],None),
            ("not 2 > 1 or 22 > 17",[True],None),
            ("not 2 > 1 and 2 > 1",[False],None),
            ("(not 2 > 1 & 2 > 1) | not 2 > 1 or 22 > 17",[True],None)
        ]

        for code, expected_result, expected_error in test_cases_success:
            result , error = run(code,"test.hope")


            result = convert_from_hope_to_python_objects(result)
            self.assertEqual(result, expected_result)

            if error is not None:        
                self.assertTrue(isinstance(error,expected_error))
            else:
                self.assertEqual(error,expected_error)




if __name__ == '__main__':
    unittest.main()