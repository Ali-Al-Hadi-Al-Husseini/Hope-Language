import unittest

from .lang import *
from .lang import List,String,Number

from .pythonfy import convert_from_hope_to_python_objects


class TestOperators(unittest.TestCase):

    def test_operator(self):
        test_cases_success = [
            
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