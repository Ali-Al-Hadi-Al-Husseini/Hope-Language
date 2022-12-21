from .Token import Token
from .Position import Position

from .tokens import *
from Errors_tools.Errors import *

from typing import List,Tuple,Optional

class Tokenizer:
    def __init__(self, text: str, fn: str) -> None:
        self.fn = fn #filename
        self.text = text
        self.position = Position(-1, 0, -1, fn, text)
        self.current_character = None
        self.globals = globals()
        self.advance()

    def advance(self,adance_char=True) -> None:
        self.position.advance(self.current_character )
        if adance_char:
            self.current_character = self.text[self.position.idx] if self.position.idx < len(
                self.text) else None

    # this method takes the text and converts it into tokens by comparing the current char with possible token 
    def make_tokens(self) -> Tuple[ Optional[List[Token]], Optional[Error]]:
        tokens = []
        # using dictionary or switch cases is faster then using if-elif-else
        while self.current_character != None:

            if self.current_character in ' \t':
                self.advance()

            elif self.current_character == '#':
                self.advance()

                while self.current_character != '\n' :
                    self.advance()
                self.advance()

            elif self.current_character in DIGITS:
                tokens.append(self.make_number())
            
            elif self.current_character in LETTERS:
                ident, error = self.make_identifier()
                if error : return error
                tokens.append(ident)

            elif self.current_character in ';\n':
                tokens.append(self.make_newline())
                
            elif self.current_character in ('"', "'"):
                tokens.append(self.make_str())

            elif self.current_character == '+':
                tokens.append(self.make_operation_and_equal(TOKEN_PLUS,tokens))

            elif self.current_character  == "&":
                tokens.append(self.make_identifier(symbol_found =True))

            elif self.current_character == '|':
                tokens.append(self.make_identifier(symbol_found =True))           
            
            elif self.current_character == '-':
                tokens.append(self.make_arrow_or_minus(tokens))

            elif self.current_character == '*':
                tokens.append(self.make_operation_and_equal(TOKEN_MUL,tokens))

            elif self.current_character == "%":
                tokens.append(self.make_operation_and_equal(TOKEN_MODULE,tokens))

            elif self.current_character == '!':
                token, error = self.make_not_equal()
                if error: return [], error
                tokens.append(token)
                self.advance()

            elif self.current_character == '/':
                tokens.append(self.make_operation_and_equal(TOKEN_DIV,tokens))
                
            elif self.current_character == '^':
                tokens.append(self.make_operation_and_equal(TOKEN_POW,tokens))

            elif self.current_character == '(':
                tokens.append(Token(TOKEN_LPAREN, start_position=self.position))
                self.advance()

            elif self.current_character == ')':
                tokens.append(Token(TOKEN_RPARENT, start_position=self.position))
                self.advance()
            elif self.current_character == '[':
                tokens.append(Token(TOKEN_LSQUARE,start_position=self.position))
                self.advance()

            elif self.current_character == ']':
                tokens.append(Token(TOKEN_RSQUARE, start_position=self.position))
                self.advance()

            elif self.current_character == ',':
                tokens.append(Token(TOKEN_COMMA, start_position=self.position))
                self.advance()


            elif self.current_character == '=':
                tokens.append(self.make_equal())
                

            elif self.current_character == '<':
                tokens.append(self.make_GT_LT())
                self.advance()

            elif self.current_character == '>':
                tokens.append(self.make_GT_LT())
                self.advance()

            elif self.current_character == '{':
                tokens.append(Token(TOKEN_LCURLY, start_position=self.position))
                self.advance()

            elif self.current_character == '}':
                tokens.append(Token(TOKEN_RCURLY, start_position=self.position))
                self.advance()


            else:
                start_position = self.position.copy()
                char = self.current_character
                self.advance()
                return [], IllegalCharError(start_position, self.position,"'" + char + "'")

        tokens.append(Token(TOKEN_EOF, start_position=self.position))
        return tokens, None

    def make_operation_and_equal(self,_type,Tokens, advance= True) -> Token:
        last_token = Tokens[-1]
        start_position = self.position
        if advance:
            self.advance()

        if self.current_character == '=':

            Tokens.append(Token(TOKEN_EQ,start_position=start_position))
            Tokens.append(Token(TOKEN_IDENTIFIER,last_token.value,start_position= start_position))
            self.advance()
            return Token(_type, start_position=self.position)
        
        return Token(_type, start_position=start_position)

    def make_newline(self) -> Token:
        token = Token(TOKEN_NEWLINE, start_position=self.position)
        self.advance()
        
        if self.current_character == None : return token

        while self.current_character in "\n;":
            self.advance()
            if self.current_character == None : return token

        return token 
    #checks weather a number is float or int and returns a token back with it's type
    def make_number(self) -> Token:
        num_str = ''
        dot_count = 0
        start_position = self.position.copy()

        while self.current_character != None and self.current_character in DIGITS or self.current_character ==  '.':
            if self.current_character == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'

            else:
                num_str += self.current_character
            self.advance()

        if dot_count == 0:
            return Token(TOKEN_INT, int(num_str),start_position, self.position)
        else:
            return Token(TOKEN_FLOAT, float(num_str), start_position, self.position)

    def make_identifier(self, symbol_found=False) -> Token:
        if symbol_found:
            symbols_table = {
                            '&': 'and',
                            '|' :'or'
            }
            start_position = self.position.copy()
            curr_symbol = symbols_table[self.current_character]
            self.advance()
            return Token(TOKEN_KEYWORD,curr_symbol,start_position,self.position)

        id_str = ''
        start_position = self.position.copy()

        while self.current_character != None and self.current_character in LETTER_DIGITS or self.current_character == '_':
            id_str += self.current_character
            self.advance()

        token_type = TOKEN_KEYWORD if id_str in KEYWORDS else TOKEN_IDENTIFIER  
        return Token(token_type,id_str,start_position,self.position), None
    

    def make_not_equal(self) ->  Tuple[Optional[Token],Optional[Error]]:
        start_position = self.position.copy()
        self.advance()

        if self.current_character == '=':
            return Token(TOKEN_NE,start_position=start_position,end_position=self.position), None

        return None, ExpectedCharError(start_position,self.position, "Expected '=' after '!' ") 
    
    def make_equal(self) -> Token:
        start_position = self.position.copy()
        self.advance()
        if self.current_character == "=":
            self.advance()
            return Token(TOKEN_EE,start_position=start_position,end_position=self.position)

        return Token(TOKEN_EQ,start_position=start_position,end_position=self.position)


    # a function  that checks if '>' or '<'  are followed by and equals sign '=' to change its type
    def make_GT_LT(self) -> Token:
        start_position = self.position.copy()
        Token_type = TOKEN_GT if self.current_character == ">" else TOKEN_LT
        self.advance()
        
        if self.current_character =='>' and Token_type == TOKEN_GT:
            return Token(TOKEN_START,start_position=start_position,end_position=self.position)

        if self.current_character =='<' and Token_type == TOKEN_LT:
            return Token(TOKEN_END,start_position=start_position,end_position=self.position)

        if self.current_character == '=':
            Token_type += 'E'
            self.advance()

        return Token(Token_type,start_position=start_position,end_position=self.position)

    def make_str(self) -> Token:
        skip = False
        start_position = self.position.copy()
        curr_quotes = self.current_character
        new_str    = ''
        skip_chars = {
                        'n':'\n',
                        't':'\t'
                    }
        self.advance()

        while (self.current_character != curr_quotes or skip) and self.current_character != None:
            if skip:
                new_str += skip_chars.get(self.current_character, self.current_character)
                skip = False
            else:
                if self.current_character == '\\':
                    skip = True
                else:
                    new_str += self.current_character
            self.advance()


        self.advance()
        return Token(TOKEN_STRING, new_str, start_position)
    
    def make_arrow_or_minus(self,tokens) -> Token:
        start_position = self.position.copy()
        self.advance()

        if self.current_character  == '>':
            self.advance()
            return Token(TOKEN_ARROW, start_position=start_position, end_position=self.position)

        else :
            return self.make_operation_and_equal(TOKEN_MINUS,tokens,False)

