""" HOPE LANGUAGE GRAMMERS

"""

import string

DIGITS        = '0123456789'
LETTERS       = string.ascii_letters # t
LETTER_DIGITS = LETTERS + DIGITS
TOKEN_INT        = 'TOKEN_INT'
TOKEN_FLOAT      = 'FLOAT'
TOKEN_PLUS       = 'PLUS' 
TOKEN_MINUS      = 'MINUS'
TOKEN_MUL        = 'MUL'
TOKEN_DIV        = 'DIV'
TOKEN_POW        = 'POW'# power token 
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
TOKEN_LCURLY      = 'LCURLY'
TOKEN_RCURLY      = 'RCURLY'
TOKEN_UNTIL       = 'UNTIL'
TOKEN_SKIP        = 'SKIP'
KEYWORDS = [ 
    'let',
    'and',
    'or',
    'not',
    'if',
    'elif',
    'else',
    'while',
    'for'
]

# this class is made for other claases to inherit from 
class Error:
    def __init__(self, start_pos: int, end_pos: int, error_name: str, details: str) -> None:
        self.error_name = error_name # gives the type of the error if it is syntax error  Illegal Char Error etc..
        self.details = details # what wrong with code it is like a description
        self.start_pos = start_pos
        self.end_pos = end_pos

    def as_string(self):
        result =  f'{self.error_name}: {self.details} \n File {self.start_pos.fn}, line {self.start_pos.line + 1}'
        result += '\n\n' + string_with_arrows(self.start_pos.ftxt, self.start_pos, self.end_pos)
        return result

class IllegalCharError(Error):
    def __init__(self,start_pos :int, end_pos: int, details='') -> None:
        super().__init__(start_pos, end_pos, 'Illegal Character', details)

class InvalidSyntaxErorr(Error):
    def __init__(self, start_pos: int, end_pos: int, details= '') -> None:
        super().__init__(start_pos, end_pos, "Invalid Syntax", details)

class RunTimeError(Error):
    def __init__(self, start_pos: int, end_pos: int, details,context) -> None:
        super().__init__(start_pos, end_pos, "Runtime Error", details)
        self.context = context

class ExpectedCharError(Error):
    def __init__(self, start_pos: int, end_pos: int, error_name: str, details: str) -> None:
        super().__init__(start_pos, end_pos, error_name, details)

    def as_string(self):
        result = self.generate_traceback()
        result +=  f'{self.error_name}: {self.details}'
        result += '\n\n' + string_with_arrows(self.start_pos.ftxt, self.start_pos, self.end_pos)

        return result

    def generate_traceback(self):
        result = ''
        pos = self.start_pos
        ctx = self.context

        while ctx:
            result = f'  File {pos.fn}, line {str(pos.line + 1)}, in {ctx.display_name}\n' + result
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
        return f'{self.type}'

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

            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())

            elif self.current_char == '+':
                tokens.append(Token(TOKEN_PLUS, start_pos=self.position))
                self.advance()

            elif self.current_char == '-':
                tokens.append(Token(TOKEN_MINUS, start_pos=self.position))
                self.advance()

            elif self.current_char == '*':
                tokens.append(Token(TOKEN_MUL, start_pos=self.position))
                self.advance()

            elif self.current_char == '!':
                token, error = self.make_not_equal()
                if error: return [], error
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

            elif self.current_char == '{':
                tokens.append(Token(TOKEN_LCURLY, start_pos=self.position))
                self.advance()

            elif self.current_char == '=':
                tokens.append(self.make_equal())
                

            elif self.current_char == '<':
                tokens.append(self.make_GT_LT())
                self.advance()

            elif self.current_char == '>':
                tokens.append(self.make_GT_LT())
                self.advance()

            else:
                start_pos = self.position.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(start_pos, self.position,"'" + char + "'")

        tokens.append(Token(TOKEN_EOF, start_pos=self.position))
        return tokens, None

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
            return Token(TOKEN_FLOAT, float(num_str, start_pos, self.position))
    
    def make_identifier(self):
        id_str = ''
        start_pos = self.position.copy()

        while self.current_char != None and self.current_char in LETTER_DIGITS + '_':
            id_str += self.current_char
            self.advance()

        token_type = TOKEN_KEYWORD if id_str in KEYWORDS else TOKEN_IDENTIFIER  
        return Token(token_type,id_str,start_pos,self.position)

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
            return Token(TOKEN_UNTIL,start_pos=start_pos,end_pos=self.position)

        if self.current_char =='<' and Token_type == TOKEN_LT:
            return Token(TOKEN_SKIP,start_pos=start_pos,end_pos=self.position)

        if self.current_char == '=':
            Token_type += 'E'
            self.advance()

        return Token(Token_type,start_pos=start_pos,end_pos=self.position)

# nodes

class NumberNode:
    def __init__(self,token : Token) -> None:
        self.token = token
        self.start_pos = token.start_pos
        self.end_pos = token.end_pos

    def __repr__(self) -> str:
        return f'{self.token}'

class unaryoperationNode:
    def __init__(self, operator_token , node) -> None:
        self.operation_token = operator_token
        self.node = node
        self.start_pos = operator_token.start_pos
        self.end_pos = node.end_pos

    def __repr__(self) -> str:
        return f'({self.operator_token}, {self.node})'

class BinOpertaionNode:
    def __init__(self, right_node, operation_token, left_node) -> None:
        self.operation_token = operation_token
        self.left_node = left_node
        self.right_node = right_node
        self.start_pos = left_node.start_pos
        self.end_pos = right_node.end_pos

    def __repr__(self) -> str:
        return f'( {self.left_node} {self.operation} {self.right_node} )'


class var_assign_node:
    def __init__(self, var_name_token, value_node) -> None:
        self.var_name_token = var_name_token
        self.value_node = value_node

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
        self.end_pos = self.else_case or self.cases[-1][0].end_pos



class ForNode():
    def __init__(self, var_name, start_value, end_value, skip_value, body ) -> None:
        self.start_value_node = start_value
        self.end_value_node   = end_value
        self.var_name_node    = var_name
        self.skip_value_node  = skip_value
        self.body_node        = body   

        self.start_pos        = self.var_name_node.start_pos
        self.end_pos          = self.body_node.end_pos

class WhileNode():
    def __init__(self,condition, body) -> None:
        self.condition_node =  condition
        self.body_node      = body

        self.start_pos        = self.condition_node.start_pos
        self.end_pos          = self.body_node.end_pos
# nodes end
    
class ParserResult:
    def __init__(self) -> None:
        self.error = None
        self.node = None
        self.advance_count = 0

    def Register_advancement(self):
        self.advance_count += 1

    def Register(self,res):
        self.advance_count += res.advance_count
        if res.error:self.error = res.error
        return  res.node
        
    def Sucsses(self,node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error  or self.advance_count  == 0:
            self.error = error
        return self

    
# takes the list of token that are returned by the tokenizer and then atates at what order should those token be executed 
class Parser:
    def __init__(self,Tokens) -> None:
        self.tokens = Tokens
        self.tok_idx = - 1 
        self.curr_token = None
        self.advance()
    
    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.curr_token = self.tokens[self.tok_idx]

        return self.curr_token

    def parse(self):
        res= self.Expression()
        if not res.error and self.curr_token.type != TOKEN_EOF:
            return res.failure(InvalidSyntaxErorr(
                self.curr_token.start_pos, self.curr_token.end_pos,
                "Expected  '+', '-', '*' or '/'"
            ))

        return res
    
# to understand the order of this reader grammers in the top of the file
    def Most(self):
        res = ParserResult()
        token = self.curr_token

        if token.type in (TOKEN_FLOAT , TOKEN_INT):
            self.register_advacement(res)
            return res.Sucsses(NumberNode(token))

        if token.type is TOKEN_IDENTIFIER:
            self.register_advacement(res)
            return res.Sucsses(var_access_node(token))

        elif token.type == TOKEN_LPAREN:
            self.register_advacement(res)
            expr = res.Register(self.Expression())
            if res.error: return res

            if self.curr_token.type == TOKEN_RPARENT   :
                self.register_advacement(res)
                return res.Sucsses(expr)
            else:
                return res.failure(InvalidSyntaxErorr(
                    self.curr_token.star_pos, self.curr_token.end_pos, 
                    "Expected ')' "
                ))
        elif token.matches(TOKEN_KEYWORD, 'if'):
            expression = res.Register(self.If_expression())
            if res.error: return res
            return res.Sucsses(expression)

        elif token.matches(TOKEN_KEYWORD, 'while'):
            expression = res.Register(self.While_expression())
            if res.error: return res
            return res.Sucsses(expression)

        elif token.matches(TOKEN_KEYWORD, 'for'):
            expression = res.Register(self.For_expression())
            if res.error: return res
            return res.Sucsses(expression)


        
        return res.failure(InvalidSyntaxErorr(
            token.start_pos, token.end_pos,
            "Expected int, float, identifier, '+', '-' or '(' "
        ))

    def power(self):
        return self.bin_op(self.Most, (TOKEN_POW,), self.Factor)

    def Factor(self):
        res = ParserResult()
        token = self.curr_token

        if token.type in (TOKEN_PLUS, TOKEN_MINUS):
            self.register_advacement(res)
            factor = res.Register(self.Factor())
            if res.error: return res
            return res.Sucsses(unaryoperationNode(token,factor))

        return self.power()

    def Term(self):
        return self.bin_op(self.Factor, (TOKEN_MUL, TOKEN_DIV))
    
    def arithmetic_expression(self):
        return self.bin_op(self.Term, (TOKEN_PLUS, TOKEN_MINUS))

    def Comparison_expression(self):
        res = ParserResult()

        if self.curr_token.matches(TOKEN_KEYWORD, "not"):
            operation_token = self.curr_token
            self.register_advacement(res)

            node  = res.Register(self.Comparison_expression())
            if res.error :return res
            return res.Sucsses(unaryoperationNode(operation_token,node))

        node = res.Register(self.bin_op(self.arithmetic_expression,(TOKEN_EE, TOKEN_NE, TOKEN_LT, TOKEN_GT, TOKEN_GTE, TOKEN_LTE)))
        
        if res.error: 
            return res.failure(InvalidSyntaxErorr(
            self.curr_token.start_pos, self.curr_token.end_pos,
            "Expected int, float, identifier, '+', '-' , '(' or 'not' "
        ))

        return res.Sucsses(node)

    def Expression(self):
        res = ParserResult()
        if self.curr_token.matches(TOKEN_KEYWORD, "let"):
            self.register_advacement(res)

            if self.curr_token.type != TOKEN_IDENTIFIER:
                return res.failure(InvalidSyntaxErorr(
                    self.curr_token.start_pos, self.curr_token.end_pos,
                    'Expected identifier'
                ))

            variable_name =  self.curr_token
            self.register_advacement(res)

            if self.curr_token.type != TOKEN_EQ:
                res.failure(InvalidSyntaxErorr(
                    self.curr_token.start_pos, self.curr_token.end_pos,
                    "Expected '=' "
                ))
            self.register_advacement(res)
            expression = res.Register(self.Expression())
            if res.error:return res
            return res.Sucsses(var_assign_node(variable_name, expression))

        node =  res.Register(self.bin_op(self.Comparison_expression, ((TOKEN_KEYWORD,"and"),  (TOKEN_KEYWORD, "or"))))

        if res.error: 
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
        if res.error: return res

        while self.curr_token.type in ops or (self.curr_token.type,self.curr_token.value) in ops:
            op_tok = self.curr_token
            self.register_advacement(res)
            right = res.Register(func_b())
            if res.error: return res
            left = BinOpertaionNode(left, op_tok, right)

        return res.Sucsses(left)

    def If_expression(self):
        res = ParserResult()
        cases = []
        else_case = []

        self.if_elif_maker(res, 'if', cases)

        while self.curr_token.matches(TOKEN_KEYWORD, "elif"):
            self.if_elif_maker(res, 'elif',cases )

        if self.curr_token.matches(TOKEN_KEYWORD, 'else'):
            self.register_advacement(res)

            else_case = res.Register(self.Expression())
            if res.error:return res
             
        return res.Sucsses(IfNode(cases, else_case))

    def if_elif_maker(self, res, ident, cases):

        # if ident == 'if' and not self.curr_token.matches(TOKEN_KEYWORD, ident):
        #     return res.failure(InvalidSyntaxErorr(self.curr_token.start_pos,self.curr_token.end_pos
        #     ,"Expected 'if' " 
        #     ))
        
        self.register_advacement(res)

        condition  = res.Register(self.Expression())
        if res.error : return res

        if not self.curr_token.type == TOKEN_LCURLY:
            return res.failure(InvalidSyntaxErorr(
                self.curr_token.start_pos, self.curr_token.end_pos,
                "Expected '{'"
            ))
        
        self.register_advacement(res)

        expression = res.Register(self.Expression())
        if res.error: return res
        cases.append((condition, expression))

    def register_advacement(self,res):
        res.Register_advancement()
        self.advance()

    def For_expression(self):
        res = ParserResult()
        self.register_advacement(res)

        if self.curr_token.type != TOKEN_IDENTIFIER:
            return res.failure(InvalidSyntaxErorr(
                self.curr_token.start_pos , self.curr_token.end_pos,
                "Expected Identifier after For loop declartion"
            ))

        pointer_name = self.curr_token
        self.register_advacement(res)
        
        if self.curr_token.type != TOKEN_EQ:
            return res.failure(InvalidSyntaxErorr(
                self.curr_token.start_pos , self.curr_token.end_pos,
                "Expected '=' after identifier"
            ))

        self.register_advacement(res)
        starting_pointer = res.Register(self.Expression())      
        if res.error: return res

        if self.curr_token.type != TOKEN_UNTIL:
            return res.failure(InvalidSyntaxErorr(
                self.curr_token.start_pos , self.curr_token.end_pos,
                "Expected '>>' "
            ))

        self.register_advacement(res) 

        end_poniter = res.Register(self.Expression())
        if res.error: return Error
        skip_value = None
        if self.curr_token.type == TOKEN_SKIP:
            self.register_advacement(res)
            skip_value = res.Register(self.Expression())

            if res.error :return res
        

        if not self.curr_token.type == TOKEN_LCURLY:
           return res.failure(InvalidSyntaxErorr(
                self.curr_token.start_pos , self.curr_token.end_pos,
                "Expected '{' "
            ))           
        
        self.register_advacement(res)
        body_content = res.Register(self.Expression())

        return res.Sucsses(ForNode(pointer_name, starting_pointer,end_poniter,skip_value, body_content))
        
    def While_expression(self):
        res = ParserResult()

        self.register_advacement(res)
        condition = res.Register(self.Expression())
        if res.error: return res

        if self.curr_token.type != TOKEN_LCURLY:
               return res.failure(InvalidSyntaxErorr(
                self.curr_token.start_pos , self.curr_token.end_pos,
                "Expected '{' "

            ))  
        self.register_advacement(res)

        body_content = res.Register(self.Expression())

        return res.Sucsses(WhileNode(condition,body_content))
class RuntimeResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if res.error: self.error = res.error
        return res.value

    def success(self, value):
        self.value = value
        return self
    
    def failure(self,error):
        self.error = error
        return self

class Number:
    def __init__(self, value) -> None:
        self.value = value
        self.set_position()
        self.set_context()

    def set_position(self, start_pos = None , end_pos = None):
        self.start_pos = start_pos
        self.end_pos = end_pos

        return self 
    
    def set_context(self,context=None):
        self.context = context
        return self

    def addition(self,other_num):
        if isinstance(other_num, Number):
            return Number(self.value + other_num.value).set_context(self.context), None

    def subtract(self,other_num):
        if isinstance(other_num, Number):
            return Number(self.value - other_num.value).set_context(self.context) , None
            
    def multiply(self,other_num):
        if isinstance(other_num, Number):
            return Number(self.value * other_num.value).set_context(self.context), None

    def divide(self,other_num):
        if isinstance(other_num, Number):
            print(other_num.value)
            if other_num.value == 0:
                return None , RunTimeError(
                    other_num.start_pos, other_num.end_pos,
                    "Division by zero",
                    self.context
                )
            return Number(self.value / other_num.value).set_context(self.context), None

    def powered(self,other_num):
        if isinstance(other_num, Number):
            return Number(self.value ** other_num.value).set_context(self.context), None    

    def get_EE(self,other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None 

    def get_NE(self,other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None 

    def get_GT(self,other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None 

    def get_LT(self,other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None 

    def get_LTE(self,other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None 

    def get_GTE(self,other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None 

    def and_with(self,other):
        if isinstance(other, Number):
           return Number(int(self.value and other.value)).set_context(self.context), None 

    def or_with(self,other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None 

    def _not(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None 

    def is_true(self):
        return not (self.value == 0)

    def copy(self):
        copy = Number(self.value)
        copy.set_position(self.start_pos,self.end_pos)
        copy.set_context(self.context)
        return copy

    def __repr__(self) -> str:
        return f'{self.value}'

class Context:
    def __init__(self,display_name, parent=None, parent_entry_pos=None) -> None:
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None

class SymbolTable:
    def __init__(self) -> None:
        self.symbols = {}
        self.parent = None

    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return  value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]

# this class takes the nodes after they were order with the parser
# and then executes them in order  
class Interpreter:
    def visit(self,node, context):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self,method_name,self.no_visit_method)
        return method(node,context)
    
    def no_visit_method(self,node, context):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_var_access_node(self, node, context):
        res = RuntimeResult()
        var_name = node.var_name_token.value
        value = context.symbol_table.get(var_name) 

        if not value:
            return res.failure(RunTimeError(
                node.start_pos, node.end_pos,
                f"{var_name} is not defined",
                context
            ))
        value = value.copy().set_position(node.start_pos, node.end_pos)
        return res.success(value)

    def visit_var_assign_node(self, node, context):
        res = RuntimeResult()
        var_name = node.var_name_token.value
        value = res.register(self.visit(node.value_node,context))

        if res.error:return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_BinOpertaionNode(self, node,context):
        res = RuntimeResult()
        left = res.register(self.visit(node.right_node,context))
        if res.error: return res
        right = res.register(self.visit(node.left_node, context))
        if res.error: return res
        
        result = None
        error = None
        if node.operation_token.type == TOKEN_PLUS:
            result, error =  left.addition(right)
        
        elif node.operation_token.type == TOKEN_MINUS:
            result, error = left.subtract(right)

        elif node.operation_token.type == TOKEN_MUL:
            result, error =  left.multiply(right)
            
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
        number = res.register(self.visit(node.node, context))
        if res.error: return res 

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
        
        for condition, expression in node.cases:
            condition_result =  res.register(self.visit(condition, context))
            if res.error: return res

            if condition_result.is_true():
                expression_result = res.register(self.visit(expression, context))
                if res.error: return res
                return res.success(expression_result)

        if node.else_case:
            else_value =res.register(self.visit(node.else_case, context))
            if res.error: return res
            return res.success(else_value)
        
        return res.success(None)
    
    def visit_ForNode(self,node, context):
        res = RuntimeResult()
        start_pointer = res.register(self.visit(node.start_value_node,context))
        if res.error:return res
        
        end_pointer = res.register(self.visit(node.end_value_node, context))
        if res.error:return res
        
        skip_value = 1
        if node.skip_value_node:
            skip_value = res.register(self.visit(node.skip_value_node,context))
            skip_value = skip_value.value
            if res.error:return res

        pointer = start_pointer.value

        def evaluate_condition():
             return pointer < end_pointer.value if skip_value >= 0 else pointer > end_pointer.value
             
        while evaluate_condition():
            context.symbol_table.set(node.var_name_node.value,Number(pointer))
            pointer += 1

            res.register(self.visit(node.body_node,context))
            if res.error: return res

        return res.success(None) 


    
    def visit_WhileNode(self, node, context):
        res = RuntimeResult()

        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.error: return res

            if not condition.is_true(): break

            res.register(self.visit(node.body_node,context))
            if res.error: return res

        return res.success(None)



global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number(0))
global_symbol_table.set("false ", Number(0))
global_symbol_table.set("true", Number(1))


def Run(text: str, fn: str):
    #generate tokens
    tokenizer = Tokenizer(text, fn)
    tokens, error =tokenizer.make_tokens()
    if error:return None ,error
    # generate Ast
    parser = Parser(tokens)
    ast = parser.parse() # abstract syntax tree
    if ast.error :return None, ast.error
    
    interpreter = Interpreter()
    context = Context("<module>")
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node,context)
    
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
