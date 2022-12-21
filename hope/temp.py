from Interpreter_tools.Interpreter import run
from Parser_tools.Parser import Parser

a = run("""let a = 2 ; a ^= 8 ;print(a)""","A.hope")
print(a)

def make_tokens(string: str):
    strings = string.split(":")
    print(strings)



make_tokens("asdadasd:5")
make_tokens("asdadasd")
