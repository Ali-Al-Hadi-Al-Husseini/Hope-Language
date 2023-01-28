import unittest

from .lang import *
from .lang import List,String,Number
from .pythonfy import matches

class TestVariables(unittest.TestCase):

    def test_variables(self):
        test_Cases_success = [
            ("""let x = 0; print(x+1)""",[0,"1"] , None),
            ("""let x = "test_case"; print(x + " hello")""",["test_case",'test_case hello'] , None),
            ("""let x = 17; print(x*2 + 7 / 3 - 8)""", [17, "28.333333333333336"], None),
            ("""let a = 18; a += 1 ; print(a)""",[18,19,'19'],None),
            ("""let a = 18; a *= 1 ; print(a)""",[18,18,'18'],None),
            ("""let a = 18; a *= 2 ; print(a)""",[18,36,'36'],None),
            ("""let a = 18; a /= 2 ; print(a)""",[18,9.0,'9.0'],None),
            ("""let a = 18; a -= 2 ; print(a)""",[18,16,'16'],None),
            ("""let a = "hello"; a *= 2 ; print(a)""",['hello',"hellohello",'hellohello'],None),

            ("""let x = abc; print(x+1)""" ,[], RunTimeError),
            ("""abc = x ;""" ,[], InvalidSyntaxErorr),
            ("""x = abc; print(x+1)""" ,[], RunTimeError),
            ("""let x = 1; print(abc+1)""" ,[], RunTimeError)    
        ]
        for code, expected_result, expected_error in test_Cases_success:
            result , error = run(code,"test.hope")

            self.assertTrue(matches(result,expected_result))

            if error:
                print(error)
                self.assertTrue(isinstance(error,expected_error))
            else:
                self.assertEqual(error,expected_error)



if __name__ == '__main__':
    unittest.main()