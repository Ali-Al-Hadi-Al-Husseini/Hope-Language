import unittest
from .hope import run,InvalidSyntaxErorr, List

class TestVariables(unittest.TestCase):

    def test_variables(self):
        test_Cases = [
            (""" func add(a,b) >>  a + b

                let z = add(1,2)   
                """,3,None),
            ("""let add =  func (a,b) >>  a + b

                let z = add(1,2)   
                """,3,None),
            ("""let add =  func (a,b) >> 
                return a + b
                <<
                let z = add(1,2)   
                """,3,None),
            ("""func add (a,b) >> 

                    if a > b >>
                        return a+b + 1 
                    else >> 
                        return a + b -1
                    <<
                <<
                let z = add(1,2)   
                """,2,None),
        ]

        for code, expected_result, expected_error in test_Cases:
            result , error = run(code,"test.hope")
            
            self.assertEqual(result.elements[1].value,expected_result)
            self.assertEqual(error,expected_error)
           


if __name__ == '__main__':
    unittest.main()
