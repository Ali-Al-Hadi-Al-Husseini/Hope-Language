import unittest

from .Hope import *
from .Hope import List,String,Number
from .pythonfy import matches

class TestVariables(unittest.TestCase):

    def test_variables(self):
        test_Cases_success = [
            ("""let x = 0; print(x+1)""",[0,"1"] , None),
            ("""let x = "test_case"; print(x + " hello")""",["test_case",'test_case hello'] , None),
            ("""let x = 17; print(x*2 + 7 / 3 - 8)""", [17, "28.333333333333336"], None),
            ("""let x = abc; print(x+1)""" ,[], RunTimeError),
            ("""let x = 1; print(abc+1)""" ,[], RunTimeError)    
        ]
        for code, expected_result, expected_error in test_Cases_success:
            result , error = run(code,"test.hope")

            self.assertTrue(matches(result,expected_result))

            if error is not None:
                self.assertTrue(isinstance(error,expected_error))
            else:
                self.assertEqual(error,expected_error)



if __name__ == '__main__':
    unittest.main()