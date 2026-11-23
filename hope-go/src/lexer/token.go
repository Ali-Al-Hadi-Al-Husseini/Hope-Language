package lexer

import (
	position "github.com/Ali-Al-Hadi-Al-Husseini/Hope-Language/hope-go/src/Position"
)

type Token struct {
	Type   string
	Value  string
	Pos    position.Position
	EndPos position.Position
}

func (tok *Token) String() string {
	if tok.Value != "" {
		return tok.Type + ":" + tok.Value
	}
	return tok.Type

}

func (tok Token) Matches(_type string, value string) bool {
	return tok.Type == _type && tok.Value == value
}
