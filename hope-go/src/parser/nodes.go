package parser

import (
	"fmt"

	lexer "github.com/Ali-Al-Hadi-Al-Husseini/Hope-Language/hope-go/src/lexer"
)

type Node interface {
	String() string
}

type Expr interface {
	Expr()
}
type Stmt interface {
	Stmt()
}
type BaseNode struct {
	Name     string
	Token    *lexer.Token
	StartPos *lexer.Position
	EndPos   *lexer.Position
}

func (node *BaseNode) String() string {
	return fmt.Sprintf("%v__%v", node.Token.String(), node.Name)
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
	bodyNodes := make([]string, len(node.Elements))
	for idx, elemn := range node.Elements {
		bodyNodes[idx] = elemn.String()
	}
	return fmt.Sprintf("ListNode__%v", bodyNodes)
}

type ListAcssesNode struct {
	Ident string
	Index string
	BaseNode
}

func (node *ListAcssesNode) String() string {
	return fmt.Sprintf("__%v__%v__ListacssesNode", node.Ident, node.Index)
}

type UnaryOperationNode struct {
	OpToken lexer.Token
	Node    Node
	BaseNode
}

func (node *UnaryOperationNode) String() string {
	return fmt.Sprintf("(%s, %v)", node.OpToken.String(), node.Node)
}

type BinOpertaionNode struct {
	LeftNode  Node
	Operation lexer.Token
	RightNode Node
	BaseNode
}

func (node *BinOpertaionNode) String() string {
	// left and right are flipped because an erro in python code where leftnode and right node are flipped in __init__
	return fmt.Sprintf("( %v %v %v )", node.RightNode, node.Operation.String(), node.LeftNode)
}

type VarAssignNode struct {
	NameToken lexer.Token
	ValueNode Node
	BaseNode
}

func (node *VarAssignNode) String() string {
	return fmt.Sprintf("%v__var_assign_node", node.NameToken.String())
}

type VarAccessNode struct {
	BaseNode
}

func (node *VarAccessNode) String() string {
	return fmt.Sprintf("%v__var_access_node", node.Token)
}

type IfNode struct {
	Cases     []Node
	ElseCases Node
	BaseNode
}

func (node *IfNode) String() string {
	casesNode := make([]string, len(node.Cases))
	for idx, elemn := range node.Cases {
		casesNode[idx] = elemn.String()
	}
	return fmt.Sprintf("%v__%v__IfNode", casesNode, node.ElseCases)
}

type ForNode struct {
	StartValueNode   Node
	EndValueNode     Node
	VarNameNode      Node
	SkipValueNode    Node
	BodyNode         Node
	ShouldReturnNull bool
	BaseNode
}

func (node *ForNode) String() string {
	return ""
}

type ControlFlow struct {
	Cases    []Node
	ElseCase Node
	BaseNode
}
type Case struct {
	conditon         Node
	stmts            Node
	ShouldReturnNull bool
	BaseNode
}

func (node *Case) String() string {
	return fmt.Sprintf("(%v, %v, %v)", node.conditon, node.stmts, node.ShouldReturnNull)
}

type WhileNode struct {
	ConditionNode    Node
	BodyNode         Node
	ShouldReturnNull bool
	BaseNode
}

type FuncDefNode struct {
	ArgNameTokens    []lexer.Token
	BodyNode         Node
	VarNameToken     lexer.Token
	ShouldReturnNull bool

	BaseNode
}

type CallNode struct {
	NodeToCall Node
	ArgNodes   []Node
	BaseNode
}

func (node *CallNode) String() string {
	return fmt.Sprintf("%v__Call_Node", node.NodeToCall)
}

type ReturnNode struct {
	node Node
	BaseNode
}

type BreakNode struct {
	BaseNode
}
type ContinueNode struct {
	BaseNode
}
