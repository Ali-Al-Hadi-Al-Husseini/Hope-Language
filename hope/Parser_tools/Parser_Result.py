class ParserResult:
    def __init__(self) -> None:
        self.error = None
        self.node = None
        self.last_registered_Advance_count = 0
        self.to_reverse_count = 0
        self.advance_count = 0


    def Register_Advancement(self) -> None:
        self.last_registered_Advance_count = 1
        self.advance_count += 1


    def Register(self,result: 'ParserResult'):
        self.last_registered_Advance_count = result.advance_count
        self.advance_count += result.advance_count

        if  result.error:self.error = result.error
        return  result.node
        

    def Sucsses(self,node) -> 'ParserResult':
        self.node = node
        return self


    def failure(self, error) -> 'ParserResult':
        if not self.error  or self.last_registered_Advance_count  == 0:
            self.error = error
        return self


    def try_Register(self, result: 'ParserResult'):
        if  result.error:
            self.to_reverse_count = result.advance_count
            return None
        return self.Register(result)