from .string_with_arrows import string_with_arrows
from Tokenizer_tools.Position import Position

class Error:
    def __init__(self, start_pos: Position, end_pos: Position, error_name: str, details: str) -> None:
        self.error_name = error_name # gives the type of the error if it is syntax error  Illegal Char Error etc..
        self.details = details # what wrong with code it is like a description
        self.start_pos = start_pos
        self.end_pos = end_pos

    def as_string(self):
        result =  str(f'{self.error_name}: {self.details} \n File {self.start_pos.fn}, line {self.start_pos.line + 1}')
        result += '\n\n' + string_with_arrows(self.start_pos.ftxt, self.start_pos, self.end_pos)
        return result


class IllegalCharError(Error):
    def __init__(self,start_pos :int, end_pos: Position, details='') -> None:
        super().__init__(start_pos, end_pos, 'Illegal Character', details)


class InvalidSyntaxErorr(Error):
    def __init__(self, start_pos: Position, end_pos: Position, details= '') -> None:
        super().__init__(start_pos, end_pos, "Invalid Syntax", details)


class Indexerror(Error):
    def __init__(self, start_pos: Position, end_pos: Position, details= '') -> None:
        super().__init__(start_pos, end_pos, "Invalid index", details)


class RunTimeError(Error):
    def __init__(self, start_pos: Position, end_pos: Position, details,context) -> None:
        super().__init__(start_pos, end_pos, "Runtime Error", details)
        self.context = context

    def as_string(self):
        result =  str(f'{self.error_name}: {self.details} \n File {self.start_pos.fn}, line {self.start_pos.line + 1}')
        result += '\n\n' + string_with_arrows(self.start_pos.ftxt, self.start_pos, self.end_pos)
        return result


class ExpectedCharError(Error):
    def __init__(self, start_pos: Position, end_pos: Position, error_name: str, details: str) -> None:
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

# s = RunTimeError(Position(0,0,0,'a','a'),Position(0,0,0,'a','a'),'asdasd','adsadsadsa')
# print(isinstance(s,RunTimeError))