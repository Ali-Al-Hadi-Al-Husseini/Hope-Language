import unittest
from hope import run,InvalidSyntaxErorr, List

class TestVariables(unittest.TestCase):

    def test_variables(self):
        test_Cases = [
            ("""if true >> print('i')""",'"i"' , None),
            ("""if false >> print(1)""", 0 , None),
            ("""if true >> print(1)""", '1' , None),
            (""" let a = 2 
                if a < 2 >> 
                    print('hello')
                elif a == 2 >> 
                    print('world')
                else >>
                    print('!')
                <<
                """,2,None)

        ]

        for code, expected_result, expected_error in test_Cases:
            result , error = run(code,"test.hope")
            
            self.assertEqual(result.elements[0].value,expected_result)
            self.assertEqual(error,expected_error)
           


if __name__ == '__main__':
    unittest.main()
