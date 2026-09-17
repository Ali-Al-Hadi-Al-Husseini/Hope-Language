package parser

import (
	"fmt"

	lexer "github.com/Ali-Al-Hadi-Al-Husseini/Hope-Language/hope-go/src/lexer"
)

type BaseNode struct {
	Name     string
	Token    *lexer.Token
	Tokens   []*lexer.Token
	StartPos *lexer.Position
	EndPos   *lexer.Position
}

func (node *BaseNode) String() string {
	return fmt.Sprintf("%v__%v", node.Token, node.Name)
}

type StringNode struct {
	BaseNode
}
