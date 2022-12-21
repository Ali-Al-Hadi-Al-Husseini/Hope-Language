from .context_and_symbol_table import *

from Errors_tools.Errors import RunTimeError
from .Types import Value

class RuntimeResult:
    def __init__(self):
        self.values = []
        self.reset()

    def reset(self):
        self.value = None
        self.error = None
        self.func_return_value = None
        self.loop_should_continue = False
        self.loop_should_break = False

    def Register(self, res):
        if  res.should_return(): self.error = res.error
        self.func_return_value = res.func_return_value
        self.loop_should_continue = res.loop_should_continue
        self.loop_should_break = res.loop_should_break


        return res.value

    def success(self, value):
        self.reset()
        self.value = value

        self.values.append(value)

        return self

    def success_return(self, value):
        self.reset()
        self.func_return_value = value
        return self
    
    def success_continue(self):
        self.reset()
        self.loop_should_continue = True
        return self

    def success_break(self):
        self.reset()
        self.loop_should_break = True
        return self

    def failure(self,error):
        self.reset()
        self.error = error
        return self

    def should_return(self):
            # Note: this will allow you to continue and break outside the current function
        return (
        self.error or
        self.func_return_value or
        self.loop_should_continue or
        self.loop_should_break
    )


class BaseFunction(Value):
    def __init__(self, name):
        super().__init__()
        self.name = name or "<anonymous>"

    def generate_new_context(self) -> Context:
        new_context = Context(self.name, self.context, self.start_position)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context

    def check_args(self, arg_names, args):
        Result = RuntimeResult()

        if len(args) > len(arg_names):
            return Result.failure(RunTimeError(
            self.start_position, self.end_position,
            str(f"{len(args) - len(arg_names)} too many args passed into {self}"),
            self.context
            ))

        if len(args) < len(arg_names):
            return Result.failure(RunTimeError(
            self.start_position, self.end_position,
            str(f"{len(arg_names) - len(args)} missing arg/s passed into {self}"),
            self.context
            ))

        return Result.success(None)

    def populate_args(self, arg_names, args, exec_ctx : Context):
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(exec_ctx)
            exec_ctx.symbol_table.set(arg_name, arg_value)

    def check_and_populate_args(self, arg_names, args, exec_ctx : Context):
        Result = RuntimeResult()
        Result.Register(self.check_args(arg_names, args))
        if  Result.should_return(): return Result
        self.populate_args(arg_names, args, exec_ctx)
        return Result.success(None)

class Function(BaseFunction):
  def __init__(self, name, body_node, arg_names, should_return_null):
    super().__init__(name)
    self.body_node = body_node
    self.arg_names = arg_names
    self.should_return_null = should_return_null


  def copy(self):
    copy = Function(self.name, self.body_node, self.arg_names,self.should_return_null)
    copy.set_context(self.context)
    copy.set_position(self.start_position, self.end_position)
    return copy

  def __repr__(self):
    return str("<function {self.name}>")

