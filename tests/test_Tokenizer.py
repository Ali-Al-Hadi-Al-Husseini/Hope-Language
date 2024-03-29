import unittest

from .lang import *


class TestTokenizer(unittest.TestCase):
    def setUp(self) -> None:
        self.tokenizer_test_cases_success = [
                ('(2+1)', ['LPAREN', 'INTEGER:2', 'PLUS', 'INTEGER:1', 'RPAREN', 'EOF']),
                ('(-2+1)', ['LPAREN', 'MINUS', 'INTEGER:2', 'PLUS', 'INTEGER:1', 'RPAREN', 'EOF']),
                ('(7 * 2)', ['LPAREN', 'INTEGER:7', 'MUL', 'INTEGER:2', 'RPAREN', 'EOF']),
                ('(7 * 3)', ['LPAREN', 'INTEGER:7', 'MUL', 'INTEGER:3', 'RPAREN', 'EOF']),
                ('(3 / 3)', ['LPAREN', 'INTEGER:3', 'DIV', 'INTEGER:3', 'RPAREN', 'EOF']),
                ('(9 / 3 )', ['LPAREN', 'INTEGER:9', 'DIV', 'INTEGER:3', 'RPAREN', 'EOF']),
                ('(9 / 3  + 1)', ['LPAREN', 'INTEGER:9', 'DIV', 'INTEGER:3', 'PLUS', 'INTEGER:1', 'RPAREN', 'EOF']),
                ('(6 / 3  + 2 )', ['LPAREN', 'INTEGER:6', 'DIV', 'INTEGER:3', 'PLUS', 'INTEGER:2', 'RPAREN', 'EOF']),
                ('(9 / 3  * 2 )', ['LPAREN', 'INTEGER:9', 'DIV', 'INTEGER:3', 'MUL', 'INTEGER:2', 'RPAREN', 'EOF']),
                ('(9 / 3  - 1)', ['LPAREN', 'INTEGER:9', 'DIV', 'INTEGER:3', 'MINUS', 'INTEGER:1', 'RPAREN', 'EOF']),
                ('(6 / 3  - 2 )', ['LPAREN', 'INTEGER:6', 'DIV', 'INTEGER:3', 'MINUS', 'INTEGER:2', 'RPAREN', 'EOF']),
                ('(9 / 3  * -2 )', ['LPAREN', 'INTEGER:9', 'DIV', 'INTEGER:3', 'MUL', 'MINUS', 'INTEGER:2', 'RPAREN', 'EOF']),
                ('((9 / 3)  * 0 )', ['LPAREN', 'LPAREN', 'INTEGER:9', 'DIV', 'INTEGER:3', 'RPAREN', 'MUL', 'INTEGER', 'RPAREN', 'EOF']),
                ('((9 / 3) / 0 )', ['LPAREN', 'LPAREN', 'INTEGER:9', 'DIV', 'INTEGER:3', 'RPAREN', 'DIV', 'INTEGER', 'RPAREN', 'EOF']),
                (" 'abc' * 'xyz ", ['STRING:abc', 'MUL', 'STRING:xyz ', 'EOF']),
                ("if true >> print('i')", ['KEYWORD:if', 'IDENTIFIER:true', 'UNTIL', 'IDENTIFIER:print', 'LPAREN', 'STRING:i', 'RPAREN', 'EOF']),
                ('if false >> print(1)', ['KEYWORD:if', 'IDENTIFIER:false', 'UNTIL', 'IDENTIFIER:print', 'LPAREN', 'INTEGER:1', 'RPAREN', 'EOF']),
                ('if true >> print(1)', ['KEYWORD:if', 'IDENTIFIER:true', 'UNTIL', 'IDENTIFIER:print', 'LPAREN', 'INTEGER:1', 'RPAREN', 'EOF']),
                (" let a = 2 \n        if a < 2 >> \n            print('hello')\n        elif a == 2 >> \n            print('world')\n        else >>\n            print('!')\n        <<\n        ", ['KEYWORD:let', 'IDENTIFIER:a', 'EQ', 'INTEGER:2', 'NEWLINE', 'KEYWORD:if', 'IDENTIFIER:a', 'LT', 'INTEGER:2', 'UNTIL', 'NEWLINE', 'IDENTIFIER:print', 'LPAREN', 'STRING:hello', 'RPAREN', 'NEWLINE', 'KEYWORD:elif', 'IDENTIFIER:a', 'EE', 'INTEGER:2', 'UNTIL', 'NEWLINE', 'IDENTIFIER:print', 'LPAREN', 'STRING:world', 'RPAREN', 'NEWLINE', 'KEYWORD:else', 'UNTIL', 'NEWLINE', 'IDENTIFIER:print', 'LPAREN', 'STRING:!', 'RPAREN', 'NEWLINE', 'SKIP', 'NEWLINE', 'EOF']),
                (' func add(a,b) >>  a + b\n        let z = add(1,2)   \n        ', ['KEYWORD:func', 'IDENTIFIER:add', 'LPAREN', 'IDENTIFIER:a', ' COMMA', 'IDENTIFIER:b', 'RPAREN', 'UNTIL', 'IDENTIFIER:a', 'PLUS', 'IDENTIFIER:b', 'NEWLINE', 'KEYWORD:let', 'IDENTIFIER:z', 'EQ', 'IDENTIFIER:add', 'LPAREN', 'INTEGER:1', ' COMMA', 'INTEGER:2', 'RPAREN', 'NEWLINE', 'EOF']),
                ('let add =  func (a,b) >>  a + b\n        let z = add(1,2)   \n        ', ['KEYWORD:let', 'IDENTIFIER:add', 'EQ', 'KEYWORD:func', 'LPAREN', 'IDENTIFIER:a', ' COMMA', 'IDENTIFIER:b', 'RPAREN', 'UNTIL', 'IDENTIFIER:a', 'PLUS', 'IDENTIFIER:b', 'NEWLINE', 'KEYWORD:let', 'IDENTIFIER:z', 'EQ', 'IDENTIFIER:add', 'LPAREN', 'INTEGER:1', ' COMMA', 'INTEGER:2', 'RPAREN', 'NEWLINE', 'EOF']),
                ('let add =  func (a,b) >> \n        return a + b\n        <<\n        let z = add(1,2)   \n        ', ['KEYWORD:let', 'IDENTIFIER:add', 'EQ', 'KEYWORD:func', 'LPAREN', 'IDENTIFIER:a', ' COMMA', 'IDENTIFIER:b', 'RPAREN', 'UNTIL', 'NEWLINE', 'KEYWORD:return', 'IDENTIFIER:a', 'PLUS', 'IDENTIFIER:b', 'NEWLINE', 'SKIP', 'NEWLINE', 'KEYWORD:let', 'IDENTIFIER:z', 'EQ', 'IDENTIFIER:add', 'LPAREN', 'INTEGER:1', ' COMMA', 'INTEGER:2', 'RPAREN', 'NEWLINE', 'EOF']),
                ('func add (a,b) >> \n\n            if a > b >>\n                return a+b + 1 \n         else >> \n                return a + b -1\n            <<\n        <<\n        let z = add(1,2)   \n        ', ['KEYWORD:func', 'IDENTIFIER:add', 'LPAREN', 'IDENTIFIER:a', ' COMMA', 'IDENTIFIER:b', 'RPAREN', 'UNTIL', 'NEWLINE', 'KEYWORD:if', 'IDENTIFIER:a', 'GT', 'IDENTIFIER:b', 'UNTIL', 'NEWLINE', 'KEYWORD:return', 'IDENTIFIER:a', 'PLUS', 'IDENTIFIER:b', 'PLUS', 'INTEGER:1', 'NEWLINE', 'KEYWORD:else', 'UNTIL', 'NEWLINE', 'KEYWORD:return', 'IDENTIFIER:a', 'PLUS', 'IDENTIFIER:b', 'MINUS', 'INTEGER:1', 'NEWLINE', 'SKIP', 'NEWLINE', 'SKIP', 'NEWLINE', 'KEYWORD:let', 'IDENTIFIER:z', 'EQ', 'IDENTIFIER:add', 'LPAREN', 'INTEGER:1', ' COMMA', 'INTEGER:2', 'RPAREN', 'NEWLINE', 'EOF']),
                ('for i= 1 -> 5 >> print(i)', ['KEYWORD:for', 'IDENTIFIER:i', 'EQ', 'INTEGER:1', 'ARROW', 'INTEGER:5', 'UNTIL', 'IDENTIFIER:print', 'LPAREN', 'IDENTIFIER:i', 'RPAREN', 'EOF']),
                ('for i= 1 -> 5 >> let a = i ', ['KEYWORD:for', 'IDENTIFIER:i', 'EQ', 'INTEGER:1', 'ARROW', 'INTEGER:5', 'UNTIL', 'KEYWORD:let', 'IDENTIFIER:a', 'EQ', 'IDENTIFIER:i', 'EOF']),
                ('for i= 1 -- 5 >> print(i) ', ['KEYWORD:for', 'IDENTIFIER:i', 'EQ', 'INTEGER:1', 'MINUS', 'MINUS', 'INTEGER:5', 'UNTIL', 'IDENTIFIER:print', 'LPAREN', 'IDENTIFIER:i', 'RPAREN', 'EOF']),
                ('let i = 0\n        while i < 5 >> i +=  1\n        print(i)\n        ', ['KEYWORD:let', 'IDENTIFIER:i', 'EQ', 'INTEGER', 'NEWLINE', 'KEYWORD:while', 'IDENTIFIER:i', 'LT', 'INTEGER:5', 'UNTIL', 'IDENTIFIER:i', 'EQ', 'IDENTIFIER:i', 'PLUS', 'INTEGER:1', 'NEWLINE', 'IDENTIFIER:print', 'LPAREN', 'IDENTIFIER:i', 'RPAREN', 'NEWLINE', 'EOF']),
                ('let i = 0\n        while i < 10 >> \n            i +=  1\n            if i == 5  >> break\n        <<\n        print(i)\n        ', ['KEYWORD:let', 'IDENTIFIER:i', 'EQ', 'INTEGER', 'NEWLINE', 'KEYWORD:while', 'IDENTIFIER:i', 'LT', 'INTEGER:10', 'UNTIL', 'NEWLINE', 'IDENTIFIER:i', 'EQ', 'IDENTIFIER:i', 'PLUS', 'INTEGER:1', 'NEWLINE', 'KEYWORD:if', 'IDENTIFIER:i', 'EE', 'INTEGER:5', 'UNTIL', 'KEYWORD:break', 'NEWLINE', 'SKIP', 'NEWLINE', 'IDENTIFIER:print', 'LPAREN', 'IDENTIFIER:i', 'RPAREN', 'NEWLINE', 'EOF']),
                ('let counter = 0\n        for i = 0 -> 10 >>\n            if i == 5 | i == 7 >> continue\n            counter += 1\n        <<\n        print(counter)\n        ', ['KEYWORD:let', 'IDENTIFIER:counter', 'EQ', 'INTEGER', 'NEWLINE', 'KEYWORD:for', 'IDENTIFIER:i', 'EQ', 'INTEGER', 'ARROW', 'INTEGER:10', 'UNTIL', 'NEWLINE', 'KEYWORD:if', 'IDENTIFIER:i', 'EE', 'INTEGER:5', 'KEYWORD:or', 'IDENTIFIER:i', 'EE', 'INTEGER:7', 'UNTIL', 'KEYWORD:continue', 'NEWLINE', 'IDENTIFIER:counter', 'EQ', 'IDENTIFIER:counter', 'PLUS', 'INTEGER:1', 'NEWLINE', 'SKIP', 'NEWLINE', 'IDENTIFIER:print', 'LPAREN', 'IDENTIFIER:counter', 'RPAREN', 'NEWLINE', 'EOF']),
                ('let i=0\n        while i < 5 >>\n            print(i) \n            i = 1 + i \n        <<\n        print(i == 4)\n        ', ['KEYWORD:let', 'IDENTIFIER:i', 'EQ', 'INTEGER', 'NEWLINE', 'KEYWORD:while', 'IDENTIFIER:i', 'LT', 'INTEGER:5', 'UNTIL', 'NEWLINE', 'IDENTIFIER:print', 'LPAREN', 'IDENTIFIER:i', 'RPAREN', 'NEWLINE', 'IDENTIFIER:i', 'EQ', 'INTEGER:1', 'PLUS', 'IDENTIFIER:i', 'NEWLINE', 'SKIP', 'NEWLINE', 'IDENTIFIER:print', 'LPAREN', 'IDENTIFIER:i', 'EE', 'INTEGER:4', 'RPAREN', 'NEWLINE', 'EOF']),
                ('let x = 0; print(x+1)', ['KEYWORD:let', 'IDENTIFIER:x', 'EQ', 'INTEGER', 'NEWLINE', 'IDENTIFIER:print', 'LPAREN', 'IDENTIFIER:x', 'PLUS', 'INTEGER:1', 'RPAREN', 'EOF']),
                ('let x = "test_case"; print(x + " hello")', ['KEYWORD:let', 'IDENTIFIER:x', 'EQ', 'STRING:test_case', 'NEWLINE', 'IDENTIFIER:print', 'LPAREN', 'IDENTIFIER:x', 'PLUS', 'STRING: hello', 'RPAREN', 'EOF']),
                ('let x = 17; print(x*2 + 7 / 3 - 8)', ['KEYWORD:let', 'IDENTIFIER:x', 'EQ', 'INTEGER:17', 'NEWLINE', 'IDENTIFIER:print', 'LPAREN', 'IDENTIFIER:x', 'MUL', 'INTEGER:2', 'PLUS', 'INTEGER:7', 'DIV', 'INTEGER:3', 'MINUS', 'INTEGER:8', 'RPAREN', 'EOF'])]

    def test_tokenizer(self):
        
        for code ,expected_result in self.tokenizer_test_cases_success:
            tokenizer = Tokenizer(code, "temp")

            tokens, error = tokenizer.make_tokens()    
            self.assertEqual(error, None)
            self.assertEqual(expected_result,[str(tok) for tok in tokens])


if __name__ == "__main__":
    unittest.main()

