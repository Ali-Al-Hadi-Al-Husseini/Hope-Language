from string import ascii_letters


DIGITS             = set('0123456789')
LETTERS            = set(ascii_letters) # t
LETTER_DIGITS      = set(ascii_letters + '0123456789')
TOKEN_STRING       = 'STRING'
TOKEN_INT          = 'INTEGER'
TOKEN_FLOAT        = 'FLOAT'
TOKEN_PLUS         = 'PLUS' 
TOKEN_MINUS        = 'MINUS'
TOKEN_MUL          = 'MUL'
TOKEN_DIV          = 'DIV'
TOKEN_POW          = 'POW '# power token 
TOKEN_MODULE       = 'MOD'
TOKEN_LPAREN       = 'LPAREN'
TOKEN_RPARENT      = 'RPAREN'
TOKEN_EQ           = 'EQ' # equals token 
TOKEN_EE           = 'EE' # equals equals '==' token used in comparison operatores
TOKEN_GT           = 'GT' # greater then '>' operator token
TOKEN_NE           = 'NE' # not equals then '!=' operator token
TOKEN_LT           = 'LT' # less then '<' operator token
TOKEN_GTE          = 'GTE' # greater then  or equal '>=' operator token
TOKEN_LTE          = 'LTE' # less then or equals '<=' operator token
TOKEN_KEYWORD      = 'KEYWORD' # keyword that are used by the language 
TOKEN_IDENTIFIER   = 'IDENTIFIER' # names that are given by the user to name variables, fucntions ...
TOKEN_EOF          = 'EOF'
TOKEN_COMMA        = ' COMMA'
TOKEN_LCURLY       = 'LCURLY'
TOKEN_RCURLY       = 'RCURLY'
TOKEN_LSQUARE      = 'LSQUARE'
TOKEN_RSQUARE      = 'RSQUARE'
TOKEN_START        = 'UNTIL'
TOKEN_END          = 'SKIP'
TOKEN_ARROW        = 'ARROW'
TOKEN_QUOTES       = '"'
TOKEN_ANDSYMBOL    = "ANDSYMBOL"
TOKEN_ORSYMBOL     = "ORSYMBOL"
TOKEN_PYTHON       = 'PYTHON'
TOKEN_NEWLINE      = 'NEWLINE'

KEYWORDS = set([ 
    'let',
    'and',
    'or',
    'not',
    'if',
    'elif',
    'else',
    'while',
    'for', 
    'func',
    'PYTHON',
    'return',
    'break',
    'continue',
    'skip',
    'run'
])

