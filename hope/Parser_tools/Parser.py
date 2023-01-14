from ..Tokenizer_tools.tokens import *
from ..Errors_tools.Errors import *

from .Parser_Result import ParserResult
from .Nodes import * 
from typing import List

class Parser:
    def __init__(self,Tokens : List[Token] ) -> None:
        self.tokens = Tokens
        self.tok_idx = - 1 
        self.Current_Token = None
        self.advance()
    
    def advance(self) -> Token:
        self.tok_idx += 1
        if self.tok_idx >= 0 and self.tok_idx < len(self.tokens):
            self.Current_Token = self.tokens[self.tok_idx]

        return self.Current_Token

    def reverse(self, amount=1) -> Token:
        self.tok_idx  -= amount
        if self.tok_idx >= 0 and self.tok_idx < len(self.tokens):
            self.Current_Token = self.tokens[self.tok_idx]

        return self.Current_Token


    def parse(self) -> ParserResult:
        Result = self.Get_Statements()
        if  not Result.error and self.Current_Token.type != TOKEN_EOF:
            return Result.failure(InvalidSyntaxErorr(
                self.Current_Token.start_position, self.Current_Token.end_position,
                "Expected  '+', '-', '*' , '/'  or any other operation"
            ))

        return Result

    def Get_Statements(self) -> ParserResult:
        Result = ParserResult()

        statements = []
        start_position = self.Current_Token.start_position.copy()

        while self.Current_Token.type  == TOKEN_NEWLINE:
            self.Register_Advancement(Result)

        # adds the first statment to statements list
        Statement = Result.Register(self.get_statement())
        if  Result.error: return Result

        statements.append(Statement)
        more_statments = True

        # checking for more statements 
        while True:
            new_line_count = 0
            while self.Current_Token.type == TOKEN_NEWLINE:
                self.Register_Advancement(Result)
                new_line_count += 1
            
            if new_line_count == 0:
                more_statments = False

            if not more_statments:  break
            Statement = Result.try_Register(self.get_statement())

            if not Statement:
                self.reverse(Result.to_reverse_count)
                more_statments = False
                continue

            statements.append(Statement)

        # self.Register_Advancement(Result)
        return Result.Sucsses(
            ListNode(statements,
            start_position,
            self.Current_Token.end_position.copy())
        )

    # get statement  such as return continue or break
    def get_statement(self) -> ParserResult:
        Result = ParserResult()
        start_position = self.Current_Token.start_position.copy()


        if self.Current_Token.matches(TOKEN_KEYWORD, 'return'):
            self.Register_Advancement(Result)

            expression = Result.try_Register(self.Expression())
            if not expression:
                self.reverse(Result.to_reverse_count)
            return Result.Sucsses(ReturnNode(expression, start_position, self.Current_Token.start_position.copy()))
        
        if self.Current_Token.matches(TOKEN_KEYWORD, 'continue'):
            self.Register_Advancement(Result)
            return Result.Sucsses(ContinueNode(start_position, self.Current_Token.start_position.copy()))

        if self.Current_Token.matches(TOKEN_KEYWORD, 'break'):
            self.Register_Advancement(Result)
            return Result.Sucsses(BreakNode(start_position, self.Current_Token.start_position.copy())) 


        expression = Result.Register(self.Expression())
        if  Result.error:return Result.failure(InvalidSyntaxErorr(start_position,self.Current_Token.start_position.copy(),
         "Expected 'let', int, float, identifier, keyword,  '+', '-' or '(' "
        ))

        return Result.Sucsses(expression)

    def call(self) -> ParserResult:
        Result = ParserResult()
        most = Result.Register(self.Most())
        if  Result.error:return Result

        if self.Current_Token.type == TOKEN_LPAREN:
            self.Register_Advancement(Result)
            argument_nodes = []

            if self.Current_Token.type == TOKEN_RPARENT:
                self.Register_Advancement(Result)

            else:
                argument_nodes.append(Result.Register(self.Expression()))

                if  Result.error:
                    return Result.failure(InvalidSyntaxErorr(
                        self.Current_Token.start_position, self.Current_Token.end_position,
                        "Expected ')' , keyword, identifier, or values "
                    ))
                
                while self.Current_Token.type == TOKEN_COMMA:
                    self.Register_Advancement(Result)

                    argument_nodes.append(Result.Register(self.Expression()))
                    if  Result.error: return Result

                if self.Current_Token.type != TOKEN_RPARENT:
                    return Result.failure(InvalidSyntaxErorr(
                        self.Current_Token.start_position, self.Current_Token.end_position,
                        "Expected ',' or ')'"
                    ))


                self.Register_Advancement(Result)
            return Result.Sucsses(CallNode(most,argument_nodes))
        return Result.Sucsses(most)

# to understand the order of this reader grammers in the top of the file
    def Most(self) -> ParserResult:
        Result = ParserResult()
        token = self.Current_Token


        if token.type in (TOKEN_FLOAT , TOKEN_INT):
            self.Register_Advancement(Result)
            return Result.Sucsses(NumberNode(token))

        elif token.type == TOKEN_STRING:
            self.Register_Advancement(Result)
            return Result.Sucsses(StringNode(token))

        # Checking for identifier node
        elif token.type is TOKEN_IDENTIFIER:
            self.Register_Advancement(Result)
            identifier = token.value
            
            if self.Current_Token.type == TOKEN_EQ:
                self.Register_Advancement(Result)
                
                new_value = Result.Register(self.Expression())
                if  Result.error:return Result

                return Result.Sucsses(var_assign_node(token,new_value))

            # checking for list or string index subscription
            elif self.Current_Token.type == TOKEN_LSQUARE:
                self.Register_Advancement(Result)
                
                # checking index token 
                if self.Current_Token.type in (TOKEN_INT, TOKEN_IDENTIFIER):
                    index = self.Current_Token
                    self.Register_Advancement(Result)


                    if self.Current_Token.type != TOKEN_RSQUARE:
                        Result.failure(InvalidSyntaxErorr(index.start_position,index.end_position,
                                                       f"Expected ']' after index {index.value}"))
                        return Result

                    end_position = self.Current_Token.end_position.copy()
                    self.Register_Advancement(Result)

                    return Result.Sucsses(ListacssesNode(identifier, index.value, token.start_position.copy(), end_position))

                else:
                    Result.failure(InvalidSyntaxErorr(self.Current_Token.start_position,self.Current_Token.end_position,
                                                    f"Expected index (integer or identifier) after [ "))
                    return Result                    

            return Result.Sucsses(var_access_node(token))


        elif token.type == TOKEN_LPAREN:
            self.Register_Advancement(Result)

            expression = Result.Register(self.Expression())
            if  Result.error: return Result

            if self.Current_Token.type == TOKEN_RPARENT   :
                self.Register_Advancement(Result)
                return Result.Sucsses(expression)
            else:
                return Result.failure(InvalidSyntaxErorr(
                    self.Current_Token.start_position, self.Current_Token.end_position, 
                    "Expected ')' "
                ))


        elif token.type == TOKEN_LSQUARE:
            expression = Result.Register(self.list_expression())
            if  Result.error:return Result
            return Result.Sucsses(expression)

        elif token.matches(TOKEN_KEYWORD, 'if'):
            expression = Result.Register(self.If_expression())
            if  Result.error: return Result
            return Result.Sucsses(expression)

        elif token.matches(TOKEN_KEYWORD, 'while'):
            expression = Result.Register(self.While_expression())
            if  Result.error: return Result
            return Result.Sucsses(expression)

        elif token.matches(TOKEN_KEYWORD, 'for'):
            expression = Result.Register(self.For_expression())
            if  Result.error: return Result
            return Result.Sucsses(expression)

        elif token.matches(TOKEN_KEYWORD, 'func'):
            expression = Result.Register(self.Func_expression())
            if  Result.error: return Result
            return Result.Sucsses(expression)

        
        return Result.failure(InvalidSyntaxErorr(
            token.start_position, token.end_position,
            "Expected int, float, identifier, '+', '-' , '('  or '[' "
        ))

    def power(self) -> ParserResult:
        return self.binary_operation(self.call, (TOKEN_POW,), self.Factor)

    def Factor(self) -> ParserResult:
        Result = ParserResult()
        token = self.Current_Token

        if token.type in (TOKEN_PLUS, TOKEN_MINUS):
            self.Register_Advancement(Result)
            factor = Result.Register(self.Factor())
            if  Result.error: return Result

            return Result.Sucsses(unaryoperationNode(token,factor))

        return self.power()

    def Term(self) -> ParserResult:
        return self.binary_operation(self.Factor, (TOKEN_MUL, TOKEN_DIV,TOKEN_MODULE))
    
    def arithmetic_expression(self) -> ParserResult:
        return self.binary_operation(self.Term, (TOKEN_PLUS, TOKEN_MINUS))

    def Comparison_expression(self) -> ParserResult:
        Result = ParserResult()

        if self.Current_Token.matches(TOKEN_KEYWORD, "not"):
            operation_token = self.Current_Token

            self.Register_Advancement(Result)
            node  = Result.Register(self.Comparison_expression())
            if  Result.error :return Result

            return Result.Sucsses(unaryoperationNode(operation_token,node))


        node = Result.Register(self.binary_operation(self.arithmetic_expression,(TOKEN_EE, TOKEN_NE, TOKEN_LT, TOKEN_GT, TOKEN_GTE, TOKEN_LTE)))
        if  Result.error: 
            return Result.failure(InvalidSyntaxErorr(
            self.Current_Token.start_position, self.Current_Token.end_position,
            "Expected int, float, identifier, keyword, function call, '+', '-' , '(' , '[' or 'not' "
        ))

        return Result.Sucsses(node)

    def Expression(self) -> ParserResult:
        Result = ParserResult()

        while self.Current_Token.type  == TOKEN_NEWLINE:
            self.Register_Advancement(Result)

        # checks for variable declaration
        if self.Current_Token.matches(TOKEN_KEYWORD, "let"):
            self.Register_Advancement(Result)

            if self.Current_Token.type != TOKEN_IDENTIFIER:
                return Result.failure(InvalidSyntaxErorr(
                    self.Current_Token.start_position, self.Current_Token.end_position,
                    f'Expected identifier found {self.Current_Token.type} \'{self.Current_Token.value}\''
                ))

            variable_name =  self.Current_Token

            self.Register_Advancement(Result)
            if self.Current_Token.type != TOKEN_EQ:
                return Result.failure(InvalidSyntaxErorr(
                    self.Current_Token.start_position, self.Current_Token.end_position,
                    f"Expected '=' found {self.Current_Token.type} \'{self.Current_Token.value}\' "
                ))
                
            self.Register_Advancement(Result)
            expression = Result.Register(self.Expression())
            if  Result.error:return Result

            return Result.Sucsses(var_assign_node(variable_name, expression,True))


        node =  Result.Register(self.binary_operation(self.Comparison_expression, ((TOKEN_KEYWORD,"and"),  (TOKEN_KEYWORD, "or"))))
        if  Result.error: 
            return Result.failure(InvalidSyntaxErorr(
                self.Current_Token.start_position, self.Current_Token.end_position,
                "Expected 'let', int, float, identifier, '+', '-' or '(' "
            ))

        return Result.Sucsses(node)

    def binary_operation(self, func_a, ops,func_b= None) -> ParserResult:
        if func_b == None:
            func_b = func_a
        
        Result = ParserResult()
        left = Result.Register(func_a())
        if  Result.error: return Result

        while self.Current_Token.type in ops or (self.Current_Token.type,self.Current_Token.value) in ops:
            operation_token = self.Current_Token
            self.Register_Advancement(Result)

            right = Result.Register(func_b())
            if  Result.error: return Result

            left = BinOpertaionNode(left, operation_token, right)

        return Result.Sucsses(left)

    def If_expression(self) -> ParserResult:
        Result = ParserResult()

        temp  = Result.Register(self.if_elif_maker('if'))
        if  Result.error:return Result

        new_cases, else_case = temp
        return Result.Sucsses(IfNode(new_cases, else_case))

    def if_elif_maker(self,keyword : str) -> ParserResult:
        Result = ParserResult()
        cases = []
        else_case = None

        
        if not self.Current_Token.matches(TOKEN_KEYWORD, keyword):
            return Result.error(InvalidSyntaxErorr(
                self.Current_Token.start_position, self.Current_Token.end_position,
                str(f"Expected {keyword}")
            ))

        self.Register_Advancement(Result)
        
        # gets condition  after if or elif keyword 
        condition  = Result.Register(self.Expression())
        if  Result.error : return Result

        if not self.Current_Token.type == TOKEN_START:
            return Result.failure(InvalidSyntaxErorr(
                self.Current_Token.start_position, self.Current_Token.end_position,
                f"Expected '>>' found {self.Current_Token.type} \'{self.Current_Token.value}\'"
            ))
        
        self.Register_Advancement(Result)

        if self.Current_Token.type == TOKEN_NEWLINE:
            self.Register_Advancement(Result)

            statements = Result.Register(self.Get_Statements())
            if  Result.error: return Result
            cases.append((condition, statements,True))

            if self.Current_Token.type == TOKEN_END:
                self.Register_Advancement(Result)

            else:
                all_cases = Result.Register(self.elif_else_expression())
                if  Result.error : return Result
                new_cases, else_case  = all_cases
                cases.extend(new_cases )
        else:
            expression = Result.Register(self.get_statement())
            if  Result.error : return Result
            cases.append((condition, expression, False))

            all_cases = Result.Register(self.elif_else_expression())
            if  Result.error: return Result

            new_cases, else_case  = all_cases
            cases.extend(new_cases)

        return Result.Sucsses(
                (cases, else_case)
        )

    def elif_expression(self) -> ParserResult:
        return self.if_elif_maker('elif')

    def else_expression(self) -> ParserResult:
        Result = ParserResult()
        else_case = None

        if self.Current_Token.matches(TOKEN_KEYWORD, 'else'):
            self.Register_Advancement(Result)
            
            if self.Current_Token.type != TOKEN_START:
                    return Result.failure(InvalidSyntaxErorr(
                        self.Current_Token.start_position, self.Current_Token.end_position,
                        f"Expected '>>' found {self.Current_Token.type} \'{self.Current_Token.value}\'"
                    ))
            
            self.Register_Advancement(Result)
            if self.Current_Token.type == TOKEN_NEWLINE:
                self.Register_Advancement(Result)

                statements = Result.Register(self.Get_Statements())
                if  Result.error: return Result

                else_case  = (statements,True)

                if self.Current_Token.type == TOKEN_END:
                    self.Register_Advancement(Result)

                else:
                    return Result.failure(InvalidSyntaxErorr(
                        self.Current_Token.start_position, self.Current_Token.end_position,
                        f"Expected '<<' found {self.Current_Token.type} \'{self.Current_Token.value}\'"
                    ))
            else:
                expression = Result.Register(self.get_statement())
                if  Result.error : return Result
                else_case = (expression, False)

        return Result.Sucsses(
            else_case
        )
    
    def elif_else_expression(self) -> ParserResult:
        Result = ParserResult()
        cases, else_case = [], None

        if self.Current_Token.matches(TOKEN_KEYWORD, "elif"):
            all_cases = Result.Register(self.elif_expression())
            if  Result.error : return Result
            cases, else_case = all_cases
        
        else:
            else_case = Result.Register(self.else_expression())
            if  Result.error: return Result

        return Result.Sucsses((cases,else_case))
            

    def Register_Advancement(self,Result) -> None:
        Result.Register_Advancement()
        self.advance()


    def ListCall_expression(self) -> None:
        _  = ParserResult()
        _ = self.Current_Token.value
        self.Register_Advancement()

    def For_expression(self) -> ParserResult:
        Result = ParserResult()

        self.Register_Advancement(Result)

        if self.Current_Token.type != TOKEN_IDENTIFIER:
            return Result.failure(InvalidSyntaxErorr(
                self.Current_Token.start_position , self.Current_Token.end_position,
                f"Expected Identifier after For loop declartion found {self.Current_Token.type} \'{self.Current_Token.value}\'"
            ))

        pointer_name = self.Current_Token
        self.Register_Advancement(Result)
        
        if self.Current_Token.type != TOKEN_EQ:
            return Result.failure(InvalidSyntaxErorr(
                self.Current_Token.start_position , self.Current_Token.end_position,
                f"Expected '=' after identifier found {self.Current_Token.type} \'{self.Current_Token.value}\'"
            ))

        self.Register_Advancement(Result)
        starting_pointer = Result.Register(self.Expression())      
        if  Result.error: return Result

        if self.Current_Token.type != TOKEN_ARROW:
            return Result.failure(InvalidSyntaxErorr(
                self.Current_Token.start_position , self.Current_Token.end_position,
                f"Expected '->'  found {self.Current_Token.type} \'{self.Current_Token.value}\' "
            ))

        self.Register_Advancement(Result) 

        end_poniter = Result.Register(self.Expression())
        if  Result.error: return Result
        skip_value = None
        if self.Current_Token.matches(TOKEN_KEYWORD,'skip'):
            self.Register_Advancement(Result)
            skip_value = Result.Register(self.Expression())

            if  Result.error :return Result

        if not self.Current_Token.type == TOKEN_START :
           return Result.failure(InvalidSyntaxErorr(
                self.Current_Token.start_position , self.Current_Token.end_position,
                f"Expected '>>' found {self.Current_Token.type} \'{self.Current_Token.value}\' "
            ))           
        
        self.Register_Advancement(Result)
        if self.Current_Token.type == TOKEN_NEWLINE:
            self.Register_Advancement(Result)

            body_content = Result.Register(self.Get_Statements())
            if  Result.error: return Result

            if not self.Current_Token.type == TOKEN_END:
                return Result.failure(InvalidSyntaxErorr(
                    self.Current_Token.start_position, self.Current_Token.end_position,
                    f"Expected '<<'  found {self.Current_Token.type}"
                ))

            self.Register_Advancement(Result)
            
            return Result.Sucsses(ForNode(pointer_name, starting_pointer,end_poniter,skip_value, body_content,True))

        body_content = Result.Register(self.get_statement())
        if  Result.error: return Result
        
        return Result.Sucsses(ForNode(pointer_name, starting_pointer,end_poniter,skip_value, body_content,False))
     
    def While_expression(self) -> ParserResult:
        Result = ParserResult()

        self.Register_Advancement(Result)
        condition = Result.Register(self.Expression())
        if  Result.error: return Result

        if self.Current_Token.type != TOKEN_START:
               return Result.failure(InvalidSyntaxErorr(
                self.Current_Token.start_position , self.Current_Token.end_position,
                f"Expected '>>'  found {self.Current_Token.type} \'{self.Current_Token.value}\' "

            ))  

        self.Register_Advancement(Result)

        if self.Current_Token.type == TOKEN_NEWLINE:
            self.Register_Advancement(Result)

            body_content = Result.Register(self.Get_Statements())
            if  Result.error: return Result

            if not self.Current_Token.type == TOKEN_END:
                return Result.failure(InvalidSyntaxErorr(
                    self.Current_Token.start_position, self.Current_Token.end_position,
                    "Expected '<<'"
                ))
            self.Register_Advancement(Result)
            return Result.Sucsses(WhileNode(condition,body_content, True))
        body_content = Result.Register(self.get_statement())
        if  Result.error: return Result

        return Result.Sucsses(WhileNode(condition, body_content,False))

    def Func_expression(self) -> ParserResult:
        Result = ParserResult()

        self.Register_Advancement(Result)

        if self.Current_Token.type == TOKEN_IDENTIFIER:
            func_name_token = self.Current_Token
            self.Register_Advancement(Result)

            if self.Current_Token.type != TOKEN_LPAREN:
                return Result.failure(InvalidSyntaxErorr(
                    self.Current_Token.start_position, self.Current_Token.end_position,
                    f"Expected '(' after function declaration  found {self.Current_Token.type} \'{self.Current_Token.value}\'"
                ))

        else:
            func_name_token = None
            if self.Current_Token.type != TOKEN_LPAREN:
                return Result.failure(InvalidSyntaxErorr(
                    self.Current_Token.start_position, self.Current_Token.end_position,
                    f"Expected identifier after function declaration  found {self.Current_Token.type} \'{self.Current_Token.value}\'"
                ))
        
        self.Register_Advancement(Result)

        arg_name_tokens = []

        if self.Current_Token.type == TOKEN_IDENTIFIER:
            arg_name_tokens.append(self.Current_Token)
            self.Register_Advancement(Result)

            while self.Current_Token.type == TOKEN_COMMA:
                self.Register_Advancement(Result)

                if self.Current_Token.type != TOKEN_IDENTIFIER:
                    return Result.failure(InvalidSyntaxErorr(
                        self.Current_Token.start_position, self.Current_Token.end_position,
                        f"Expected identifier  found {self.Current_Token.type} \'{self.Current_Token.value}\'"
                    ))
                arg_name_tokens.append(self.Current_Token)
                self.Register_Advancement(Result)

            if self.Current_Token.type != TOKEN_RPARENT:
                    return Result.failure(InvalidSyntaxErorr(
                    self.Current_Token.start_position, self.Current_Token.end_position,
                    f"Expected ')' or ','  after function declaration found {self.Current_Token.type} \'{self.Current_Token.value}\'"
                ))

        else:
            if self.Current_Token.type != TOKEN_RPARENT:
                return Result.failure(InvalidSyntaxErorr(
                        self.Current_Token.start_position, self.Current_Token.end_position,
                        f"Expected ')' or  identifier after function declaration found {self.Current_Token.type} \'{self.Current_Token.value}\'"
                    ))
        self.Register_Advancement(Result)
            
        if self.Current_Token.type != TOKEN_START:
            return Result.failure(InvalidSyntaxErorr(
                    self.Current_Token.start_position, self.Current_Token.end_position,
                    f"Expected '>>' found {self.Current_Token.type} \'{self.Current_Token.value}\' "
                ))

        self.Register_Advancement(Result)

        if self.Current_Token.type != TOKEN_NEWLINE:##
            
            body = Result.Register(self.Expression())
            if  Result.error:return Result

            return Result.Sucsses(functionDefNode(func_name_token, arg_name_tokens, body,True))

        self.Register_Advancement(Result)
        
        while self.Current_Token.type == TOKEN_NEWLINE:
            self.Register_Advancement(Result)

        body = Result.Register(self.Get_Statements())
        if  Result.error:return Result

        if not self.Current_Token.type == TOKEN_END:
            return Result.failure(InvalidSyntaxErorr(
                self.Current_Token.start_position,self.Current_Token.end_position,
                f"Expected '<<' found {self.Current_Token.type} \'{self.Current_Token.value}\'"
            ))
        self.Register_Advancement(Result)

        return Result.Sucsses(
            functionDefNode(
                func_name_token,
                arg_name_tokens,
                body,
                False
            )
        )
    
    def list_expression(self) -> ParserResult:
        Result = ParserResult()
        elements_nodes = []
        start_position = self.Current_Token.start_position.copy()

        self.Register_Advancement(Result)

        if self.Current_Token.type == TOKEN_RSQUARE:
            self.Register_Advancement(Result) 
        else:
            elements_nodes.append(Result.Register(self.Expression()))
            if  Result.error:
                return Result.failure(InvalidSyntaxErorr(
                    self.Current_Token.start_position, self.Current_Token.end_position,
                    f"Expected ']' , keyword, identifier  or values found {self.Current_Token.type} \'{self.Current_Token.value}\'"
                ))
            
            while self.Current_Token.type == TOKEN_COMMA:
                self.Register_Advancement(Result)

                elements_nodes.append(Result.Register(self.Expression()))
                if  Result.error: return Result

            if self.Current_Token.type != TOKEN_RSQUARE:
                return Result.failure(InvalidSyntaxErorr(
                    self.Current_Token.start_position, self.Current_Token.end_position,
                    f"Expected ',' or ']' found {self.Current_Token.type} \'{self.Current_Token.value}\'"
                ))

            self.Register_Advancement(Result)
        
        return Result.Sucsses(ListNode(elements_nodes, start_position, self.Current_Token.end_position.copy()))
