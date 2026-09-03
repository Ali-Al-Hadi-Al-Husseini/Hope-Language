package lexer

const (
	TOKEN_STRING     = "STRING"
	TOKEN_INT        = "INTEGER"
	TOKEN_FLOAT      = "FLOAT"
	TOKEN_PLUS       = "PLUS"
	TOKEN_MINUS      = "MINUS"
	TOKEN_MUL        = "MUL"
	TOKEN_DIV        = "DIV"
	TOKEN_POW        = "POW " // power token
	TOKEN_MODULE     = "MOD"
	TOKEN_LPAREN     = "LPAREN"
	TOKEN_RPARENT    = "RPAREN"
	TOKEN_EQ         = "EQ"         // equals token
	TOKEN_EE         = "EE"         // equals equals "==" token used in comparison operatores
	TOKEN_GT         = "GT"         // greater then ">" operator token
	TOKEN_NE         = "NE"         // not equals then "!=" operator token
	TOKEN_LT         = "LT"         // less then "<" operator token
	TOKEN_GTE        = "GTE"        // greater then  or equal ">=" operator token
	TOKEN_LTE        = "LTE"        // less then or equals "<=" operator token
	TOKEN_KEYWORD    = "KEYWORD"    // keyword that are used by the language
	TOKEN_IDENTIFIER = "IDENTIFIER" // names that are given by the user to name variables, fucntions ...
	TOKEN_EOF        = "EOF"
	TOKEN_COMMA      = " COMMA"
	TOKEN_LCURLY     = "LCURLY"
	TOKEN_RCURLY     = "RCURLY"
	TOKEN_LSQUARE    = "LSQUARE"
	TOKEN_RSQUARE    = "RSQUARE"
	TOKEN_START      = "UNTIL"
	TOKEN_END        = "SKIP"
	TOKEN_ARROW      = "ARROW"
	TOKEN_QUOTES     = "\""
	TOKEN_ANDSYMBOL  = "ANDSYMBOL"
	TOKEN_ORSYMBOL   = "ORSYMBOL"
	TOKEN_PYTHON     = "PYTHON"
	TOKEN_NEWLINE    = "NEWLINE"
)

var KEYWORDS = map[string]bool{

	"let":      true,
	"and":      true,
	"or":       true,
	"not":      true,
	"if":       true,
	"elif":     true,
	"else":     true,
	"while":    true,
	"for":      true,
	"func":     true,
	"PYTHON":   true,
	"return":   true,
	"break":    true,
	"continue": true,
	"skip":     true,
	"run":      true,
}

type Token struct {
	Type  string
	Value string
	Position
}

func (tok Token) Matches(_type string, value string) bool {
	return tok.Type == _type && tok.Value == value
}

type Position struct {
	Idx  int
	Line int
	Col  int
	CodeFile
}

type CodeFile struct {
	Name string
	Text string
}

func (pos *Position) Advance(currChar string) Position {
	pos.Idx += 1
	pos.Col += 1

	if currChar == "\n" {
		pos.Line += 1
		pos.Col += 1
	}
	return *pos
}
func (pos Position) Copy() Position {
	return pos
}
