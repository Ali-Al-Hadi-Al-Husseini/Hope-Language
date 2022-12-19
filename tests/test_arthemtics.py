import unittest

from Hope import *
from Hope import List,String,Number

from pythonfy import convert_from_hope_to_python_objects


class TestArthemtics(unittest.TestCase):

    def test_arthemtics(self):
        test_cases_success = [
            ("(2+1)",[3] , None),
            ("(-2+1)",[-1] , None),
            ("(7 * 2)",[14] , None),
            ("(7 * 3)",[21] , None),
            ("(3 / 3)",[1.0] , None),
            ("(9 / 3 )",[3.0] , None),
            ("(9 / 3  + 1)",[4.0] , None), 
            ("(6 / 3  + 2 )",[4.0] , None),
            ("(9 / 3  * 2 )",[6.0] , None),
            ("(9 / 3  - 1)",[2.0] , None), 
            ("(6 / 3  - 2 )",[0.0] , None),
            ("(9 / 3  * -2 )",[-6.0] , None),
            ("((9 / 3)  * 0 )",[0.0] , None),
            ("((9 / 3) / 0 )",[None] , RunTimeError),
            (""" 'abc' * 'xyz """,[None] , RunTimeError),

        ]

        for code, expected_result, expected_error in test_cases_success:
            result , error = run(code,"test.hope")

            if result != [None] :
                result = convert_from_hope_to_python_objects(result)
                self.assertEqual(result, expected_result)

            if error is not None:        
                self.assertTrue(isinstance(error,expected_error))
            else:
                self.assertEqual(error,expected_error)




if __name__ == '__main__':
    unittest.main()