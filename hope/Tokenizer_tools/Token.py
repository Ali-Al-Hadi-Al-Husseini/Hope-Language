from .Position import Position

class Token():
    def __init__(self, _type: str, value=None, start_position: Position = None, end_position: Position = None) -> None:
        self.type = _type
        self.value = value

        if start_position:
            self.start_position = start_position.copy()
            self.end_position = start_position.copy()
            self.end_position.advance()

        if end_position:
            self.end_position = end_position.copy()


    def __repr__(self) -> str:
        if self.value:
            return "{}:{}".format(self.type, self.value)
        return str(f'{self.type}')


    def matches(self, _type, value : str) -> bool:
        return self.type == _type and self.value == value
