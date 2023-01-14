from .context_and_symbol_table import * 
from ..Errors_tools.Errors import *


class Value():
    def __init__(self):
        self.set_position()
        self.set_context()

    def set_position(self, start_position=None, end_position=None):
        self.start_position = start_position
        self.end_position = end_position
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


    def copy(self):
        raise Exception('No copy method defined')

    def is_true(self):
        return False

    def illegal_operation(self, other=None):
        if not other: other = self
        return RunTimeError(
            self.start_position, other.end_position,
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
        copy.set_position(self.start_position, self.end_position)
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

    def __len__(self):
        return len(self.elements)
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
    #             other.start_position, other.end_position,
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
    #             return None, RunTimeError(
    #                 other.start_position, other.end_position,
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
        cop.set_position(self.start_position, self.end_position)
        cop.set_context(self.context)
        return cop

class Number(Value):
    def __init__(self, value)-> None:
        super().__init__()
        self.value = value
        if type(value) == Number:
            value = value.value
            self.value = value
    
        if type(value) == str:
            if (float(value) % 1) != 0:
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
                return None, RunTimeError(
                    other.start_position, other.end_position,
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
        copy.set_position(self.start_position, self.end_position)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return self.value != 0

    def __repr__(self):
        return str(self.value)
        
Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)



