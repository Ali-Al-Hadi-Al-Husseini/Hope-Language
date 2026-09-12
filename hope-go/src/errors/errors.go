package errors

import (
	lexer "github.com/Ali-Al-Hadi-Al-Husseini/Hope-Language/hope-go/src/lexer"
)

type Error struct {
	Name     string
	Details  string
	StartPos *lexer.Position
	EndPos   *lexer.Position
}
