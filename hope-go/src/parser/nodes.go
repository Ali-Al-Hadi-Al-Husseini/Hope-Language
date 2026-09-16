package parser

import (
	lexer "github.com/Ali-Al-Hadi-Al-Husseini/Hope-Language/hope-go/src/lexer"
)

type BaseNode struct {
	Token    *lexer.Token
	Tokens   []*lexer.Token
	StartPos *lexer.Position
	EndPos   *lexer.Position
}
