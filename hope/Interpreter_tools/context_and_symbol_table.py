class Context:
    def __init__(self,display_name, parent=None, parent_entry_pos=None) -> None:
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table: SymbolTable = None

class SymbolTable:
    def __init__(self,parent=None) -> None:
        self.symbols = {}
        self.parent = parent

    def get(self, name: str) -> any:
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return  value

    def set(self, name: str, value: any) -> None:
        self.symbols[name] = value

    def remove(self, name:str) -> None:
        del self.symbols[name]

    def is_in(self,name: str) -> bool:
        return name  in self.symbols

    def __repr__(self) -> str:
        return '"{}"'.format(self.value)
