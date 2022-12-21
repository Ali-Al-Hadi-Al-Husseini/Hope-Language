
from .Functions_and_Runtime_Result import Function,BaseFunction,RuntimeResult

from Errors_tools.Errors import *
from Tokenizer_tools.tokens import  *

from .context_and_symbol_table import *
from .Types import *

from .levenshtein_distance import find_closest_to_string
import turtle


class Interpreter:
    def __init__(self) -> None:
        self.Built_in_identifiers = set(global_symbol_table.symbols.keys())

    def visit(self,node, context : Context):
        method_name = str(f"visit_{type(node).__name__}")
        method = getattr(self,method_name,self.no_visit_method)
        return method(node,context) 
    
    def no_visit_method(self,node, context : Context):
        raise Exception(str(f"No visit_{type(node).__name__} method defined"))

    def visit_var_access_node(self, node, context : Context):
        Result = RuntimeResult()
        var_name = node.var_name_token.value
        value = context.symbol_table.get(var_name) 

        if not value:
            closest_identifier = find_closest_to_string(var_name,context,global_symbol_table,[])
            if closest_identifier is not None:
                return Result.failure(RunTimeError(
                    node.start_position, node.end_position,
                    str(f"{var_name} is not defined did you mean \'{closest_identifier}\'?"),
                    context
                ))
            return Result.failure(RunTimeError(
                    node.start_position, node.end_position,
                    str(f"{var_name} is not defined"),
                    context
                ))
        value = value.copy().set_position(node.start_position, node.end_position).set_context(context)
        return Result.success(value)

    def visit_StringNode(self,node,context : Context):
        return RuntimeResult().success(
            String(node.token.value).set_context(context).set_position(node.start_position,node.end_position)
        )    

    def visit_var_assign_node(self, node, context : Context):
        Result = RuntimeResult()
        var_name = node.var_name_token.value
        value = Result.Register(self.visit(node.value_node,context))

        if  Result.should_return():return Result

        if global_symbol_table.is_in(var_name)  or node.force:
            global_symbol_table.set(var_name,value)
            
        else:
            closest_identifier = find_closest_to_string(var_name,context,global_symbol_table,self.Built_in_identifiers)
            if closest_identifier is not None:
                return Result.failure(InvalidSyntaxErorr(
                    node.start_position, node.end_position,
                    str(f"Variable '{var_name}' refernced before assignment did you mean {closest_identifier}?")
                ))
            return  Result.failure(InvalidSyntaxErorr(
                    node.start_position, node.end_position,
                    str(f"Variable '{var_name}' refernced before assignment")
                ))
            
        return Result.success(value) 

    def visit_BinOpertaionNode(self, node,context : Context):
        Result = RuntimeResult()
        left = Result.Register(self.visit(node.right_node,context))
        if  Result.should_return(): return Result
        right = Result.Register(self.visit(node.left_node, context))
        if  Result.should_return(): return Result
        
        result = None
        error = None
        if node.operation_token.type == TOKEN_PLUS:
            result, error =  left.addition(right)
        
        elif node.operation_token.type == TOKEN_MINUS:
            result, error = left.subtract(right)

        elif node.operation_token.type == TOKEN_MUL:
            result, error =  left.multiply(right)

        elif node.operation_token.type == TOKEN_MODULE:
            result, error = left.module(right)

        elif node.operation_token.type == TOKEN_DIV:
            result, error =  left.divide(right)

        elif node.operation_token.type == TOKEN_POW:
            result, error =  left.powered(right)

        elif node.operation_token.type == TOKEN_EE:
            result, error =  left.get_EE(right)

        elif node.operation_token.type == TOKEN_NE:
            result, error =  left.get_NE(right)

        elif node.operation_token.type == TOKEN_GT:
            result, error =  left.get_GT(right)

        elif node.operation_token.type == TOKEN_LT:
            result, error =  left.get_LT(right)

        elif node.operation_token.type == TOKEN_GTE:
            result, error =  left.get_GTE(right)
        
        elif node.operation_token.type == TOKEN_LTE:
            result, error =  left.get_LTE(right)
        
        elif node.operation_token.matches(TOKEN_KEYWORD,"and"):
            result, error =  left.and_with(right)
        
        elif node.operation_token.matches(TOKEN_KEYWORD, "or"):
            result, error =  left.or_with(right)


        if error:
            return Result.failure(error)
        else:
            return Result.success(result.set_position(node.start_position,node.end_position))    
    
    def visit_unaryoperationNode(self,node,context : Context):
        Result = RuntimeResult()
        number = Result.Register(self.visit(node.node, context))
        if  Result.should_return(): return Result 

        error = None
        if node.operation_token.type == TOKEN_MINUS:
            number, error = number.multiply(Number(-1))

        elif node.operation_token.matches(TOKEN_KEYWORD, 'not'):
            number, error = number._not()

        if error:
            return Result.failure(error)
        else:
            return Result.success(number.set_position(node.start_position,node.end_position))

    def visit_NumberNode(self,node,context : Context):
        return RuntimeResult().success(
            Number(node.token.value).set_context(context).set_position(node.start_position,node.end_position)
        )

    def visit_IfNode(self, node, context : Context):
        Result = RuntimeResult()
        
        for condition, expression,should_return_null in node.cases:
            condition_result =  Result.Register(self.visit(condition, context))
            if  Result.should_return(): return Result

            if condition_result.is_true():
                expression_result = Result.Register(self.visit(expression, context))
                if  Result.should_return(): return Result
                return Result.success(Number.null if should_return_null else expression_result)

        if node.else_case:
            expression ,should_return_null = node.else_case
            else_value =Result.Register(self.visit(expression, context))
            if  Result.should_return(): return Result
            return Result.success(Number.null if should_return_null else else_value)
        
        return Result.success(Number.null)
    
    def visit_ForNode(self, node, context : Context):
        Result = RuntimeResult()
        elements = []
        start_pointer = Result.Register(self.visit(node.start_value_node,context))

        if  Result.should_return():return Result
        
        end_pointer = Result.Register(self.visit(node.end_value_node, context))
        if  Result.should_return():return Result
        
        skip_value = Number(1)
        if node.skip_value_node:
            skip_value = Result.Register(self.visit(node.skip_value_node,context))
            if  Result.should_return():return Result

        pointer = start_pointer.value

        def evaluate_condition():
             return pointer < end_pointer.value if skip_value.value >= 0 else pointer > end_pointer.value
             
        while evaluate_condition():
            context.symbol_table.set(node.var_name_node.value,Number(pointer))
            pointer += skip_value.value
            value = Result.Register(self.visit(node.body_node,context))
            if  Result.should_return() and Result.loop_should_continue == False and Result.loop_should_break == False: return Result

            if Result.loop_should_break:
                break
            
            if Result.loop_should_continue:
                continue

            elements.append(value)

        return Result.success(
            Number.null if node.should_return_null else 
            List(elements).set_context(context).set_position(node.start_position,node.end_position)
        )

    
    def visit_WhileNode(self, node, context : Context):
        Result = RuntimeResult()
        elements = []
        
        while True:
            condition = Result.Register(self.visit(node.condition_node, context))
            if  Result.should_return(): return Result

            if not condition.is_true(): break

            value = Result.Register(self.visit(node.body_node,context))
            if  Result.should_return() and Result.loop_should_continue == False and Result.loop_should_break == False: return Result

            if Result.loop_should_break:
                break
            
            if Result.loop_should_continue:
                continue
            
            elements.append(value)

        return Result.success(
            Number.null if node.should_return_null else
            List(elements).set_context(context).set_position(node.start_position,node.end_position)
        )


    def visit_ListNode(self,node,context : Context):
        Result = RuntimeResult()
        elements = []

        for elem in node.elements_nodes:
            elements.append(Result.Register(self.visit(elem,context)))
            if  Result.should_return() : return Result
        
        return Result.success(
            List(elements).set_context(context).set_position(node.start_position,node.end_position)
        )

    def visit_functionDefNode(self,node, context,):
        Result = RuntimeResult()
        func_name = node.var_name_token.value if node.var_name_token else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_tokens]
        func_value = Function(func_name, body_node, arg_names,node.should_return_null).set_context(context).set_position(node.start_position, node.end_position)


        if node.var_name_token:
            context.symbol_table.set(func_name, func_value)

        return Result.success(func_value)


    def visit_ReturnNode(self, node, context : Context):
        Result = RuntimeResult()
        if node.node_to_return:
            value = Result.Register(self.visit(node.node_to_return, context))
            if Result.should_return(): return Result
        else:
            value = Number.null
        
        return Result.success_return(value)

    def visit_ContinueNode(self, node, context : Context):
        return RuntimeResult().success_continue()

    def visit_BreakNode(self, node, context : Context):
        return RuntimeResult().success_break()

    def visit_ListacssesNode(self,node, context : Context):
        Result = RuntimeResult()
        list_name = node.ident
        list_values = context.symbol_table.get(list_name)
        idx =  node.index if type(node.index) == int else context.symbol_table.get(node.index).value
        
        if isinstance(list_values,List):

            if len(list_values.elements) <= idx:
                return Result.failure(Indexerror(node.start_position,node.end_position,
                                                                f"{idx} is out of range while the length of \'{list_name}\'  is { len(list_values.elements)}\n Rember that indexing start at 0"))
            return Result.success(list_values.elements[idx])
        
        elif isinstance(list_values,String):
            if len(list_values.value) <= idx:
                return Result.failure(Indexerror(node.start_position,node.end_position,
                                                                f"{idx} is out of range while the length of \'{list_name}\'  is { len(list_values.elements)}\n Rember that indexing start at 0"))

            return Result.success(String(list_values.value[idx]))
        return Result.failure(SyntaxError(node.start_position,node.end_position,
                                                                f"{type(list_values)} is not subscriptable"))

    def visit_CallNode(self, node, context : Context):
        Result = RuntimeResult()
        args = []

        value_to_call = Result.Register(self.visit(node.node_to_call, context))
        if  Result.should_return(): return Result
        value_to_call = value_to_call.copy().set_position(node.start_position, node.end_position)

        for arg_node in node.arg_nodes:
            args.append(Result.Register(self.visit(arg_node, context)))
            if  Result.should_return(): return Result

        if isinstance(value_to_call,Function):
            return_value = Result.Register(self.execute_function(value_to_call,args))
            if  Result.should_return(): return Result

        elif isinstance(value_to_call,BaseFunction):
            return_value = Result.Register(value_to_call.execute(args))
            if  Result.should_return(): return Result        

            
        return_value = return_value.copy().set_position(node.start_position, node.end_position).set_context(context)
        return Result.success(return_value)

    def execute_function(self,func, args,):
        Result = RuntimeResult()
        interpreter = Interpreter()

        if not isinstance(func,(Function,BaseFunction)):
            return Result.failure(RunTimeError(
                func.start_position, func.end_position,
                'Illegal operation',
                func.context
            ))
    
        exec_ctx = func.generate_new_context()


        Result.Register(func.check_and_populate_args(func.arg_names, args, exec_ctx))
        if  Result.should_return(): return Result

        value = Result.Register(interpreter.visit(func.body_node, exec_ctx))
        if  Result.should_return() and Result.func_return_value == None: return Result

        return_value = (value if func.should_return_null else None) or Result.func_return_value or Number.null

        return Result.success(return_value)

from Tokenizer_tools.Tokenizer import Tokenizer
from Parser_tools.Parser import Parser

from os import name,system
import time     



def run(text: str, fn: str):
    #generate tokens
    start = time.time()

    tokenizer = Tokenizer(text, fn)
    tokens, error =tokenizer.make_tokens()

    end = time.time()
    # print(f' Tokenizing took {end-start}')

    if error:return None, error
    # generate Ast
    start = time.time()

    parser = Parser(tokens)
    ast = parser.parse() # abstract syntax tree

    end = time.time()
    # print(f' Parsing took {end-start}')
    if ast.error :return None, ast.error

    start = time.time()
    
    interpreter = Interpreter()
    context = Context("<module>")
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    end = time.time()
    # print(f' interpreting took {end-start}')
    
    return result.values, result.error


class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, args):
        Result = RuntimeResult()
        exec_ctx = self.generate_new_context()

        method_name =str( f'execute_{self.name}')
        method = getattr(self, method_name, self.no_visit_method)


        Result.Register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
        if  Result.should_return(): return Result

        return_value = Result.Register(method(exec_ctx))
        if  Result.should_return(): return Result
        return Result.success(return_value)

    def no_visit_method(self, node, context : Context):
        raise Exception(str(f'No execute_{self.name} method defined'))

    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_position(self.start_position, self.end_position)
        return copy

    def __repr__(self):
        return str(f"<built-in function {self.name}>")

  #####################################

    def execute_print(self, exec_ctx : Context):
        value = exec_ctx.symbol_table.get('value')
        if type(value) == Number:
            print(value)
        else:
            print(str(value)[1:-1])
        return RuntimeResult().success(String(str(exec_ctx.symbol_table.get('value'))))
    execute_print.arg_names = ['value']

  
    def execute_input(self, exec_ctx : Context):
        list_reper = list(str(exec_ctx.symbol_table.get('value')))
        text = input("".join(list_reper[1:-1]))

        return RuntimeResult().success(String(text))
    execute_input.arg_names = ['value']

    def execute_input_int(self, exec_ctx : Context):
        while True:
            list_reper = list(str(exec_ctx.symbol_table.get('value')))
            text = input("".join(list_reper[1:-1]))
            try:
                number = int(text)
                break
            except ValueError:
                print(str(f"'{text}' must be an integer. Try again!"))
        return RuntimeResult().success(Number(number))
    execute_input_int.arg_names = ['value']

    def execute_clear(self, exec_ctx : Context):
        system('cls' if name == 'nt' else 'cls') 
        return RuntimeResult().success(Number.null)
    execute_clear.arg_names = []

    def execute_is_num(self, exec_ctx : Context):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), Number)
        return RuntimeResult().success(Number.true if is_number else Number.false)
    execute_is_num.arg_names = ["value"]

    def execute_is_string(self, exec_ctx : Context):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), String)
        return RuntimeResult().success(Number.true if is_number else Number.false)
    execute_is_string.arg_names = ["value"]

    def execute_is_list(self, exec_ctx : Context):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), List)
        return RuntimeResult().success(Number.true if is_number else Number.false)
    execute_is_list.arg_names = ["value"]

    def execute_is_function(self, exec_ctx : Context):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), BaseFunction)
        return RuntimeResult().success(Number.true if is_number else Number.false)
    execute_is_function.arg_names = ["value"]

    def execute_append(self, exec_ctx : Context):
        list_ = exec_ctx.symbol_table.get("list")
        value = exec_ctx.symbol_table.get("value")

        if not isinstance(list_, List):
            return RuntimeResult().failure(RunTimeError(
            self.start_position, self.end_position,
            "First argument must be list",
            exec_ctx
            ))

        list_.elements.append(value)
        return RuntimeResult().success(Number.null)
    execute_append.arg_names = ["list", "value"]

    def execute_pop(self, exec_ctx : Context):
        list_ = exec_ctx.symbol_table.get("list")
        index = exec_ctx.symbol_table.get("index")

        if not isinstance(list_, List):
            return RuntimeResult().failure(RunTimeError(
            self.start_position, self.end_position,
            "First argument must be list",
            exec_ctx
            ))

        if not isinstance(index, Number):
            return RuntimeResult().failure(RunTimeError(
            self.start_position, self.end_position,
            "Second argument must be number",
            exec_ctx
            ))

        try:
            element = list_.elements.pop(index.value)
        except:
            return RuntimeResult().failure(RunTimeError(
            self.start_position, self.end_position,
            'Element at this index could not be removed from list because index is out of bounds',
            exec_ctx
            ))
        return RuntimeResult().success(element)
    execute_pop.arg_names = ["list", "index"]

    def execute_extend(self, exec_ctx : Context):
        listA = exec_ctx.symbol_table.get("listA")
        listB = exec_ctx.symbol_table.get("listB")

        if not isinstance(listA, List):
            return RuntimeResult().failure(RunTimeError(
                self.start_position, self.end_position,
                "First argument must be list",
                exec_ctx
            ))

        if not isinstance(listB, List):
            return RuntimeResult().failure(RunTimeError(
                self.start_position, self.end_position,
                "Second argument must be list",
                exec_ctx
            ))

        listA.elements.extend(listB.elements)
        return RuntimeResult().success(Number.null)
    execute_extend.arg_names = ["listA", "listB"]

    def execute_length(self,exec_ctx : Context):
        list_ = exec_ctx.symbol_table.get("list")

        if not isinstance(list_, List):
            return RuntimeResult().failure(RunTimeError(
                self.pos_start, self.pos_end,
                "Argument must be list",
                exec_ctx
            ))

        return RuntimeResult().success(Number(len(list_.elements)))
    execute_length.arg_names = ["list"]     

    def execute_Run(self,exec_ctx : Context):
        fn = exec_ctx.symbol_table.get('fn')

        if not isinstance(fn, String):
            return RuntimeResult().failure(RunTimeError(
            self.start_position, self.end_position,
            "Second argument must be string",
            exec_ctx
        ))

        fn = fn.value

        try:
            with open(fn, "r") as f:
                script = str(f.read())
        except Exception as e:
            return RuntimeResult().failure(RunTimeError(
                self.start_position, self.end_position,
                str(f"Failed to load script \"{fn}\"\n") + str(e),
                exec_ctx
            ))

        temp_ = list(script)
        while temp_[0] == "\n":
            temp_.pop(0)

        _ , error = run(temp_, fn)
        if error:
            return RuntimeResult().failure(RunTimeError(
                self.start_position, self.end_position,
                str(f"Failed to finish executing script \"{fn}\"\n") +
                error.as_string(),
                exec_ctx
            ))

        return RuntimeResult().success(Number.null)
    execute_Run.arg_names = ['fn']

    def execute_format(self,exec_ctx : Context):
        string = exec_ctx.symbol_table.get('string')
        values = exec_ctx.symbol_table.get('values')

        return RuntimeResult().success(String(string.value.format(*values.elements)))
    execute_format.arg_names = ['string','values']

            # =======================
            # GAMES BUILT IN Function
            # =======================
    
    def execute_generate_windows(self,exec_ctx : Context):
        name = exec_ctx.symbol_table.get('name')
        title = exec_ctx.symbol_table.get('title')
        bgcolor = exec_ctx.symbol_table.get('bgcolor')
        width = exec_ctx.symbol_table.get('width')
        height = exec_ctx.symbol_table.get('height')
        tracer = exec_ctx.symbol_table.get('tracer')
        # set name as key for windows object in symbol table 
        
        windows = turtle.Screen()
        windows.title(title.value)
        windows.bgcolor(bgcolor.value)
        windows.setup(width=width.value, height=height.value)
        windows.tracer(tracer.value)

        if name.value  in global_symbol_table.symbols:
            return RuntimeResult().failure(RunTimeError(
                self.start_position, self.end_position,
                str(f"Identifier {name} used before \n") ,
                exec_ctx
            ))

        global_symbol_table.set(name.value,windows)

        return RuntimeResult().success(Number.null)
    execute_generate_windows.arg_names = ['name','title','bgcolor','width','height','tracer']


    def execute_start_windows_listen(self,exec_ctx : Context):
        name = exec_ctx.symbol_table.get('name')

        if name.value  not in global_symbol_table.symbols:
            return RuntimeResult().failure(RunTimeError(
                self.start_position, self.end_position,
                str(f"windows not initialized \n") ,
                exec_ctx
            ))

        window = global_symbol_table.get(name.value)
        window.listen()

        return RuntimeResult().success(Number.null)
    execute_start_windows_listen.arg_names = ['name']


    def execute_generate_shape(self,exec_ctx: Context):
        shape_ = exec_ctx.symbol_table.get('shape_')
        color = exec_ctx.symbol_table.get('color')
        wid = exec_ctx.symbol_table.get('wid')
        le = exec_ctx.symbol_table.get('len')
        goto1 = exec_ctx.symbol_table.get('goto1')
        goto2 = exec_ctx.symbol_table.get('goto2')
        hide = exec_ctx.symbol_table.get('hide')
        write = exec_ctx.symbol_table.get('write')
        name = exec_ctx.symbol_table.get('name')


        # set name as key for shape object in symbol table 
        Shape = turtle.Turtle()
        Shape.shape(shape_.value)
        Shape.color(color.value)
        Shape.penup()
        if wid.value != 0 and le.value != 0: 
            Shape.shapesize(stretch_wid=wid.value, stretch_len=le.value)

        if hide.value == 1:
            Shape.hideturtle()
        Shape.goto(goto1.value,goto2.value)

        if write.value != '':
            Shape.write(write.value, align="center", font=("Courier", 24,'normal'))
        global_symbol_table.set(name.value,Shape)

        return RuntimeResult().success(Number.null)

    execute_generate_shape.arg_names = [ 'name','shape_','color','wid','len','goto1','goto2','hide','write']


    def execute_move_on_y(self,exec_ctx : Context):
        movement = exec_ctx.symbol_table.get('movement')
        name = exec_ctx.symbol_table.get('name')
        # get shape object from symbol table and and move on y axis

        if name.value not in global_symbol_table.symbols:
            return RuntimeResult().failure(RunTimeError(
                self.start_position, self.end_position,
                str(f"shape object  not initialized \n") ,
                exec_ctx
            ))

        object = global_symbol_table.get(name.value)
        y = object.ycor()
        y += movement.value
        object.sety(y)

        return RuntimeResult().success(Number.null)

    execute_move_on_y.args_names = ['name','movement']

    def execute_move_on_x(self,exec_ctx : Context):
        movement = exec_ctx.symbol_table.get('movement')
        name = exec_ctx.symbol_table.get('name')
        # get shape object from symbol table and and move on y axis

        if name.value not in global_symbol_table.symbols:
            return RuntimeResult().failure(RunTimeError(
                self.start_position, self.end_position,
                str(f"shape object  not initialized \n") ,
                exec_ctx
            ))

        object = global_symbol_table.get(name.value)
        x = object.xcor()
        x += movement
        object.setx(x)

        return RuntimeResult().success(Number.null)

    execute_move_on_x.args_names = ['name','movement']


    def execute_add_key_press_event(self, exec_ctx:Context):
        #get windowsand shape  objects form symbol_Table
        windows_name = exec_ctx.symbol_table.get('windows_name')
        action = exec_ctx.symbol_table.get('action')
        key = exec_ctx.symbol_table.get('key')
        name = exec_ctx.symbol_table.get('name')


        if name.value not in  global_symbol_table.symbols:
            return RuntimeResult().failure(RunTimeError(
                self.start_position, self.end_position,
                str(f"windows not initialized \n") ,
                exec_ctx
            ))

        def movement_handler(shape_object: turtle.Turtle,direction):
            if direction == 'up':
                shape_object.sety(shape_object.ycor() + 30)
            elif direction == 'down':
                shape_object.sety(shape_object.ycor() - 30)


        window = global_symbol_table.get(windows_name.value)
        shape_obj = global_symbol_table.get(name.value)
        handler = lambda :movement_handler(shape_obj,action.value)
        window.onkeypress(handler,key.value)

        return RuntimeResult().success(Number.null)

    execute_add_key_press_event.arg_names = ['windows_name','name','action','key']


    def execute_set_y(self,exec_ctx : Context):
        name = exec_ctx.symbol_table.get('name')
        y_cor = exec_ctx.symbol_table.get('ycor')

        if name.value not in  global_symbol_table.symbols:
            return RuntimeResult().failure(RunTimeError(
                self.start_position, self.end_position,
                str(f"shape not initialized \n") ,
                exec_ctx
            ))

        shape_object = global_symbol_table.get(name.value)
        shape_object.sety(y_cor.value)

        return RuntimeResult().success(Number.null)
    execute_set_y.arg_names = ['name','ycor']


    def execute_set_x(self,exec_ctx : Context):
        name = exec_ctx.symbol_table.get('name')
        x_cor = exec_ctx.symbol_table.get('xcor')
        
        if name.value not in  global_symbol_table.symbols:
            return RuntimeResult().failure(RunTimeError(
                self.start_position, self.end_position,
                str(f"shape not initialized \n") ,
                exec_ctx
            ))

        shape_object = global_symbol_table.get(name.value)
        shape_object.setx(x_cor.value) 

        return RuntimeResult().success(Number.null)
    execute_set_x.arg_names = ['name','xcor']


    def execute_get_y(self,exec_ctx : Context):
        name = exec_ctx.symbol_table.get('name')

        if name.value not in  global_symbol_table.symbols:
            return RuntimeResult().failure(RunTimeError(
                self.start_position, self.end_position,
                str(f"shape not initialized \n") ,
                exec_ctx
            ))

        shape_object = global_symbol_table.get(name.value)
        ycor = shape_object.ycor()
        return RuntimeResult().success(Number(ycor))

    execute_get_y.arg_names = ['name']


    def execute_get_x(self,exec_ctx : Context):
        name = exec_ctx.symbol_table.get('name')

        if name.value not in  global_symbol_table.symbols:
            return RuntimeResult().failure(RunTimeError(
                self.start_position, self.end_position,
                str(f"shape not initialized \n") ,
                exec_ctx
            ))

        shape_object = global_symbol_table.get(name.value)
        xcor = shape_object.xcor()
        return RuntimeResult().success(Number(xcor))
    execute_get_x.arg_names = ['name']


    def execute_clear_shape(self,exec_ctx : Context):
        name = exec_ctx.symbol_table.get('name')

        if name.value not in  global_symbol_table.symbols:
            return RuntimeResult().failure(RunTimeError(
                self.start_position, self.end_position,
                str(f"shape not initialized \n") ,
                exec_ctx
            ))

        shape_object = global_symbol_table.get(name.value)
        shape_object.clear()

        return RuntimeResult().success(Number.null)
    execute_clear_shape.arg_names = ['name']


    def execute_write_shape(self,exec_ctx : Context):
        name = exec_ctx.symbol_table.get('name')
        txt = exec_ctx.symbol_table.get('txt')

        if name.value not in  global_symbol_table.symbols:
            return RuntimeResult().failure(RunTimeError(
                self.start_position, self.end_position,
                str(f"shape not initialized \n") ,
                exec_ctx
            ))

        shape_object = global_symbol_table.get(name.value)
        shape_object.write(txt.value,align="center", font=("Courier", 24,'normal'))

        return RuntimeResult().success(Number.null)

    execute_write_shape.arg_names = ['name','txt']


    def execute_shape_goto(self,exec_ctx):
        name = exec_ctx.symbol_table.get('name')
        x = exec_ctx.symbol_table.get('x')
        y = exec_ctx.symbol_table.get('y')

        if name.value not in  global_symbol_table.symbols:
            return RuntimeResult().failure(RunTimeError(
                self.start_position, self.end_position,
                str(f"shape not initialized \n") ,
                exec_ctx
            ))

        shape_object = global_symbol_table.get(name.value)
        shape_object.goto(x.value,y.value)

        return RuntimeResult().success(Number.null)
    execute_shape_goto.arg_names = ['name','x','y']


    def execute_windows_update(self,exec_ctx):
        name = exec_ctx.symbol_table.get('name')

        if name.value not in  global_symbol_table.symbols:
            return RuntimeResult().failure(RunTimeError(
                self.start_position, self.end_position,
                str(f"shape not initialized \n") ,
                exec_ctx
            ))

        shape_object = global_symbol_table.get(name.value)
        shape_object.update()
        
        return RuntimeResult().success(Number.null)
    execute_windows_update.arg_names = ['name',]



BuiltInFunction.print       = BuiltInFunction("print")
BuiltInFunction.input       = BuiltInFunction("input")
BuiltInFunction.input_int   = BuiltInFunction("input_int")
BuiltInFunction.clear       = BuiltInFunction("clear")
BuiltInFunction.is_num      = BuiltInFunction("is_num")
BuiltInFunction.is_string   = BuiltInFunction("is_string")
BuiltInFunction.is_list     = BuiltInFunction("is_list")
BuiltInFunction.is_function = BuiltInFunction("is_function")
BuiltInFunction.append      = BuiltInFunction("append")
BuiltInFunction.pop         = BuiltInFunction("pop")
BuiltInFunction.extend      = BuiltInFunction("extend")
BuiltInFunction.Run         = BuiltInFunction("Run")
BuiltInFunction.length      = BuiltInFunction("length")

#games 
BuiltInFunction.generate_windows = BuiltInFunction('generate_windows')
BuiltInFunction.start_windows_listen = BuiltInFunction('start_windows_listen')
BuiltInFunction.generate_shape = BuiltInFunction('generate_shape')
BuiltInFunction.move_on_y = BuiltInFunction('move_on_y')
BuiltInFunction.move_on_x = BuiltInFunction('move_on_x')
BuiltInFunction.add_key_press_event = BuiltInFunction('add_key_press_event')

BuiltInFunction.set_y = BuiltInFunction('set_y')
BuiltInFunction.set_x = BuiltInFunction('set_x')
BuiltInFunction.get_x = BuiltInFunction('get_x')
BuiltInFunction.get_y = BuiltInFunction('get_y')
BuiltInFunction.clear_shape = BuiltInFunction('clear_shape')
BuiltInFunction.write_shape = BuiltInFunction('write_shape')
BuiltInFunction.shape_goto = BuiltInFunction('shape_goto')
BuiltInFunction.windows_update = BuiltInFunction('windows_update')
BuiltInFunction.format = BuiltInFunction('format')




global_symbol_table = SymbolTable()

global_symbol_table.set("null", Number.null)
global_symbol_table.set("false", Number.false)
global_symbol_table.set("true", Number.true)

global_symbol_table.set("print", BuiltInFunction.print)
global_symbol_table.set("input", BuiltInFunction.input)
global_symbol_table.set("input_int", BuiltInFunction.input_int)
global_symbol_table.set("clear", BuiltInFunction.clear)
global_symbol_table.set("cls", BuiltInFunction.clear)
global_symbol_table.set("is_num", BuiltInFunction.is_num)
global_symbol_table.set("is_string", BuiltInFunction.is_string)
global_symbol_table.set("is_list", BuiltInFunction.is_list)
global_symbol_table.set("is_func", BuiltInFunction.is_function)
global_symbol_table.set("append", BuiltInFunction.append)
global_symbol_table.set("pop", BuiltInFunction.pop)
global_symbol_table.set("extend", BuiltInFunction.extend)
global_symbol_table.set("Run", BuiltInFunction.Run)
global_symbol_table.set("length", BuiltInFunction.length)

global_symbol_table.set("generate_windows", BuiltInFunction.generate_windows)
global_symbol_table.set("add_key_press_event", BuiltInFunction.add_key_press_event)
global_symbol_table.set("start_windows_listen", BuiltInFunction.start_windows_listen)
global_symbol_table.set("generate_shape", BuiltInFunction.generate_shape)

global_symbol_table.set("move_on_y", BuiltInFunction.move_on_y)
global_symbol_table.set("move_on_x", BuiltInFunction.move_on_x)

global_symbol_table.set("set_y", BuiltInFunction.set_y)
global_symbol_table.set("set_x", BuiltInFunction.set_x)
global_symbol_table.set("get_y", BuiltInFunction.get_y)
global_symbol_table.set("get_x", BuiltInFunction.get_x)

global_symbol_table.set("clear_shape", BuiltInFunction.clear_shape)
global_symbol_table.set("write_shape", BuiltInFunction.write_shape)
global_symbol_table.set("shape_goto", BuiltInFunction.shape_goto)
global_symbol_table.set("windows_update", BuiltInFunction.windows_update)
global_symbol_table.set('format',BuiltInFunction.format)


