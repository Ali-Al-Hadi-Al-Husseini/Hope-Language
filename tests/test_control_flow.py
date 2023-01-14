import unittest

from .Hope import *
from .Hope import List,String,Number

from .pythonfy import convert_from_hope_to_python_objects

class TestControlFlow(unittest.TestCase):

    def test_control_flow(self):
        test_Cases = [
            ("""if true >> print('i')""",['i'] , None),
            ("""if false >> print(1)""", [0] , None),
            ("""if true >> print(1)""", ['1'] , None),
            (""" let a = 2 
                if a < 2 >> 
                    print('hello')
                elif a == 2 >> 
                    print('world')
                else >>
                    print('!')
                <<
                """,[2,0],None)

        ]

        for code, expected_result, expected_error in test_Cases:
            result , error = run(code,"test.hope")
            result = convert_from_hope_to_python_objects(result)
            
            self.assertEqual(result,expected_result)
            self.assertEqual(error,expected_error)
           


if __name__ == '__main__':
    unittest.main()
