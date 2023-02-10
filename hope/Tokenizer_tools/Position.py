class Position:
    def __init__(self, idx: int, line: int, col: int, fn: str, ftxt: str) -> None:
        
        self.idx = idx
        self.line = line
        self.col = col
        self.fn = fn    # file name
        self.ftxt = ftxt # file text
        
    
    def advance(self, current_character : str = None) -> 'Position':
        self.idx += 1
        self.col += 1

        if current_character == '\n':
            self.line += 1
            self.col = 0

        return self

    def copy(self) -> 'Position':
        return Position(self.idx, self.line, self.col,self.fn,self.ftxt)

