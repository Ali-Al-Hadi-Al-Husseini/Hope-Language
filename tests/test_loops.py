import unittest

from Hope import *
from Hope import List,String,Number

from pythonfy import matches,convert_from_hope_to_python_objects

class TestLoops(unittest.TestCase):

    def test_loops(self):
        test_Cases = [
            ("""for i= 1 -> 5 >> print(i)""",[['1', '2' ,'3', '4']] , None),
            ("""for i= 1 -> 5 >> let a = i """,[[1, 2, 3, 4]] , None),
            ("""for i= 1 -- 5 >> print(i) """, None , InvalidSyntaxErorr)  ,
            ("""let i = 0
                while i < 5 >> i +=  1
                print(i)
                """,[0,[1,2,3,4,5], "5"] , None),
            ("""let i = 0
                while i < 10 >> 
                    i +=  1
                    if i == 5  >> break
                <<
                print(i)
                """,[0, 0,"5"] , None),
            ("""let counter = 0
                for i = 0 -> 10 >>
                    if i == 5 | i == 7 >> continue
                    counter += 1
                <<
                print(counter)
                """,[0,0,"8"] , None),
            ("""let i=0
                while i < 5 >>
                    print(i) 
                    i = 1 + i 
                <<
                print(i == 4)
                """,  [0, 0,"0"] , None),

        ]

        for code, expected_result, expected_error in test_Cases:
            result , error = run(code,"test.hope")

            self.assertTrue(matches(result,expected_result))            

            if error is not None:
                self.assertTrue(isinstance(error,expected_error))
            else:
                self.assertEqual(error,expected_error)
           


if __name__ == '__main__':
    unittest.main()
