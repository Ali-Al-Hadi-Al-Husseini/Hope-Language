package parser

import (
	lexer "github.com/Ali-Al-Hadi-Al-Husseini/Hope-Language/hope-go/src/lexer"
)

type node struct {
	StartPos *lexer.Position
	EndPos   *lexer.Position
}
