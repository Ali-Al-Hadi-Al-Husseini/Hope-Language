""" HOPE

"""
import string
import os
import sys


DIGITS           = '0123456789'
LETTERS          = string.ascii_letters # t
LETTER_DIGITS    = string.ascii_letters + DIGITS
TOKEN_STRING     = 'STRING'
TOKEN_INT        = 'TOKEN_INT'
TOKEN_FLOAT      = 'FLOAT'
TOKEN_PLUS       = 'PLUS' 
TOKEN_MINUS      = 'MINUS'
TOKEN_MUL        = 'MUL'
TOKEN_DIV        = 'DIV'
TOKEN_POW        = 'POW'# power token 
TOKEN_MODULE     =  'MOD'
TOKEN_LPAREN     = 'LPAREN'
TOKEN_RPARENT    = 'RPAREN'
TOKEN_EQ         = 'EQ' # equals token 
TOKEN_EE         = 'EE' # equals equals '==' token used in comparison operatores
TOKEN_GT         = 'GT' # greater then '>' operator token
TOKEN_NE         = 'NE' # not equals then '!=' operator token
TOKEN_LT         = 'LT' # less then '<' operator token
TOKEN_GTE        = 'GTE' # greater then  or equal '>=' operator token
TOKEN_LTE        = 'LTE' # less then or equals '<=' operator token
TOKEN_KEYWORD    = 'KEYWORD' # keyword that are used by the language 
TOKEN_IDENTIFIER = 'IDENTIFIER' # names that are given by the user to name variables, fucntions ...
TOKEN_EOF        = 'EOF'
TOKEN_COMMA      = ' COMMA'
TOKEN_LCURLY     = 'LCURLY'
TOKEN_RCURLY     = 'RCURLY'
TOKEN_LSQUARE    = 'LSQUARE'
TOKEN_RSQUARE    = 'RSQUARE'
TOKEN_START      = 'UNTIL'
TOKEN_END        = 'SKIP'
TOKEN_ARROW      = 'ARROW'
TOKEN_QUOTES     = '"'
TOKEN_ANDSYMBOL  = "ANDSYMBOL"
TOKEN_ORSYMBOL   = "ORSYMBOL"
TOKEN_PYTHON     = 'PYTHON'
TOKEN_NEWLINE    = 'NEWLINE'

KEYWORDS = [ 
    'let',
    'and',
    'or',
    'not',
    'if',
    'elif',
    'else',
    'while',
    'for', 
    'func',
    'PYTHON',
    'return',
    'break',
    'continue',
    'skip',
    'run'
]

# this class is made for other claases to inherit from 
class Error:
    def __init__(self, start_pos: int, end_pos: int, error_name: str, details: str) -> None:
        self.error_name = error_name # gives the type of the error if it is syntax error  Illegal Char Error etc..
        self.details = details # what wrong with code it is like a description
        self.start_pos = start_pos
        self.end_pos = end_pos

    def as_string(self):
        result =  str(f'{self.error_name}: {self.details} \n File {self.start_pos.fn}, line {self.start_pos.line + 1}')
        result += '\n\n' + string_with_arrows(self.start_pos.ftxt, self.start_pos, self.end_pos)
        return result

class IllegalCharError(Error):
    def __init__(self,start_pos :int, end_pos: int, details='') -> None:
        super().__init__(start_pos, end_pos, 'Illegal Character', details)

class InvalidSyntaxErorr(Error):
    def __init__(self, start_pos: int, end_pos: int, details= '') -> None:
        super().__init__(start_pos, end_pos, "Invalid Syntax", details)

class Indexerror(Error):
    def __init__(self, start_pos: int, end_pos: int, details= '') -> None:
        super().__init__(start_pos, end_pos, "Invalid index", details)


class RunTimeError(Error):
    def __init__(self, start_pos: int, end_pos: int, details,context) -> None:
        super().__init__(start_pos, end_pos, "Runtime Error", details)
        self.context = context

    def as_string(self):
        result =  str(f'{self.error_name}: {self.details} \n File {self.start_pos.fn}, line {self.start_pos.line + 1}')
        result += '\n\n' + string_with_arrows(self.start_pos.ftxt, self.start_pos, self.end_pos)
        return result

class ExpectedCharError(Error):
    def __init__(self, start_pos: int, end_pos: int, error_name: str, details: str) -> None:
        super().__init__(start_pos, end_pos, error_name, details)

    def as_string(self):
        result = self.generate_traceback()
        result +=  str(f'{self.error_name}: {self.details}')
        result += '\n\n' + string_with_arrows(self.start_pos.ftxt, self.start_pos, self.end_pos)

        return result

    def generate_traceback(self):
        result = ''
        pos = self.start_pos
        ctx = self.context

        while ctx:
            result = str(f'  File {pos.fn}, line {str(pos.line + 1)}, in {ctx.display_name}\n') + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return 'Traceback (most recent call last):\n' + result


# this class tracks the postion of a token to display where is the error if ther any 
class Position:
    def __init__(self, idx: int, line: int, col: int, fn: str, ftxt: str) -> None:
        self.idx = idx
        self.line = line
        self.col = col
        self.fn = fn    # file name
        self.ftxt = ftxt # file text
        
    
    def advance(self, current_char=None):
        # inceases the position by one
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.line += 1
            self.col = 0
        return self

    def copy(self):
        return Position(self.idx, self.line, self.col,self.fn,self.ftxt)


# relates the type (from the token types defined above )of a token with it value a 
class Token():
    def __init__(self, _type: str, value=None, start_pos=None, end_pos=None) -> None:
        self.type = _type
        self.value = value

        if start_pos:
            self.start_pos = start_pos.copy()
            self.end_pos = start_pos.copy()
            self.end_pos.advance()

        if end_pos:
            self.end_pos = end_pos

    def __repr__(self) -> str:
        if self.value:
            return "{}:{}".format(self.type, self.value)
        return str(f'{self.type}')

    def matches(self, _type, value):
        return self.type == _type and self.value == value


# takes raw string input and outputs a list of all token created from the given text/str
class Tokenizer:
    def __init__(self, text: str, fn: str) -> None:
        self.fn = fn #filename
        self.text = text
        self.position = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.position.advance(self.current_char )
        self.current_char = self.text[self.position.idx] if self.position.idx < len(
            self.text) else None

    # this method takes the text and converts it into tokens by comparing the current char with possible token 
    def make_tokens(self):
        tokens = []

        while self.current_char != None:

            if self.current_char in ' \t':
                self.advance()

            elif self.current_char == '#':
                self.advance()

                while self.current_char != '\n' :
                    self.advance()
                self.advance()

            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            
            elif self.current_char in LETTERS:
                ident, error = self.make_identifier()
                if error : return error
                tokens.append(ident)

            elif self.current_char in ';\n':
                tokens.append(self.make_newline())
                #self.advance()
                
            elif self.current_char in ('"', "'"):
                tokens.append(self.make_str())

            elif self.current_char == '+':
                tokens.append(Token(TOKEN_PLUS, start_pos=self.position))
                self.advance()

            elif self.current_char  == "&":
                tokens.append(self.make_identifier(symbol_found =True))

            elif self.current_char == '|':
                tokens.append(self.make_identifier(symbol_found =True))           
            
            elif self.current_char == '-':
                tokens.append(self.make_arrow())
                

            elif self.current_char == '*':
                tokens.append(Token(TOKEN_MUL, start_pos=self.position))
                self.advance()
            
            elif self.current_char == "%":
                tokens.append(Token(TOKEN_MODULE,start_pos=self.position))
                self.advance()

            elif self.current_char == '!':
                token, error = self.make_not_equal()
                if error: return [], error
                tokens.append(token)
                self.advance()

            elif self.current_char == '/':
                tokens.append(Token(TOKEN_DIV, start_pos=self.position))
                self.advance()
                
            elif self.current_char == '^':
                tokens.append(Token(TOKEN_POW, start_pos=self.position))
                self.advance()

            elif self.current_char == '(':
                tokens.append(Token(TOKEN_LPAREN, start_pos=self.position))
                self.advance()

            elif self.current_char == ')':
                tokens.append(Token(TOKEN_RPARENT, start_pos=self.position))
                self.advance()
            elif self.current_char == '[':
                tokens.append(Token(TOKEN_LSQUARE,start_pos=self.position))
                self.advance()

            elif self.current_char == ']':
                tokens.append(Token(TOKEN_RSQUARE, start_pos=self.position))
                self.advance()

            elif self.current_char == ',':
                tokens.append(Token(TOKEN_COMMA, start_pos=self.position))
                self.advance()


            elif self.current_char == '=':
                tokens.append(self.make_equal())
                

            elif self.current_char == '<':
                tokens.append(self.make_GT_LT())
                self.advance()

            elif self.current_char == '>':
                tokens.append(self.make_GT_LT())
                self.advance()

            elif self.current_char == '{':
                tokens.append(Token(TOKEN_LCURLY, start_pos=self.position))
                self.advance()

            elif self.current_char == '}':
                tokens.append(Token(TOKEN_RCURLY, start_pos=self.position))
                self.advance()


            else:
                start_pos = self.position.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(start_pos, self.position,"'" + char + "'")

        tokens.append(Token(TOKEN_EOF, start_pos=self.position))
        return tokens, None

    def make_newline(self):
        tok = Token(TOKEN_NEWLINE, start_pos=self.position)
        self.advance()
        
        if self.current_char == None : return tok

        while self.current_char in "\n;":
            self.advance()
            if self.current_char == None : return tok

        return tok 
    #checks weather a number is float or int and returns a token back with it's type
    def make_number(self):
        num_str = ''
        dot_count = 0
        start_pos = self.position.copy()

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'

            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TOKEN_INT, int(num_str),start_pos, self.position)
        else:
            return Token(TOKEN_FLOAT, float(num_str), start_pos, self.position)

    def make_identifier(self, symbol_found=False):
        if symbol_found:
            symbols_table = {
                            '&': 'and',
                            '|' :'or'
            }
            start_pos = self.position.copy()
            curr_symbol = symbols_table[self.current_char]
            self.advance()
            return Token(TOKEN_KEYWORD,curr_symbol,start_pos,self.position)

        id_str = ''
        start_pos = self.position.copy()

        while self.current_char != None and self.current_char in LETTER_DIGITS + '_':
            id_str += self.current_char
            self.advance()

        token_type = TOKEN_KEYWORD if id_str in KEYWORDS else TOKEN_IDENTIFIER  
        return Token(token_type,id_str,start_pos,self.position), None
    



    def make_not_equal(self):
        start_pos = self.position.copy()
        self.advance()

        if self.current_char == '=':
            return Token(TOKEN_NE,start_pos=start_pos,end_pos=self.position), None

        return None, ExpectedCharError(start_pos,self.position, "Expected '=' after '!' ") 
    
    def make_equal(self):
        start_pos = self.position.copy()
        self.advance()
        if self.current_char == "=":
            self.advance()
            return Token(TOKEN_EE,start_pos=start_pos,end_pos=self.position)

        return Token(TOKEN_EQ,start_pos=start_pos,end_pos=self.position)


    # a function  that checks if '>' or '<'  are followed by and equals sign '=' to change its type
    def make_GT_LT(self):
        start_pos = self.position.copy()
        Token_type = TOKEN_GT if self.current_char == ">" else TOKEN_LT
        self.advance()
        
        if self.current_char =='>' and Token_type == TOKEN_GT:
            return Token(TOKEN_START,start_pos=start_pos,end_pos=self.position)

        if self.current_char =='<' and Token_type == TOKEN_LT:
            return Token(TOKEN_END,start_pos=start_pos,end_pos=self.position)

        if self.current_char == '=':
            Token_type += 'E'
            self.advance()

        return Token(Token_type,start_pos=start_pos,end_pos=self.position)

    def make_str(self):
        skip = False
        start_pos = self.position.copy()
        curr_quotes = self.current_char
        new_str    = ''
        skip_chars = {
                        'n':'\n',
                        't':'\t'
                    }
        self.advance()

        while (self.current_char != curr_quotes or skip) and self.current_char != None:
            if skip:
                new_str += skip_chars.get(self.current_char, self.current_char)
                skip = False
            else:
                if self.current_char == '\\':
                    skip = True
                else:
                    new_str += self.current_char
            self.advance()


        self.advance()
        return Token(TOKEN_STRING, new_str, start_pos)
    
    def make_arrow(self):
        start_pos = self.position.copy()
        self.advance()

        if self.current_char  == '>':
            return Token(TOKEN_ARROW, start_pos=start_pos, end_pos=self.position)
        else :
            return Token(TOKEN_MINUS,start_pos = start_pos)



# nodes
class StringNode:
    def __init__(self,token : Token) -> None:
        self.token = token
        self.start_pos = token.start_pos
        self.end_pos = token.end_pos

    def __repr__(self) -> str:
        return str(f'{self.token}')

class NumberNode:
    def __init__(self,token : Token) -> None:
        self.token = token
        self.start_pos = token.start_pos
        self.end_pos = token.end_pos

    def __repr__(self) -> str:
        return str(f'{self.token}')

class ListNode:
    def __init__(self,elements_nodes,start_pos,end_pos):
        self.elements_nodes = elements_nodes
        self.start_pos = start_pos
        self.end_pos  = end_pos

class ListacssesNode:
    def __init__(self, ident, index, start_pos,end_pos):
        self.ident = ident
        self.index = index
        self.start_pos = start_pos
        self.end_pos = end_pos


class unaryoperationNode:
    def __init__(self, operator_token , node) -> None:
        self.operation_token = operator_token
        self.node = node
        self.start_pos = operator_token.start_pos
        self.end_pos = node.end_pos

    def __repr__(self) -> str:
        return str(f'({self.operator_token}, {self.node})')

class BinOpertaionNode:
    def __init__(self, right_node, operation_token, left_node) -> None:
        self.operation_token = operation_token
        self.left_node = left_node
        self.right_node = right_node
        self.start_pos = left_node.start_pos
        self.end_pos = right_node.end_pos

    def __repr__(self) -> str:
        return str(f'( {self.left_node} {self.operation_token} {self.right_node} )')


class var_assign_node:
    def __init__(self, var_name_token, value_node,force =False) -> None:
        self.var_name_token = var_name_token
        self.value_node = value_node
        self.force = force

        self.start_pos = var_name_token.start_pos
        self.end_pos = var_name_token.end_pos       

class var_access_node:
    def __init__(self,var_token) -> None:
        self.var_name_token = var_token
        
        self.start_pos = var_token.start_pos
        self.end_pos = var_token.end_pos

class IfNode:
    def __init__(self,cases, else_case) -> None:
        self.cases = cases
        self.else_case = else_case

        self.start_pos = self.cases[0][0].start_pos
        self.end_pos = (self.else_case or self.cases[-1])[0].end_pos



class ForNode():
    def __init__(self, var_name, start_value, end_value, skip_value, body, should_return_null) -> None:
        self.start_value_node = start_value
        self.end_value_node   = end_value
        self.var_name_node    = var_name
        self.skip_value_node  = skip_value
        self.body_node        = body   
        self.should_return_null = should_return_null

        self.start_pos        = self.var_name_node.start_pos
        self.end_pos          = self.body_node.end_pos

class WhileNode():
    def __init__(self,condition, body,should_return_null) -> None:
        self.condition_node =  condition
        self.body_node      = body
        self.should_return_null = should_return_null

        self.start_pos        = self.condition_node.start_pos
        self.end_pos          = self.body_node.end_pos


class functionDefNode():
    def __init__(self, var_name_token, arg_name_tokens, body_node,should_return_null) -> None:
        self.arg_name_tokens = arg_name_tokens
        self.body_node =  body_node
        self.var_name_token = var_name_token
        self.should_return_null = should_return_null


        if self.var_name_token:
            self.start_pos = var_name_token.start_pos
        elif len(self.arg_name_tokens) > 0:
            self.start_pos = self.arg_name_tokens[0].start_pos
        else:
            self.start_pos = self.body_node.start_pos
        
        self.end_pos =  self.body_node.end_pos


class CallNode:
  def __init__(self, node_to_call, arg_nodes):
    self.node_to_call = node_to_call
    self.arg_nodes = arg_nodes

    self.start_pos = self.node_to_call.start_pos

    if len(self.arg_nodes) > 0:
      self.end_pos = self.arg_nodes[-1].end_pos
    else:
      self.end_pos = self.node_to_call.end_pos

class ReturnNode:
    def __init__(self,node_to_return, start_pos, end_pos ) -> None:
        self.node_to_return = node_to_return
        
        self.pos_start = start_pos
        self.end_pos = end_pos


class BreakNode:
    def __init__(self,start_pos,end_pos) -> None:
        self.pos_start = start_pos
        self.end_pos = end_pos

class ContinueNode:
    def __init__(self,start_pos, end_pos) -> None:
        self.pos_start = start_pos
        self.end_pos = end_pos

# nodes end
    
class ParserResult:
    def __init__(self) -> None:
        self.error = None
        self.node = None
        self.last_registered_Advance_count = 0
        self.to_reverse_count = 0
        self.advance_count = 0

    def Register_advancement(self):
        self.last_registered_Advance_count = 1
        self.advance_count += 1

    def Register(self,res):
        self.last_registered_Advance_count = res.advance_count
        self.advance_count += res.advance_count
        if  res.error:self.error = res.error
        return  res.node
        
    def Sucsses(self,node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error  or self.last_registered_Advance_count  == 0:
            self.error = error
        return self

    def try_Register(self, res):
        if  res.error:
            self.to_reverse_count = res.advance_count
            return None
        return self.Register(res)





    
# takes the list of token that are returned by the tokenizer and then atates at what order should those token be executed 
class Parser:
    def __init__(self,Tokens) -> None:
        self.tokens = Tokens
        self.tok_idx = - 1 
        self.curr_token = None
        self.advance()
    
    def advance(self):
        self.tok_idx += 1
        if self.tok_idx >= 0 and self.tok_idx < len(self.tokens):
            self.curr_token = self.tokens[self.tok_idx]

        return self.curr_token

    def reverse(self, amount=1):
        self.tok_idx  -= amount
        if self.tok_idx >= 0 and self.tok_idx < len(self.tokens):
            self.curr_token = self.tokens[self.tok_idx]

        return self.curr_token


    def parse(self,):
        res= self.statments()
        if  not res.error and self.curr_token.type != TOKEN_EOF:
            return res.failure(InvalidSyntaxErorr(
                self.curr_token.start_pos, self.curr_token.end_pos,
                "Expected  '+', '-', '*' , '/'  or any other operation"
            ))

        return res

    def statments(self):
        res = ParserResult()
        statments = []
        start_pos = self.curr_token.start_pos.copy()


        while self.curr_token.type  == TOKEN_NEWLINE:
            self.Register_advacement(res)

        stat = res.Register(self.statment())
        if  res.error: return res
        statments.append(stat)

        more_statments = True

        while True:
            new_line_count = 0
            while self.curr_token.type == TOKEN_NEWLINE:
                self.Register_advacement(res)
                new_line_count += 1
            
            if new_line_count == 0:
                more_statments = False

            if not more_statments:  break
            stat = res.try_Register(self.statment())
            if not stat:
                self.reverse(res.to_reverse_count)
                more_statments = False
                continue

            statments.append(stat)
        # self.Register_advacement(res)
        return res.Sucsses(
            ListNode(statments,
            start_pos,
            self.curr_token.end_pos.copy())
        )

    def statment(self):
        res = ParserResult()
        start_pos = self.curr_token.start_pos.copy()

        if self.curr_token.matches(TOKEN_KEYWORD, 'return'):
            self.Register_advacement(res)

            expression = res.try_Register(self.Expression())
            if not expression:
                self.reverse(res.to_reverse_count)
            return res.Sucsses(ReturnNode(expression, start_pos, self.curr_token.start_pos.copy()))
        
        if self.curr_token.matches(TOKEN_KEYWORD, 'continue'):
            self.Register_advacement(res)
            return res.Sucsses(ContinueNode(start_pos, self.curr_token.start_pos.copy()))

        if self.curr_token.matches(TOKEN_KEYWORD, 'break'):
            self.Register_advacement(res)
            return res.Sucsses(BreakNode(start_pos, self.curr_token.start_pos.copy())) 

        expression = res.Register(self.Expression())
        if  res.error:return res.failure(InvalidSyntaxErorr(start_pos,self.curr_token.start_pos.copy(),
         "Expected 'let', int, float, identifier, keyword,  '+', '-' or '(' "
        ))
        return res.Sucsses(expression)

    def call(self):
        res = ParserResult()
        most = res.Register(self.Most())
        if  res.error:return res

        if self.curr_token.type == TOKEN_LPAREN:
            self.Register_advacement(res)
            arg_nodes = []

            if self.curr_token.type == TOKEN_RPARENT:
                self.Register_advacement(res)
            else:
                arg_nodes.append(res.Register(self.Expression()))
                if  res.error:
                    return res.failure(InvalidSyntaxErorr(
                        self.curr_token.start_pos, self.curr_token.end_pos,
                        "Expected ')' , keyword, identifier, or values "
                    ))
                
                while self.curr_token.type == TOKEN_COMMA:
                    self.Register_advacement(res)

                    arg_nodes.append(res.Register(self.Expression()))
                    if  res.error: return res

                if self.curr_token.type != TOKEN_RPARENT:
                    return res.failure(InvalidSyntaxErorr(
                        self.curr_token.start_pos, self.curr_token.end_pos,
                        "Expected ',' or ')'"
                    ))

                self.Register_advacement(res)
            return res.Sucsses(CallNode(most,arg_nodes))
        return res.Sucsses(most)

# to understand the order of this reader grammers in the top of the file
    def Most(self):
        res = ParserResult()
        token = self.curr_token

        if token.type in (TOKEN_FLOAT , TOKEN_INT):
            self.Register_advacement(res)
            return res.Sucsses(NumberNode(token))

        elif token.type == TOKEN_STRING:
            self.Register_advacement(res)
            return res.Sucsses(StringNode(token))

        elif token.type is TOKEN_IDENTIFIER:
            self.Register_advacement(res)
            ident = token.value
            if self.curr_token.type == TOKEN_EQ:
                self.Register_advacement(res)
                new_value = res.Register(self.Expression())
                if  res.error:return res

                return res.Sucsses(var_assign_node(token,new_value))

            elif self.curr_token.type == TOKEN_LSQUARE:
                self.Register_advacement(res)
                if self.curr_token.type in (TOKEN_INT, TOKEN_IDENTIFIER):
                    index = self.curr_token
                    self.Register_advacement(res)

                    if self.curr_token.type != TOKEN_RSQUARE:
                        res.failure(InvalidSyntaxErorr(index.start_pos,index.end_pos,
                                                       f"Expected ']' after index {index.value}"))
                        return res
                    end_pos = self.curr_token.end_pos.copy()
                    self.Register_advacement(res)

                    return res.Sucsses(ListacssesNode(ident, index.value, token.start_pos.copy(), end_pos))
            return res.Sucsses(var_access_node(token))

        elif token.type == TOKEN_LPAREN:
            self.Register_advacement(res)
            expr = res.Register(self.Expression())
            if  res.error: return res

            if self.curr_token.type == TOKEN_RPARENT   :
                self.Register_advacement(res)
                return res.Sucsses(expr)
            else:
                return res.failure(InvalidSyntaxErorr(
                    self.curr_token.star_pos, self.curr_token.end_pos, 
                    "Expected ')' "
                ))

        elif token.type == TOKEN_LSQUARE:
            expression = res.Register(self.list_expression())
            if  res.error:return Error
            return res.Sucsses(expression)

        elif token.matches(TOKEN_KEYWORD, 'if'):
            expression = res.Register(self.If_expression())
            if  res.error: return res
            return res.Sucsses(expression)

        elif token.matches(TOKEN_KEYWORD, 'while'):
            expression = res.Register(self.While_expression())
            if  res.error: return res
            return res.Sucsses(expression)

        elif token.matches(TOKEN_KEYWORD, 'for'):
            expression = res.Register(self.For_expression())
            if  res.error: return res
            return res.Sucsses(expression)

        elif token.matches(TOKEN_KEYWORD, 'func'):
            expression = res.Register(self.Func_expression())
            if  res.error: return res
            return res.Sucsses(expression)

        
        return res.failure(InvalidSyntaxErorr(
            token.start_pos, token.end_pos,
            "Expected int, float, identifier, '+', '-' , '('  or '[' "
        ))

    def power(self):
        return self.bin_op(self.call, (TOKEN_POW,), self.Factor)

    def Factor(self):
        res = ParserResult()
        token = self.curr_token

        if token.type in (TOKEN_PLUS, TOKEN_MINUS):
            self.Register_advacement(res)
            factor = res.Register(self.Factor())
            if  res.error: return res
            return res.Sucsses(unaryoperationNode(token,factor))

        return self.power()

    def Term(self):
        return self.bin_op(self.Factor, (TOKEN_MUL, TOKEN_DIV,TOKEN_MODULE))
    
    def arithmetic_expression(self):
        return self.bin_op(self.Term, (TOKEN_PLUS, TOKEN_MINUS))

    def Comparison_expression(self):
        res = ParserResult()

        if self.curr_token.matches(TOKEN_KEYWORD, "not"):
            operation_token = self.curr_token
            self.Register_advacement(res)

            node  = res.Register(self.Comparison_expression())
            if  res.error :return res
            return res.Sucsses(unaryoperationNode(operation_token,node))

        node = res.Register(self.bin_op(self.arithmetic_expression,(TOKEN_EE, TOKEN_NE, TOKEN_LT, TOKEN_GT, TOKEN_GTE, TOKEN_LTE)))
        
        if  res.error: 
            return res.failure(InvalidSyntaxErorr(
            self.curr_token.start_pos, self.curr_token.end_pos,
            "Expected int, float, identifier, keyword, '+', '-' , '(' , '[' or 'not' "
        ))

        return res.Sucsses(node)

    def Expression(self):
        res = ParserResult()

        while self.curr_token.type  == TOKEN_NEWLINE:
            self.Register_advacement(res)

        if self.curr_token.matches(TOKEN_KEYWORD, "let"):
            self.Register_advacement(res)

            if self.curr_token.type != TOKEN_IDENTIFIER:
                return res.failure(InvalidSyntaxErorr(
                    self.curr_token.start_pos, self.curr_token.end_pos,
                    'Expected identifier'
                ))

            variable_name =  self.curr_token
            self.Register_advacement(res)

            if self.curr_token.type != TOKEN_EQ:
                return res.failure(InvalidSyntaxErorr(
                    self.curr_token.start_pos, self.curr_token.end_pos,
                    "Expected '=' "
                ))
            self.Register_advacement(res)
            expression = res.Register(self.Expression())
            if  res.error:return res
            return res.Sucsses(var_assign_node(variable_name, expression,True))


        node =  res.Register(self.bin_op(self.Comparison_expression, ((TOKEN_KEYWORD,"and"),  (TOKEN_KEYWORD, "or"))))
        if  res.error: 
            return res.failure(InvalidSyntaxErorr(
                self.curr_token.start_pos, self.curr_token.end_pos,
                "Expected 'let', int, float, identifier, '+', '-' or '(' "
            ))

        return res.Sucsses(node)

    def bin_op(self, func_a, ops,func_b= None):
        if func_b == None:
            func_b = func_a
        
        res = ParserResult()
        left = res.Register(func_a())
        if  res.error: return res

        while self.curr_token.type in ops or (self.curr_token.type,self.curr_token.value) in ops:
            op_tok = self.curr_token
            self.Register_advacement(res)
            right = res.Register(func_b())
            if  res.error: return res
            left = BinOpertaionNode(left, op_tok, right)

        return res.Sucsses(left)

    def If_expression(self):
        res = ParserResult()
        temp  = res.Register(self.if_elif_maker('if'))
        if  res.error:return res
        new_cases, else_case = temp
        return res.Sucsses(IfNode(new_cases, else_case))

    def if_elif_maker(self,ident):
        res = ParserResult()
        cases = []
        else_case = None

        # if ident == 'if' and not self.curr_token.matches(TOKEN_KEYWORD, ident):
        #     return res.failure(InvalidSyntaxErorr(self.curr_token.start_pos,self.curr_token.end_pos
        #     ,"Expected 'if' " 
        #     ))
        
        if not self.curr_token.matches(TOKEN_KEYWORD, ident):
            return res.error(InvalidSyntaxErorr(
                self.curr_token.start_pos, self.curr_token.end_pos,
                str(f"Expected {ident}")
            )

            )
        self.Register_advacement(res)

        condition  = res.Register(self.Expression())
        if  res.error : return res

        if not self.curr_token.type == TOKEN_START:
            return res.failure(InvalidSyntaxErorr(
                self.curr_token.start_pos, self.curr_token.end_pos,
                "Expected '>>'"
            ))
        
        self.Register_advacement(res)

        if self.curr_token.type == TOKEN_NEWLINE:
            self.Register_advacement(res)

            statments = res.Register(self.statments())
            if  res.error: return res
            cases.append((condition, statments,True))

            if self.curr_token.type == TOKEN_END:
                self.Register_advacement(res)

            else:
                all_cases = res.Register(self.elif_else_expression())
                if  res.error : return res
                new_cases, else_case  = all_cases
                cases.extend(new_cases )
        else:
            expression = res.Register(self.statment())
            if  res.error : return res
            cases.append((condition, expression, False))

            all_cases = res.Register(self.elif_else_expression())
            if  res.error: return res
            new_cases, else_case  = all_cases
            cases.extend(new_cases)

        return res.Sucsses(
                (cases, else_case)
        )

    def elif_expression(self):
        return self.if_elif_maker('elif')

    def else_expression(self):
        res = ParserResult()
        else_case = None

        if self.curr_token.matches(TOKEN_KEYWORD, 'else'):
            self.Register_advacement(res)
            
            if self.curr_token.type != TOKEN_START:
                    return res.failure(InvalidSyntaxErorr(
                        self.curr_token.start_pos, self.curr_token.end_pos,
                        "Expected '>>'"
                    ))
            
            self.Register_advacement(res)
            if self.curr_token.type == TOKEN_NEWLINE:
                self.Register_advacement(res)

                statments = res.Register(self.statments())
                if  res.error: return res
                else_case  = (statments,True)

                if self.curr_token.type == TOKEN_END:
                    self.Register_advacement(res)

                else:
                    return res.failure(InvalidSyntaxErorr(
                        self.curr_token.start_pos, self.curr_token.end_pos,
                        "Expected '<<'"
                    ))
            else:
                expression = res.Register(self.statment())
                if  res.error : return res
                else_case = (expression, False)

        return res.Sucsses(
            else_case
        )
    
    def elif_else_expression(self):
        res = ParserResult()
        cases, else_case = [], None

        if self.curr_token.matches(TOKEN_KEYWORD, "elif"):
            all_cases = res.Register(self.elif_expression())
            if  res.error : return res
            cases, else_case = all_cases
        
        else:
            
            else_case = res.Register(self.else_expression())
            if  res.error: return res

        return res.Sucsses((cases,else_case))
            

    def Register_advacement(self,res):
        res.Register_advancement()
        self.advance()



    def ListCall_expression(self):
        res  = ParserResult()
        txt = self.curr_token.value
        self.Register_advacement()

    def For_expression(self):
        res = ParserResult()


        self.Register_advacement(res)

        if self.curr_token.type != TOKEN_IDENTIFIER:
            return res.failure(InvalidSyntaxErorr(
                self.curr_token.start_pos , self.curr_token.end_pos,
                "Expected Identifier after For loop declartion"
            ))

        pointer_name = self.curr_token
        self.Register_advacement(res)
        
        if self.curr_token.type != TOKEN_EQ:
            return res.failure(InvalidSyntaxErorr(
                self.curr_token.start_pos , self.curr_token.end_pos,
                "Expected '=' after identifier"
            ))

        self.Register_advacement(res)
        starting_pointer = res.Register(self.Expression())      
        if  res.error: return res

        if self.curr_token.type != TOKEN_ARROW:
            return res.failure(InvalidSyntaxErorr(
                self.curr_token.start_pos , self.curr_token.end_pos,
                "Expected '->' "
            ))

        self.Register_advacement(res) 

        end_poniter = res.Register(self.Expression())
        if  res.error: return Error
        skip_value = None
        if self.curr_token.matches(TOKEN_KEYWORD,'skip'):
            self.Register_advacement(res)
            skip_value = res.Register(self.Expression())


            if  res.error :return res
        

        if not self.curr_token.type == TOKEN_START :
           return res.failure(InvalidSyntaxErorr(
                self.curr_token.start_pos , self.curr_token.end_pos,
                "Expected '>>' "
            ))           
        
        self.Register_advacement(res)
        if self.curr_token.type == TOKEN_NEWLINE:
            self.Register_advacement(res)

            body_content = res.Register(self.statments())
            if  res.error: return res

            if not self.curr_token.type == TOKEN_END:
                return res.failure(InvalidSyntaxErorr(
                    self.curr_token.start_pos, self.curr_token.end_pos,
                    "Expected '<<'"
                ))

            self.Register_advacement(res)
            
            return res.Sucsses(ForNode(pointer_name, starting_pointer,end_poniter,skip_value, body_content,True))

        body_content = res.Register(self.statment())
        if  res.error: return res
        
        return res.Sucsses(ForNode(pointer_name, starting_pointer,end_poniter,skip_value, body_content,False))
     
    def While_expression(self):
        res = ParserResult()

        self.Register_advacement(res)
        condition = res.Register(self.Expression())
        if  res.error: return res

        if self.curr_token.type != TOKEN_START:
               return res.failure(InvalidSyntaxErorr(
                self.curr_token.start_pos , self.curr_token.end_pos,
                "Expected '>>' "

            ))  

        self.Register_advacement(res)

        if self.curr_token.type == TOKEN_NEWLINE:
            self.Register_advacement(res)

            body_content = res.Register(self.statments())
            if  res.error: return res

            if not self.curr_token.type == TOKEN_END:
                return res.failure(InvalidSyntaxErorr(
                    self.curr_token.start_pos, self.curr_token.end_pos,
                    "Expected '<<'"
                ))
            self.Register_advacement(res)
            return res.Sucsses(WhileNode(condition,body_content, True))
        body_content = res.Register(self.statment())
        if  res.error: return res

        return res.Sucsses(WhileNode(condition, body_content,False))

    def Func_expression(self):
        res = ParserResult()

        self.Register_advacement(res)

        if self.curr_token.type == TOKEN_IDENTIFIER:
            func_name_token = self.curr_token
            self.Register_advacement(res)

            if self.curr_token.type != TOKEN_LPAREN:
                return res.failure(InvalidSyntaxErorr(
                    self.curr_token.start_pos, self.curr_token.end_pos,
                    "Expected '(' after function declaration"
                ))

        else:
            func_name_token = None
            if self.curr_token.type != TOKEN_LPAREN:
                return res.failure(InvalidSyntaxErorr(
                    self.curr_token.start_pos, self.curr_token.end_pos,
                    "Expected identifier after function declaration"
                ))
        
        self.Register_advacement(res)

        arg_name_tokens = []

        if self.curr_token.type == TOKEN_IDENTIFIER:
            arg_name_tokens.append(self.curr_token)
            self.Register_advacement(res)

            while self.curr_token.type == TOKEN_COMMA:
                self.Register_advacement(res)

                if self.curr_token.type != TOKEN_IDENTIFIER:
                    return res.failure(InvalidSyntaxErorr(
                        self.curr_token.start_pos, self.curr_token.end_pos,
                        "Expected identifier"
                    ))
                arg_name_tokens.append(self.curr_token)
                self.Register_advacement(res)

            if self.curr_token.type != TOKEN_RPARENT:
                    return res.failure(InvalidSyntaxErorr(
                    self.curr_token.start_pos, self.curr_token.end_pos,
                    "Expected ')' or ','  after function declaration"
                ))

        else:
            if self.curr_token.type != TOKEN_RPARENT:
                return res.failure(InvalidSyntaxErorr(
                        self.curr_token.start_pos, self.curr_token.end_pos,
                        "Expected ')' or  identifier after function declaration"
                    ))
        self.Register_advacement(res)
            
        if self.curr_token.type != TOKEN_START:
            return res.failure(InvalidSyntaxErorr(
                    self.curr_token.start_pos, self.curr_token.end_pos,
                    "Expected '>>' "
                ))

        self.Register_advacement(res)

        if self.curr_token.type != TOKEN_NEWLINE:##
            
            body = res.Register(self.Expression())
            if  res.error:return res

            return res.Sucsses(functionDefNode(func_name_token, arg_name_tokens, body,True))

        self.Register_advacement(res)
        
        while self.curr_token.type == TOKEN_NEWLINE:
            self.Register_advacement(res)

        body = res.Register(self.statments())
        if  res.error:return res

        if not self.curr_token.type == TOKEN_END:
            return res.failure(InvalidSyntaxErorr(
                self.curr_token.start_pos,self.curr_token.end_pos,
                "Expected '<<'"
            ))
        self.Register_advacement(res)

        return res.Sucsses(
            functionDefNode(
                func_name_token,
                arg_name_tokens,
                body,
                False
            )
        )
    
    def list_expression(self):
        res = ParserResult()
        elements_nodes = []
        start_pos = self.curr_token.start_pos.copy()

        self.Register_advacement(res)

        if self.curr_token.type == TOKEN_RSQUARE:
            self.Register_advacement(res) 
        else:
            elements_nodes.append(res.Register(self.Expression()))
            if  res.error:
                return res.failure(InvalidSyntaxErorr(
                    self.curr_token.start_pos, self.curr_token.end_pos,
                    "Expected ']' , keyword, identifier  or values"
                ))
            
            while self.curr_token.type == TOKEN_COMMA:
                self.Register_advacement(res)

                elements_nodes.append(res.Register(self.Expression()))
                if  res.error: return res

            if self.curr_token.type != TOKEN_RSQUARE:
                return res.failure(InvalidSyntaxErorr(
                    self.curr_token.start_pos, self.curr_token.end_pos,
                    "Expected ',' or ']'"
                ))

            self.Register_advacement(res)
        
        return res.Sucsses(ListNode(elements_nodes, start_pos, self.curr_token.end_pos.copy()))

class RuntimeResult:
    def __init__(self):
        self.reset()

    def reset(self):
        self.value = None
        self.error = None
        self.func_return_value = None
        self.loop_should_continue = False
        self.loop_should_break = False

    def Register(self, res):
        if  res.should_return(): self.error = res.error
        self.func_return_value = res.func_return_value
        self.loop_should_continue = res.loop_should_continue
        self.loop_should_break = res.loop_should_break
        return res.value

    def success(self, value):
        self.reset()
        self.value = value
        return self

    def success_return(self, value):
        self.reset()
        self.func_return_value = value
        return self
    
    def success_continue(self):
        self.reset()
        self.loop_should_continue = True
        return self

    def success_break(self):
        self.reset()
        self.loop_should_break = True
        return self

    def failure(self,error):
        self.reset()
        self.error = error
        return self
    def should_return(self):
            # Note: this will allow you to continue and break outside the current function
        return (
        self.error or
        self.func_return_value or
        self.loop_should_continue or
        self.loop_should_break
    )

class Value():
    def __init__(self):
        self.set_position()
        self.set_context()

    def set_position(self, start_pos=None, end_pos=None):
        self.start_pos = start_pos
        self.end_pos = end_pos
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def addition(self, other):
        return None, self.illegal_operation(other)

    def subtract(self, other):
        return None, self.illegal_operation(other)

    def multiply(self, other):
        return None, self.illegal_operation(other)

    def divide(self, other):
        return None, self.illegal_operation(other)

    def powered(self, other):
        return None, self.illegal_operation(other)

    def get_EQ(self, other):
        return None, self.illegal_operation(other)

    def get_EE(self, other):
        return None, self.illegal_operation(other)

    def get_NE(self, other):
        return None, self.illegal_operation(other)

    def get_LT(self, other):
        return None, self.illegal_operation(other)

    def get_GT(self, other):
        return None, self.illegal_operation(other)

    def get_LTE(self, other):
        return None, self.illegal_operation(other)

    def get_GTE(self, other):
        return None, self.illegal_operation(other)

    def and_with(self, other):
        return None, self.illegal_operation(other)

    def or_with(self, other):
        return None, self.illegal_operation(other)

    def _not(self):
        return None, self.illegal_operation()

    def execute(self, args):
        return RuntimeResult().failure(self.illegal_operation())

    def copy(self):
        raise Exception('No copy method defined')

    def is_true(self):
        return False

    def illegal_operation(self, other=None):
        if not other: other = self
        return RuntimeError(
            self.start_pos, other.end_pos,
            'Illegal operation',
            self.context
        )

class String(Value):
    def __init__(self,value):
        super().__init__()
        self.value = value

    def multiply(self, other):
        if isinstance(other,Number):
            return String(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self,other)

    def addition(self, other):
        return String(self.value + str(other.value)).set_context(self.context), None


    def change_to(self,char, by_this):
        if isinstance(char,String) and isinstance(by_this,String):
            for idx in range(len(self.value)):
                if self.value[idx] == char.value:
                    self.value[idx] = by_this
            return self.value, None

        else:
            return None, Value.illegal_operation(char,by_this) 

    def length(self):
        return Number(len(self.value))

    def copy(self):
        copy = String(self.value)
        copy.set_context(self.context)
        copy.set_position(self.start_pos, self.end_pos)
        return copy
    def __repr__(self):
        return str(f'"{self.value}"'
)
class List(Value):
    def __init__(self,elements) -> None:
        super().__init__()
        self.elements = elements

    def addition(self, other):
        if isinstance(other,List):
            new_list = self.elements[:]
            new_list.extend(other.elements)
            return List(new_list), None
        else:
            new_list = self.elements[:]
            new_list.append(other.value)
            return List(new_list), None

    def multiply(self, other):
        if isinstance(other, Number):
            new_list = self.elements[:]
            for i in range(other.value - 1):
                new_listt = self.elements[:]
                new_list.extend(new_listt)
            return List(new_list), None
        else:
            return None, Value.illegal_operation(self,other)

# should be wokred on
    # def divide(self, other):
    #     pop_count = 0
    #     if isinstance(other, List):
    #         new_list = self.elements[:]
    #         other_elements = other.elements[:]


    #         return List(new_list) , None

    #     elif other.value in self.elements:
    #         new_list = self.elements[:]
    #         for idx in range(len(self.elements)):
    #             if self.elements[idx -pop_count] == other.value:
    #                 new_list.pop(idx - pop_count )
    #                 pop_count +=1

    #         return List(new_list) , None
        
    #     else:
    #         return None, RunTimeError(
    #             other.start_pos, other.end_pos,
    #             "Element is not in the list"
    #             ,self.context
    #         )


    # def minus(self,other):
    #     new_list = self.elements[:]
    #     if isinstance(other, List):
    #         pop_count = 0
    #         for num in other.elements:
    #             new_list.pop(num -pop_count)
    #             pop_count +=1
    #         return List(new_list), None

    #     elif isinstance(other,Number):
    #         if other.value < (len(new_list) -1):
    #             new_list.pop(other.value)
    #             return List(new_list), None
    #         else:
    #             return None, RuntimeError(
    #                 other.start_pos, other.end_pos,
    #                 "Invalid index".
    #                 self.context
    #             )
    #     else:
    #         return None, Value.illegal_operation(self,other)

    def __repr__(self) -> str:
        return  str(f" [{', '.join([str(elem) for elem in self.elements])}] ")

    def __len__(self) -> int:
        return len(self.elements)

    def copy(self):
        cop = List(self.elements)
        cop.set_position(self.start_pos, self.end_pos)
        cop.set_context(self.context)
        return cop

class Number(Value):
    def __init__(self, value)-> None:
        super().__init__()
        self.value = value
        if type(value) == str:
            if (float(value) %1) != 0:
                self.value = float(value)
            else:
                self.value = int(value)   

    def addition(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def subtract(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def multiply(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def module(self,other):
        if isinstance(other, Number):
            return Number(self.value % other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def divide(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RuntimeError(
                    other.start_pos, other.end_pos,
                    'Division by zero',
                    self.context
                )

            return Number(self.value / other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def powered(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_EQ(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_EE(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)


    def get_NE(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_LT(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_GT(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_LTE(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_GTE(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def and_with(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def or_with(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def _not(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None

    def copy(self):
        copy = Number(self.value)
        copy.set_position(self.start_pos, self.end_pos)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return self.value != 0

    def __repr__(self):
        return str(self.value)
Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)

class BaseFunction(Value):
    def __init__(self, name):
        super().__init__()
        self.name = name or "<anonymous>"

    def generate_new_context(self):
        new_context = Context(self.name, self.context, self.start_pos)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context

    def check_args(self, arg_names, args):
        res = RuntimeResult()

        if len(args) > len(arg_names):
            return res.failure(RunTimeError(
            self.start_pos, self.end_pos,
            str(f"{len(args) - len(arg_names)} too many args passed into {self}"),
            self.context
            ))

        if len(args) < len(arg_names):
            return res.failure(RunTimeError(
            self.start_pos, self.end_pos,
            str(f"{len(arg_names) - len(args)} too few args passed into {self}"),
            self.context
            ))

        return res.success(None)

    def populate_args(self, arg_names, args, exec_ctx):
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(exec_ctx)
            exec_ctx.symbol_table.set(arg_name, arg_value)

    def check_and_populate_args(self, arg_names, args, exec_ctx):
        res = RuntimeResult()
        res.Register(self.check_args(arg_names, args))
        if  res.should_return(): return res
        self.populate_args(arg_names, args, exec_ctx)
        return res.success(None)

class Function(BaseFunction):
  def __init__(self, name, body_node, arg_names, should_return_null):
    super().__init__(name)
    self.body_node = body_node
    self.arg_names = arg_names
    self.should_return_null = should_return_null

  def execute(self, args):
    
    res = RuntimeResult()
    interpreter = Interpreter()
    exec_ctx = self.generate_new_context()

    res.Register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
    if  res.should_return(): return res

    value = res.Register(interpreter.visit(self.body_node, exec_ctx))
    if  res.should_return() and res.func_return_value == None: return res
    return_value = (value if self.should_return_null else None) or res.func_return_value or Number.null

    return res.success(return_value)

  def copy(self):
    copy = Function(self.name, self.body_node, self.arg_names,self.should_return_null)
    copy.set_context(self.context)
    copy.set_position(self.start_pos, self.end_pos)
    return copy

  def __repr__(self):
    return str("<function {self.name}>")

class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, args):
        res = RuntimeResult()
        exec_ctx = self.generate_new_context()

        method_name =str( f'execute_{self.name}')
        method = getattr(self, method_name, self.no_visit_method)


        res.Register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
        if  res.should_return(): return res

        return_value = res.Register(method(exec_ctx))
        if  res.should_return(): return res
        return res.success(return_value)

    def no_visit_method(self, node, context):
        raise Exception(str(f'No execute_{self.name} method defined'))

    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_position(self.start_pos, self.end_pos)
        return copy

    def __repr__(self):
        return str(f"<built-in function {self.name}>")

  #####################################

    def execute_print(self, exec_ctx):
        value = exec_ctx.symbol_table.get('value')
        if type(value) == Number:
            print(value)
        else:
            print(str(value)[1:-1])
        return RuntimeResult().success(String(str(exec_ctx.symbol_table.get('value'))))
    execute_print.arg_names = ['value']

  
    def execute_input(self, exec_ctx):
        list_reper = list(str(exec_ctx.symbol_table.get('value')))
        text = input("".join(list_reper[1:-1]))

        return RuntimeResult().success(String(text))
    execute_input.arg_names = ['value']

    def execute_input_int(self, exec_ctx):
        while True:
            list_reper = list(str(exec_ctx.symbol_table.get('value')))
            text = input("".join(list_reper[1:-1]))
            try:
                number = int(text)
                break
            except ValueError:
                print(str(f"'{text}' must be an integer. Try again!"))
        return RuntimeResult().success(Number(number))
    execute_input_int.arg_names = ['value']

    def execute_clear(self, exec_ctx):
        os.system('cls' if os.name == 'nt' else 'cls') 
        return RuntimeResult().success(Number.null)
    execute_clear.arg_names = []

    def execute_is_num(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), Number)
        return RuntimeResult().success(Number.true if is_number else Number.false)
    execute_is_num.arg_names = ["value"]

    def execute_is_string(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), String)
        return RuntimeResult().success(Number.true if is_number else Number.false)
    execute_is_string.arg_names = ["value"]

    def execute_is_list(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), List)
        return RuntimeResult().success(Number.true if is_number else Number.false)
    execute_is_list.arg_names = ["value"]

    def execute_is_function(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), BaseFunction)
        return RuntimeResult().success(Number.true if is_number else Number.false)
    execute_is_function.arg_names = ["value"]

    def execute_append(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        value = exec_ctx.symbol_table.get("value")

        if not isinstance(list_, List):
            return RuntimeResult().failure(RunTimeError(
            self.start_pos, self.end_pos,
            "First argument must be list",
            exec_ctx
            ))

        list_.elements.append(value)
        return RuntimeResult().success(Number.null)
    execute_append.arg_names = ["list", "value"]

    def execute_pop(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        index = exec_ctx.symbol_table.get("index")

        if not isinstance(list_, List):
            return RuntimeResult().failure(RunTimeError(
            self.start_pos, self.end_pos,
            "First argument must be list",
            exec_ctx
            ))

        if not isinstance(index, Number):
            return RuntimeResult().failure(RunTimeError(
            self.start_pos, self.end_pos,
            "Second argument must be number",
            exec_ctx
            ))

        try:
            element = list_.elements.pop(index.value)
        except:
            return RuntimeResult().failure(RunTimeError(
            self.start_pos, self.end_pos,
            'Element at this index could not be removed from list because index is out of bounds',
            exec_ctx
            ))
        return RuntimeResult().success(element)
    execute_pop.arg_names = ["list", "index"]

    def execute_extend(self, exec_ctx):
        listA = exec_ctx.symbol_table.get("listA")
        listB = exec_ctx.symbol_table.get("listB")

        if not isinstance(listA, List):
            return RuntimeResult().failure(RunTimeError(
                self.start_pos, self.end_pos,
                "First argument must be list",
                exec_ctx
            ))

        if not isinstance(listB, List):
            return RuntimeResult().failure(RunTimeError(
                self.start_pos, self.end_pos,
                "Second argument must be list",
                exec_ctx
            ))

        listA.elements.extend(listB.elements)
        return RuntimeResult().success(Number.null)
    execute_extend.arg_names = ["listA", "listB"]

    def execute_length(self,exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")

        if not isinstance(list_, List):
            return RuntimeResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "Argument must be list",
                exec_ctx
            ))

        return RuntimeResult().success(Number(len(list_.elements)))
    execute_length.arg_names = ["list"]     

    def execute_Run(self,exec_ctx):
        fn = exec_ctx.symbol_table.get('fn')

        if not isinstance(fn, String):
            return RuntimeResult().failure(RunTimeError(
            self.start_pos, self.end_pos,
            "Second argument must be string",
            exec_ctx
        ))

        fn = fn.value

        try:
            with open(fn, "r") as f:
                script = str(f.read())
        except Exception as e:
            return RuntimeResult().failure(RunTimeError(
                self.start_pos, self.end_pos,
                str(f"Failed to load script \"{fn}\"\n") + str(e),
                exec_ctx
            ))

        temp_ = list(script)
        while temp_[0] == "\n":
            temp_.pop(0)

        _ , error = run(temp_, fn)
        if error:
            return RuntimeResult().failure(RunTimeError(
                self.start_pos, self.end_pos,
                str(f"Failed to finish executing script \"{fn}\"\n") +
                error.as_string(),
                exec_ctx
            ))

        return RuntimeResult().success(Number.null)
    execute_Run.arg_names = ['fn']

BuiltInFunction.print       = BuiltInFunction("print")
BuiltInFunction.input       = BuiltInFunction("input")
BuiltInFunction.input_int   = BuiltInFunction("input_int")
BuiltInFunction.clear       = BuiltInFunction("clear")
BuiltInFunction.is_num      =  BuiltInFunction("is_num")
BuiltInFunction.is_string   = BuiltInFunction("is_string")
BuiltInFunction.is_list     = BuiltInFunction("is_list")
BuiltInFunction.is_function = BuiltInFunction("is_function")
BuiltInFunction.append      = BuiltInFunction("append")
BuiltInFunction.pop         = BuiltInFunction("pop")
BuiltInFunction.extend      = BuiltInFunction("extend")
BuiltInFunction.Run         = BuiltInFunction("Run")
BuiltInFunction.length      = BuiltInFunction("length")


class Context:
    def __init__(self,display_name, parent=None, parent_entry_pos=None) -> None:
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None

class SymbolTable:
    def __init__(self,parent=None) -> None:
        self.symbols = {}
        self.parent = parent

    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return  value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]

    def is_in(self,name):
        return True if name  in self.symbols.keys() else False

    def __repr__(self) -> str:
        return '"{}"'.format(self.value)

# this class takes the nodes after they were order with the parser
# and then executes them in order  
class Interpreter:
    def visit(self,node, context):
        method_name = str(f"visit_{type(node).__name__}")
        method = getattr(self,method_name,self.no_visit_method)
        return method(node,context) 
    
    def no_visit_method(self,node, context):
        raise Exception(str(f"No visit_{type(node).__name__} method defined"))

    def visit_var_access_node(self, node, context):
        res = RuntimeResult()
        var_name = node.var_name_token.value
        value = context.symbol_table.get(var_name) 

        if not value:
            return res.failure(RunTimeError(
                node.start_pos, node.end_pos,
                str(f"{var_name} is not defined"),
                context
            ))
        value = value.copy().set_position(node.start_pos, node.end_pos).set_context(context)
        return res.success(value)

    def visit_StringNode(self,node,context):
        return RuntimeResult().success(
            String(node.token.value).set_context(context).set_position(node.start_pos,node.end_pos)
        )    

    def visit_var_assign_node(self, node, context):
        res = RuntimeResult()
        var_name = node.var_name_token.value
        value = res.Register(self.visit(node.value_node,context))

        if  res.should_return():return res
        if global_symbol_table.is_in(var_name)  or node.force:
            global_symbol_table.set(var_name,value)
            
        
        else:
            return res.failure(InvalidSyntaxErorr(
                node.start_pos, node.end_pos,
                str(f"Variable '{var_name}' refernced before assignment")
            ))
            
        return res.success(value) 

    def visit_BinOpertaionNode(self, node,context):
        res = RuntimeResult()
        left = res.Register(self.visit(node.right_node,context))
        if  res.should_return(): return res
        right = res.Register(self.visit(node.left_node, context))
        if  res.should_return(): return res
        
        result = None
        error = None
        if node.operation_token.type == TOKEN_PLUS:
            result, error =  left.addition(right)
        
        elif node.operation_token.type == TOKEN_MINUS:
            result, error = left.subtract(right)

        elif node.operation_token.type == TOKEN_MUL:
            result, error =  left.multiply(right)

        elif node.operation_token.type == TOKEN_MODULE:
            result, error = left.module(right)

        elif node.operation_token.type == TOKEN_DIV:
            result, error =  left.divide(right)

        elif node.operation_token.type == TOKEN_POW:
            result, error =  left.powered(right)

        elif node.operation_token.type == TOKEN_EE:
            result, error =  left.get_EE(right)

        elif node.operation_token.type == TOKEN_NE:
            result, error =  left.get_NE(right)

        elif node.operation_token.type == TOKEN_GT:
            result, error =  left.get_GT(right)

        elif node.operation_token.type == TOKEN_LT:
            result, error =  left.get_LT(right)

        elif node.operation_token.type == TOKEN_GTE:
            result, error =  left.get_GTE(right)
        
        elif node.operation_token.type == TOKEN_LTE:
            result, error =  left.get_LTE(right)
        
        elif node.operation_token.matches(TOKEN_KEYWORD,"and"):
            result, error =  left.and_with(right)
        
        elif node.operation_token.matches(TOKEN_KEYWORD, "or"):
            result, error =  left.or_with(right)

    
        if error:
            return res.failure(error)
        else:
            return res.success(result.set_position(node.start_pos,node.end_pos))    
    
    def visit_unaryoperationNode(self,node,context):
        res = RuntimeResult()
        number = res.Register(self.visit(node.node, context))
        if  res.should_return(): return res 

        error = None
        if node.operation_token.type == TOKEN_MINUS:
            number, error = number.multiply(Number(-1))

        elif node.operation_token.matches(TOKEN_KEYWORD, 'not'):
            number, error = number._not()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_position(node.start_pos,node.end_pos))

    def visit_NumberNode(self,node,context):
        return RuntimeResult().success(
            Number(node.token.value).set_context(context).set_position(node.start_pos,node.end_pos)
        )

    def visit_IfNode(self, node, context):
        res = RuntimeResult()
        
        for condition, expression,should_return_null in node.cases:
            condition_result =  res.Register(self.visit(condition, context))
            if  res.should_return(): return res

            if condition_result.is_true():
                expression_result = res.Register(self.visit(expression, context))
                if  res.should_return(): return res
                return res.success(Number.null if should_return_null else expression_result)

        if node.else_case:
            expression ,should_return_null = node.else_case
            else_value =res.Register(self.visit(expression, context))
            if  res.should_return(): return res
            return res.success(Number.null if should_return_null else else_value)
        
        return res.success(Number.null)
    
    def visit_ForNode(self, node, context):
        res = RuntimeResult()
        elements = []
        start_pointer = res.Register(self.visit(node.start_value_node,context))

        if  res.should_return():return res
        
        end_pointer = res.Register(self.visit(node.end_value_node, context))
        if  res.should_return():return res
        
        skip_value = Number(1)
        if node.skip_value_node:
            skip_value = res.Register(self.visit(node.skip_value_node,context))
            if  res.should_return():return res

        pointer = start_pointer.value

        def evaluate_condition():
             return pointer < end_pointer.value if skip_value.value >= 0 else pointer > end_pointer.value
             
        while evaluate_condition():
            context.symbol_table.set(node.var_name_node.value,Number(pointer))
            pointer += skip_value.value
            value = res.Register(self.visit(node.body_node,context))
            if  res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res

            if res.loop_should_break:
                break
            
            if res.loop_should_continue:
                continue

            elements.append(value)

        return res.success(
            Number.null if node.should_return_null else 
            List(elements).set_context(context).set_position(node.start_pos,node.end_pos)
        )



    
    def visit_WhileNode(self, node, context):
        res = RuntimeResult()
        elements = []
        while True:
            condition = res.Register(self.visit(node.condition_node, context))
            if  res.should_return(): return res

            if not condition.is_true(): break

            value = res.Register(self.visit(node.body_node,context))
            if  res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res

            if res.loop_should_break:
                break
            
            if res.loop_should_continue:
                continue
            
            elements.append(value)

        return res.success(
            Number.null if node.should_return_null else
            List(elements).set_context(context).set_position(node.start_pos,node.end_pos)
        )


    def visit_ListNode(self,node,context):
        res = RuntimeResult()
        elements = []

        for elem in node.elements_nodes:
            elements.append(res.Register(self.visit(elem,context)))
            if  res.should_return() : return res
        
        return res.success(
            List(elements).set_context(context).set_position(node.start_pos,node.end_pos)
        )

    def visit_functionDefNode(self,node, context,):
        res = RuntimeResult()
        func_name = node.var_name_token.value if node.var_name_token else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_tokens]
        func_value = Function(func_name, body_node, arg_names,node.should_return_null).set_context(context).set_position(node.start_pos, node.end_pos)


        if node.var_name_token:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)

    def visit_CallNode(self, node, context):
        res = RuntimeResult()
        args = []

        value_to_call = res.Register(self.visit(node.node_to_call, context))
        if  res.should_return(): return res
        value_to_call = value_to_call.copy().set_position(node.start_pos, node.end_pos)

        for arg_node in node.arg_nodes:
            args.append(res.Register(self.visit(arg_node, context)))
            if  res.should_return(): return res

        return_value = res.Register(value_to_call.execute(args))
        if  res.should_return(): return res
        return_value = return_value.copy().set_position(node.start_pos, node.end_pos).set_context(context)
        return res.success(return_value)

    def visit_ReturnNode(self, node, context):
        res = RuntimeResult()
        if node.node_to_return:
            value = res.Register(self.visit(node.node_to_return, context))
            if res.should_return(): return res
        else:
            value = Number.null
        
        return res.success_return(value)

    def visit_ContinueNode(self, node, context):
        return RuntimeResult().success_continue()

    def visit_BreakNode(self, node, context):
        return RuntimeResult().success_break()

    def visit_ListacssesNode(self,node, context):
        res = RuntimeResult()
        list_name = node.ident
        list_values = context.symbol_table.get(list_name).elements
        idx =  node.index if type(node.index) == int else context.symbol_table.get(node.index).value

        if len(list_values) <= idx:
            return res.failure(Indexerror(node.start_pos,node.end_pos,
                                                              "List index out of range"))
        return res.success(list_values[idx])




global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number.null)
global_symbol_table.set("false", Number.false)
global_symbol_table.set("true", Number.true)
global_symbol_table.set("print", BuiltInFunction.print)
global_symbol_table.set("input", BuiltInFunction.input)
global_symbol_table.set("input_int", BuiltInFunction.input_int)
global_symbol_table.set("clear", BuiltInFunction.clear)
global_symbol_table.set("cls", BuiltInFunction.clear)
global_symbol_table.set("is_num", BuiltInFunction.is_num)
global_symbol_table.set("is_string", BuiltInFunction.is_string)
global_symbol_table.set("is_list", BuiltInFunction.is_list)
global_symbol_table.set("is_func", BuiltInFunction.is_function)
global_symbol_table.set("append", BuiltInFunction.append)
global_symbol_table.set("pop", BuiltInFunction.pop)
global_symbol_table.set("extend", BuiltInFunction.extend)
global_symbol_table.set("Run", BuiltInFunction.Run)
global_symbol_table.set("length", BuiltInFunction.length)


def run(text: str, fn: str):
    #generate tokens
    tokenizer = Tokenizer(text, fn)
    tokens, error =tokenizer.make_tokens()
    if error:return None, error
    # generate Ast
    parser = Parser(tokens)
    ast = parser.parse() # abstract syntax tree
    if ast.error :return None, ast.error
    
    interpreter = Interpreter()
    context = Context("<module>")
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)
    
    return result.value, result.error

# this is not my code 
def string_with_arrows(text, start_pos, end_pos):

    result = ''

    # Calculate indices
    idx_start = max(text.rfind('\n', 0, start_pos.idx), 0)
    idx_end = text.find('\n', idx_start + 1)
    if idx_end < 0: idx_end = len(text)
    
    # Generate each line
    line_count = end_pos.line - start_pos.line + 1
    for i in range(line_count):
        # Calculate line columns
        line = text[idx_start:idx_end]
        col_start = start_pos.col if i == 0 else 0
        col_end = end_pos.col if i == line_count - 1 else len(line) - 1

        # Append to result
        result += line + '\n'
        result += ' ' * col_start + '^' * (col_end - col_start)

        # Re-calculate indices
        idx_start = idx_end
        idx_end = text.find('\n', idx_start + 1)
        if idx_end < 0: idx_end = len(text)

    return result.replace('\t', '')



if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = None
    
    if file_name is not None:
        with open(file_name,'r') as file:
            script = str(file.read())

        result , error = run(script,file_name)
        if error:
            print(error.as_string())

    else :
        while True:
            text = input('Hope >>>')
            result, error = run(text, '<stdin>')
            
            if text.strip() == '':
                continue
            
            if text == 'exit':
                break
            
            if error:
                print(error.as_string())

