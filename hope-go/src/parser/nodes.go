package parser

import (
	"fmt"

	lexer "github.com/Ali-Al-Hadi-Al-Husseini/Hope-Language/hope-go/src/lexer"
)

type Node interface {
	String() string
}
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

type NumberNode struct {
	BaseNode
}

type ListNode struct {
	Elements []Node
	BaseNode
}

func (node *ListNode) String() string {
	bodyNodes := make([]string, 0, len(node.Elements))
	for idx, elemn := range node.Elements {
		bodyNodes[idx] = elemn.String()
	}
	return fmt.Sprintf("ListNode__%v", bodyNodes)
}
