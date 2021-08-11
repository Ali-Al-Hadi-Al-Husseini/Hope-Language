import string

DIGITS        = '0123456789'
LETTERS       = string.ascii_letters
LETTER_DIGITS = LETTERS + DIGITS
TT_INT        = 'TT_INT'
TT_FLOAT      = 'FLOAT'
TT_PLUS       = 'PLUS' 
TT_MINUS      = 'MINUS'
TT_MUL        = 'MUL'
TT_DIV        = 'DIV'
TT_POW        = 'POW'
TT_LPAREN     = 'LPAREN'
TT_RPARENT    = 'RPAREN'
TT_EQ         = 'EQ'
TT_EE         = 'EE'
TT_GT         = 'GT'
TT_NE         = 'NE'
TT_LT         = 'LT'
TT_GTE        = 'GTE'
TT_LTE        = 'LTE'    
TT_KEYWORD    = 'KEYWORD'
TT_IDENTIFIER = 'IDENTIFIER'
TT_EOF        = 'EOF'

KEYWORDS = [ 
    'let',
    'and',
    'or',
    'not'
]

class Error:
    def __init__(self, pos_start: int, pos_end: int, error_name: str, details: str) -> None:
        self.error_name = error_name # gives the type of the error if it is syntax error  Illegal Char Error etc..
        self.details = details # what wrong with code it is like a description
        self.pos_start = pos_start
        self.pos_end = pos_end

    def as_string(self):
        result =  f'{self.error_name}: {self.details} \n File {self.pos_start.fn}, line {self.pos_start.line + 1}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

class IllegalCharError(Error):
    def __init__(self,pos_start :int, pos_end: int, details='') -> None:
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

class InvalidSyntaxErorr(Error):
    def __init__(self, pos_start: int, pos_end: int, details= '') -> None:
        super().__init__(pos_start, pos_end, "Invalid Syntax", details)

class RunTimeError(Error):
    def __init__(self, pos_start: int, pos_end: int, details,context) -> None:
        super().__init__(pos_start, pos_end, "Runtime Error", details)
        self.context = context

class ExpectedCharError(Error):
    def __init__(self, pos_start: int, pos_end: int, error_name: str, details: str) -> None:
        super().__init__(pos_start, pos_end, error_name, details)

    def as_string(self):
        result = self.generate_traceback()
        result +=  f'{self.error_name}: {self.details}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)

        return result

    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result = f'  File {pos.fn}, line {str(pos.line + 1)}, in {ctx.display_name}\n' + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return 'Traceback (most recent call last):\n' + result

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

class Lexer:
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

    # this method takes the text and converts it into tokens
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
                tokens.append(Token(TT_PLUS, start_pos=self.position))
                self.advance()

            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, start_pos=self.position))
                self.advance()

            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, start_pos=self.position))
                self.advance()

            elif self.current_char == '!':
                token, error = self.make_not_equal()
                if error: return [], error
                self.advance()

            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, start_pos=self.position))
                self.advance()
                
            elif self.current_char == '^':
                tokens.append(Token(TT_POW, start_pos=self.position))
                self.advance()

            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, start_pos=self.position))
                self.advance()

            elif self.current_char == ')':
                tokens.append(Token(TT_RPARENT, start_pos=self.position))
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
                pos_start = self.position.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.position,"'" + char + "'")

        tokens.append(Token(TT_EOF, start_pos=self.position))
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.position.copy()

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
            return Token(TT_INT, int(num_str),pos_start, self.position)
        else:
            return Token(TT_FLOAT, float(num_str, pos_start, self.position))
    
    def make_identifier(self):
        id_str = ''
        pos_start = self.position.copy()

        while self.current_char != None and self.current_char in LETTER_DIGITS + '_':
            id_str += self.current_char
            self.advance()

        token_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER  
        return Token(token_type,id_str,pos_start,self.position)

    def make_not_equal(self):
        pos_start = self.position.copy()
        self.advance()

        if self.current_char == '=':
            return Token(TT_NE,start_pos=pos_start,end_pos=self.position), None

        return None, ExpectedCharError(pos_start,self.position, "Expected '=' after '!' ") 
    
    def make_equal(self):
        start_pos = self.position.copy()
        self.advance()
        if self.current_char == "=":
            self.advance()
            return Token(TT_EE,start_pos=start_pos,end_pos=self.position)

        return Token(TT_EQ,start_pos=start_pos,end_pos=self.position())
        
    def make_GT_LT(self):
        start_pos = self.position.copy
        Token_type = TT_GT if self.current_char == ">" else TT_LT
        self.advance()
        
        if self.current_char == '=':
            Token_type += 'E'
            self.advance()

        return Token(Token_type,start_pos=start_pos,end_pos=self.position)

# nodes

class NumberNode:
    def __init__(self,token : Token) -> None:
        self.token = token
        self.pos_start = token.start_pos
        self.pos_end = token.end_pos

    def __repr__(self) -> str:
        return f'{self.token}'

class unaryoperationNode:
    def __init__(self, operator_token , node) -> None:
        self.operation_token = operator_token
        self.node = node
        self.pos_start = operator_token.start_pos
        self.pos_end = node.pos_end

    def __repr__(self) -> str:
        return f'({self.operator_token}, {self.node})'

class BinOpertaionNode:
    def __init__(self, right_node, operation_token, left_node) -> None:
        self.operation_token = operation_token
        self.left_node = left_node
        self.right_node = right_node
        self.pos_start = left_node.pos_start
        self.pos_end = right_node.pos_end

    def __repr__(self) -> str:
        return f'( {self.left_node} {self.operation} {self.right_node} )'


class var_assign_node:
    def __init__(self, var_name_token, value_node):
        self.var_name_token = var_name_token
        self.value_node = value_node

        self.pos_start = var_name_token.start_pos
        self.end_start = var_name_token.end_pos       

class var_access_node:
    def __init__(self,var_token):
        self.var_name_token = var_token
        
        self.pos_start = var_token.start_pos
        self.end_start = var_token.end_pos

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
        if not res.error and self.curr_token.type != TT_EOF:
            return res.failure(InvalidSyntaxErorr(
                self.curr_token.start_pos, self.curr_token.end_pos,
                "Expected  '+', '-', '*' or '/'"
            ))

        return res
    
    def Most(self):
        res = ParserResult()
        token = self.curr_token

        if token.type in (TT_FLOAT , TT_INT):
            res.Register_advancement()
            self.advance()
            return res.Sucsses(NumberNode(token))

        if token.type is TT_IDENTIFIER:
            res.Register_advancement()
            self.advance()
            return res.Sucsses(var_access_node(token))

        elif token.type == TT_LPAREN:
            res.Register_advancement()
            self.advance()
            expr = res.Register(self.Expression())
            if res.error: return res

            if self.curr_token.type == TT_RPARENT   :
                res.Register_advancement()
                self.advance()
                return res.Sucsses(expr)
            else:
                return res.failure(InvalidSyntaxErorr(
                    self.curr_token.star_pos, self.curr_token.end_pos, 
                    "Expected ')' "
                ))
        
        return res.failure(InvalidSyntaxErorr(
            token.start_pos, token.end_pos,
            "Expected int, float, identifier, '+', '-' or '(' "
        ))

    def power(self):
        return self.bin_op(self.Most, (TT_POW,), self.Factor)

    def Factor(self):
        res = ParserResult()
        token = self.curr_token

        if token.type in (TT_PLUS, TT_MINUS):
            res.Register_advancement()
            self.advance()
            factor = res.Register(self.Factor())
            if res.error: return res
            return res.Sucsses(unaryoperationNode(token,factor))

        return self.power()

    def Term(self):
        return self.bin_op(self.Factor, (TT_MUL, TT_DIV))

    def Expression(self):
        res = ParserResult()
        if self.curr_token.matches(TT_KEYWORD, "let"):
            res.Register_advancement()
            self.advance()

            if self.curr_token.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxErorr(
                    self.curr_token.start_pos, self.curr_token.end_pos,
                    'Expected identifier'
                ))

            variable_name =  self.curr_token
            res.Register_advancement()
            self.advance()

            if self.curr_token.type != TT_EQ:
                res.failure(InvalidSyntaxErorr(
                    self.curr_token.start_pos, self.curr_token.end_pos,
                    "Expected '=' "
                ))
            res.Register_advancement()
            self.advance()
            expression = res.Register(self.Expression())
            if res.error:return res
            return res.Sucsses(var_assign_node(variable_name, expression))

        node =  res.Register(self.bin_op(self.Term, (TT_PLUS, TT_MINUS)))

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

        while self.curr_token.type in ops:
            op_tok = self.curr_token
            res.Register_advancement()
            self.advance()
            right = res.Register(func_b())
            if res.error: return res
            left = BinOpertaionNode(left, op_tok, right)

        return res.Sucsses(left)

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

    def set_position(self, pos_start = None , pos_end = None):
        self.pos_start = pos_start
        self.pos_end = pos_end

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
                    other_num.pos_start, other_num.pos_end,
                    "Division by zero",
                    self.context
                )
            return Number(self.value / other_num.value).set_context(self.context), None

    def powered(self,other_num):
        if isinstance(other_num, Number):
            return Number(self.value ** other_num.value).set_context(self.context), None    

    def copy(self):
        copy = Number(self.value)
        copy.set_position(self.pos_start,self.pos_end)
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
                node.pos_start, node.pos_end,
                f"{var_name} is not defined",
                context
            ))
        value = value.copy().set_position(node.pos_start, node.pos_end)
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
        if node.operation_token.type == TT_PLUS:
            result, error =  left.addition(right)
        
        elif node.operation_token.type == TT_MINUS:
            result, error = left.subtract(right)

        elif node.operation_token.type == TT_MUL:
            result, error =  left.multiply(right)
            
        elif node.operation_token.type == TT_DIV:
            result, error =  left.divide(right)

        elif node.operation_token.type == TT_POW:
            result, error =  left.powered(right)
    
        if error:
            return res.failure(error)
        else:
            return res.success(result.set_position(node.pos_start,node.pos_end))    
    
    def visit_unaryoperationNode(self,node,context):
        res = RuntimeResult()
        number = res.register(self.visit(node.node, context))
        if res.error: return res 

        error = None
        if node.operation_token.type == TT_MINUS:
            number, error = number.multiply(Number(-1))

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_position(node.pos_start,node.pos_end))

    def visit_NumberNode(self,node,context):
        return RuntimeResult().success(
            Number(node.token.value).set_context(context).set_position(node.pos_start,node.pos_end)
        )


global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number(0))


def Run(text: str, fn: str):
    #generate tokens
    lexer = Lexer(text, fn)
    tokens, error = lexer.make_tokens()
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
def string_with_arrows(text, pos_start, pos_end):

    result = ''

    # Calculate indices
    idx_start = max(text.rfind('\n', 0, pos_start.idx), 0)
    idx_end = text.find('\n', idx_start + 1)
    if idx_end < 0: idx_end = len(text)
    
    # Generate each line
    line_count = pos_end.line - pos_start.line + 1
    for i in range(line_count):
        # Calculate line columns
        line = text[idx_start:idx_end]
        col_start = pos_start.col if i == 0 else 0
        col_end = pos_end.col if i == line_count - 1 else len(line) - 1

        # Append to result
        result += line + '\n'
        result += ' ' * col_start + '^' * (col_end - col_start)

        # Re-calculate indices
        idx_start = idx_end
        idx_end = text.find('\n', idx_start + 1)
        if idx_end < 0: idx_end = len(text)

    return result.replace('\t', '')
