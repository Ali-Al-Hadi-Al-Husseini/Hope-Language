import unittest
from .hope import run

class TestVariables(unittest.TestCase):

    def test_variables(self):
        test_Cases_success = [
            ("""print(2+1)""",["3"] , None),
            ("""print(-2+1)""",["-1"] , None),
            ("""print(7 * 2)""",["14"] , None),
            ("""print(7 * 3)""",["21"] , None),
            ("""print(3 / 3)""",["1.0"] , None),
            ("""print(9 / 3 )""",["3.0"] , None),
            ("""print(9 / 3  + 1)""",["4.0"] , None), 
            ("""print(6 / 3  + 2 )""",["4.0"] , None),
            ("""print(9 / 3  * 2 )""",["6.0"] , None),
            ("""print(9 / 3  - 1)""",["2.0"] , None), 
            ("""print(6 / 3  - 2 )""",["0.0"] , None),
            ("""print(9 / 3  * -2 )""",["-6.0"] , None),
        ]
        for code, expected_result, expected_error in test_Cases_success:
            result , error = run(code,"test.hope")
            print(code)
            for idx in range(len(expected_result) if expected_result != None else 0):
         
                value_result  = result.elements[idx].value
                expected_value_result = expected_result[idx]

                self.assertEqual(value_result,expected_value_result)

            if error is not None:
                self.assertTrue(isinstance(error,expected_error))
            else:
                self.assertEqual(error,expected_error)
           



