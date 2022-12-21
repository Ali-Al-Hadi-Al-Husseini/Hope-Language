from Tokenizer_tools.Token import Token
from Tokenizer_tools.Position import Position

class StringNode:
    def __init__(self,token : Token) -> None:
        self.token = token
        self.start_position = token.start_position
        self.end_position = token.end_position

    def __repr__(self) -> str:
        return str(f'{self.token}')

class NumberNode:
    def __init__(self,token : Token) -> None:
        self.token = token
        self.start_position = token.start_position
        self.end_position = token.end_position

    def __repr__(self) -> str:
        return str(f'{self.token}')

class ListNode:
    def __init__(self,elements_nodes,start_position : Position ,end_position : Position) -> None:
        self.elements_nodes = elements_nodes
        self.start_position = start_position
        self.end_position  = end_position

class ListacssesNode:
    def __init__(self, ident, index, start_position : Position,end_position : Position) -> None:
        self.ident = ident
        self.index = index
        self.start_position = start_position
        self.end_position = end_position


class unaryoperationNode:
    def __init__(self, operator_token : Token , node) -> None:
        self.operation_token = operator_token
        self.node = node
        self.start_position = operator_token.start_position
        self.end_position = node.end_position

    def __repr__(self) -> str:
        return str(f'({self.operator_token}, {self.node})')

class BinOpertaionNode:
    def __init__(self, right_node, operation_token : Token, left_node) -> None:
        self.operation_token = operation_token
        self.left_node = left_node
        self.right_node = right_node
        self.start_position = left_node.start_position
        self.end_position = right_node.end_position

    def __repr__(self) -> str:
        return str(f'( {self.left_node} {self.operation_token} {self.right_node} )')


class var_assign_node:
    def __init__(self, var_name_token, value_node,force = False) -> None:
        self.var_name_token = var_name_token
        self.value_node = value_node
        self.force = force

        self.start_position = var_name_token.start_position
        self.end_position = var_name_token.end_position       

class var_access_node:
    def __init__(self,var_token : Token) -> None:
        self.var_name_token = var_token
        
        self.start_position = var_token.start_position
        self.end_position = var_token.end_position

class IfNode:
    def __init__(self,cases, else_case) -> None:
        self.cases = cases
        self.else_case = else_case

        self.start_position = self.cases[0][0].start_position
        self.end_position = (self.else_case or self.cases[-1])[0].end_position



class ForNode():
    def __init__(self, var_name, start_value, end_value, skip_value, body, should_return_null) -> None:
        self.start_value_node = start_value
        self.end_value_node   = end_value
        self.var_name_node    = var_name
        self.skip_value_node  = skip_value
        self.body_node        = body   
        self.should_return_null = should_return_null

        self.start_position        = self.var_name_node.start_position
        self.end_position          = self.body_node.end_position

class WhileNode():
    def __init__(self, condition, body, should_return_null) -> None:
        self.condition_node =  condition
        self.body_node      = body
        self.should_return_null = should_return_null

        self.start_position        = self.condition_node.start_position
        self.end_position          = self.body_node.end_position


class functionDefNode():
    def __init__(self, var_name_token, arg_name_tokens, body_node, should_return_null) -> None:
        self.arg_name_tokens = arg_name_tokens
        self.body_node =  body_node
        self.var_name_token = var_name_token
        self.should_return_null = should_return_null


        if self.var_name_token:
            self.start_position = var_name_token.start_position
        elif len(self.arg_name_tokens) > 0:
            self.start_position = self.arg_name_tokens[0].start_position
        else:
            self.start_position = self.body_node.start_position
        
        self.end_position =  self.body_node.end_position


class CallNode:
  def __init__(self, node_to_call, arg_nodes) -> None:
    self.node_to_call = node_to_call
    self.arg_nodes = arg_nodes

    self.start_position = self.node_to_call.start_position

    if len(self.arg_nodes) > 0:
      self.end_position = self.arg_nodes[-1].end_position
    else:
      self.end_position = self.node_to_call.end_position

class ReturnNode:
    def __init__(self,node_to_return, start_position : Position, end_position : Position ) -> None:
        self.node_to_return = node_to_return
        
        self.pos_start = start_position
        self.end_position = end_position


class BreakNode:
    def __init__(self,start_position : Position,end_position : Position) -> None:
        self.pos_start = start_position
        self.end_position = end_position

class ContinueNode:
    def __init__(self,start_position : Position, end_position : Position) -> None:
        self.pos_start = start_position
        self.end_position = end_position
