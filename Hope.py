DIGITS = '0123456789'
TT_INT = 'TT_INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS' 
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPARENT = 'RPAREN'
TT_EOF = 'EOF'

class Error:
    def __init__(self, pos_start, pos_end, error_name, details) -> None:
        self.error_name = error_name
        self.details = details
        self.pos_start = pos_start
        self.pos_end = pos_end

    def as_string(self):
        result =  f'{self.error_name}: {self.details} \n File {self.pos_start.fn}, line {self.pos_start.line + 1}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

class IllegalCharError(Error):
    def __init__(self,pos_start, pos_end, details='') -> None:
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

class InavlidSyntaxErorr(Error):
    def __init__(self, pos_start, pos_end, details= '') -> None:
        super().__init__(pos_start, pos_end, "Invalid Syntax", details)

class Position:
    def __init__(self, idx, line, col, fn, ftxt) -> None:
        self.idx = idx
        self.line = line
        self.col = col
        self.fn = fn    
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.line += 1
            self.col = 0
        return self

    def copy(self):
        return Position(self.idx, self.line, self.col,self.fn,self.ftxt)


class Token():
    def __init__(self, _type, value=None, start_pos=None, end_pos=None) -> None:
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


class Lexer:
    def __init__(self, text, fn) -> None:
        self.fn = fn
        self.text = text
        self.position = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.position.advance(self.current_char )
        self.current_char = self.text[self.position.idx] if self.position.idx < len(
            self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:

            if self.current_char in ' \t':
                self.advance()

            elif self.current_char in DIGITS:
                tokens.append(self.make_number())

            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, start_pos=self.position))
                self.advance()

            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, start_pos=self.position))
                self.advance()

            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, start_pos=self.position))
                self.advance()

            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, start_pos=self.position))
                self.advance()

            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, start_pos=self.position))
                self.advance()

            elif self.current_char == ')':
                tokens.append(Token(TT_RPARENT, start_pos=self.position))
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

class NumberNode:
    def __init__(self,token) -> None:
        self.token = token

    def __repr__(self) -> str:
        return f'{self.token}'

class unaryoperationNode:
    def __init__(self, operator_token , node) -> None:
        self.operator_token = operator_token
        self.node = node

    def __repr__(self) -> str:
        return f'({self.operator_token}, {self.node})'

class BinOpertaionNode:
    def __init__(self, right_node, opertaion, left_node) -> None:
        self.operation = opertaion
        self.left_node = left_node
        self.right_node = right_node

    def __repr__(self) -> str:
        return f'( {self.left_node} {self.operation} {self.right_node} )'
    

class ParserResult:
    def __init__(self) -> None:
        self.error = None
        self.node = None
    
    def Register(self,res):
        if isinstance(res, ParserResult):
            if res.error:self.error = res.error
            return  res.node
        return res

    def Sucsses(self,node):
        self.node = node
        return self

    def failure(self, error):
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
            return res.failure(InavlidSyntaxErorr(
                self.curr_token.start_pos, self.curr_token.end_pos,
                "Expected  '+', '-', '*' or '/'"
            ))

        return res

    def Factor(self):
        res = ParserResult()
        token = self.curr_token

        if token.type in (TT_PLUS, TT_MINUS):
            res.Register(self.advance())
            factor = res.Register(self.Factor())
            if res.error: return res
            return res.Sucsses(unaryoperationNode(token,factor))
             
        elif token.type in (TT_FLOAT , TT_INT):
            res.Register(self.advance())
            return res.Sucsses(NumberNode(token))

        elif token.type == TT_LPAREN:
            res.Register(self.advance())
            expr = res.Register(self.Expression())
            if res.error: return res

            if self.curr_token.type == TT_RPARENT   :
                res.Register(self.advance())
                return res.Sucsses(expr)
            else:
                return res.failure(InavlidSyntaxErorr(
                    self.curr_token.star_pos, self.curr_token.end_pos, 
                    "Expected ')' "
                ))
            
        
            

        return res.failure(InavlidSyntaxErorr(token.start_pos, token.end_pos, "Expected float or int"))

    def Term(self):
        res = ParserResult()
        left = res.Register(self.Factor())

        if res.error:return res
        while self.curr_token.type in (TT_MUL, TT_DIV):
            operation_token = self.curr_token
            res.Register(self.advance())
            right = res.Register(self.Factor())
            if res.error:return res
            left = BinOpertaionNode(left,operation_token, right)

        return res.Sucsses(left)

    def Expression(self):
        res = ParserResult()
        left = res.Register(self.Term())

        if res.error:return res
        while self.curr_token.type in (TT_MINUS, TT_PLUS ):
            operation_token = self.curr_token
            res.Register(self.advance())
            right = res.Register(self.Term())
            if res.error:return res
            left = BinOpertaionNode(left,operation_token, right)

        return res.Sucsses(left)

        
        


def Run(text, fn):
    #generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:return None ,error
    # generate Ast
    parser = Parser(tokens)
    ast = parser.parse()
    return ast.node, ast.error

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

