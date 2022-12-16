import unittest
from .hope import run,InvalidSyntaxErorr, List

class TestVariables(unittest.TestCase):

    def test_variables(self):
        test_Cases = [
            ("""for i= 1 -> 5 >> print(i)""",[['1', "2", "3", "4"]] , None),
            ("""let i = 0; while i < 10 >>; print(i); i = i + 1 ;<< ; print(i)""",[0, 0, "10"] , None),
            ("""for i= 1 -- 5 >> print(i) """, None , InvalidSyntaxErorr)  ,
            ("""let i=0; while i < 5 >> ; print(i) ; i = 1 + i ;<< ; print(i == 4)""",  [0, 0,"0"] , None),
        ]

        for code, expected_result, expected_error in test_Cases:
            result , error = run(code,"test.hope")
            
            for idx in range(len(expected_result) if expected_result != None else 0):
                
                if isinstance(result.elements[idx],List):
                    value_result  = result.elements[idx].elements 
                    expected_value_result = expected_result[idx]

                    for idx, value in enumerate(value_result):
                        self.assertEqual(value.value,expected_value_result[idx])
                else:
                    value_result  = result.elements[idx]
                    expected_value_result = expected_result[idx]                    
                    self.assertEqual(value_result.value,expected_value_result)

            if error is not None:
                self.assertTrue(isinstance(error,expected_error))
            else:
                self.assertEqual(error,expected_error)
           


if __name__ == '__main__':
    unittest.main()
