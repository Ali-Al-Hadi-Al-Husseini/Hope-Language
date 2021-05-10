DIGITS = '0123456789'
TT_INT = 'TT_INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPARENT = 'RPAREN'


class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.error_name = error_name
        self.details = details
        self.pos_start = pos_start
        self.pos_end = pos_end

    def as_string(self):
        return f'{self.error_name}: {self.details}'


class IllegalCharError(Error):
    def __init__(self, details):
        super().__init__('Illegal Character', details)


class Position:
    def __init__(self, idx, line, col):
        self.idx = idx
        self.line = line
        self.col = col

    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.line += 1
            self.col = 0
        return self

    def copy(self):
        return Position(self.idx, self.line, self.col)


class Token():
    def __init__(self, _type, value=None):
        self.type = _type
        self.value = value

    def __repr__(self):
        if self.value:
            return "{}:{}".format(self.type, self.value)
        return f'{self.type}'


class Lexer:
    def __init__(self, text):
        self.text = text
        self.position = Position(-1, 0, -1)
        self.current_char = None
        self.advance()

    def advance(self):
        self.position.advance()
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
                tokens.append(Token(TT_PLUS))
                self.advance()

            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()

            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()

            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()

            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()

            elif self.current_char == ')':
                tokens.append(Token(TT_RPARENT))
                self.advance()
            else:
                pos_start = self.position.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.position, "'" + char + "'")

        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0

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
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))


def Run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()
    return tokens, error
