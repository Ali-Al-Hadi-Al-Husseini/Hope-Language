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