package parser

import (
	"fmt"
	"reflect"
	"testing"

	"github.com/Ali-Al-Hadi-Al-Husseini/Hope-Language/hope-go/src/lexer"
)

type testCase struct {
	expresion string
	want      string
}

func TestParser(t *testing.T) {
	testCases := []testCase{
		{"(2+1)", "ListNode__[( INTEGER:1__NumberNode PLUS INTEGER:2__NumberNode )]"},
		{"(-2+1)", "ListNode__[( INTEGER:1__NumberNode PLUS (MINUS, INTEGER:2__NumberNode) )]"},
		{"(7 * 2)", "ListNode__[( INTEGER:2__NumberNode MUL INTEGER:7__NumberNode )]"},
		{"(7 * 3)", "ListNode__[( INTEGER:3__NumberNode MUL INTEGER:7__NumberNode )]"},
		{"(3 / 3)", "ListNode__[( INTEGER:3__NumberNode DIV INTEGER:3__NumberNode )]"},
		{"(9 / 3 )", "ListNode__[( INTEGER:3__NumberNode DIV INTEGER:9__NumberNode )]"},
		{"(9 / 3  + 1)", "ListNode__[( INTEGER:1__NumberNode PLUS ( INTEGER:3__NumberNode DIV INTEGER:9__NumberNode ) )]"},
		{"(6 / 3  + 2 )", "ListNode__[( INTEGER:2__NumberNode PLUS ( INTEGER:3__NumberNode DIV INTEGER:6__NumberNode ) )]"},
		{"(9 / 3  * 2 )", "ListNode__[( INTEGER:2__NumberNode MUL ( INTEGER:3__NumberNode DIV INTEGER:9__NumberNode ) )]"},
		{"(9 / 3  - 1)", "ListNode__[( INTEGER:1__NumberNode MINUS ( INTEGER:3__NumberNode DIV INTEGER:9__NumberNode ) )]"},
		{"(6 / 3  - 2 )", "ListNode__[( INTEGER:2__NumberNode MINUS ( INTEGER:3__NumberNode DIV INTEGER:6__NumberNode ) )]"},
		{"(9 / 3  * -2 )", "ListNode__[( (MINUS, INTEGER:2__NumberNode) MUL ( INTEGER:3__NumberNode DIV INTEGER:9__NumberNode ) )]"},
		{"((9 / 3)  * 0 )", "ListNode__[( INTEGER:0__NumberNode MUL ( INTEGER:3__NumberNode DIV INTEGER:9__NumberNode ) )]"},
		{"((9 / 3) / 0 )", "ListNode__[( INTEGER:0__NumberNode DIV ( INTEGER:3__NumberNode DIV INTEGER:9__NumberNode ) )]"},
		{" 'abc' * 'xyz '", "ListNode__[( STRING:xyz __StringNode MUL STRING:abc__StringNode )]"},
		{"if true >> print('i')", "ListNode__[[(IDENTIFIER:true__var_access_node, IDENTIFIER:print__var_access_node__Call_Node, false)]__<nil>__IfNode]"},
		{"if false >> print(1)", "ListNode__[[(IDENTIFIER:false__var_access_node, IDENTIFIER:print__var_access_node__Call_Node, false)]__<nil>__IfNode]"},
		{"if true >> print(1)", "ListNode__[[(IDENTIFIER:true__var_access_node, IDENTIFIER:print__var_access_node__Call_Node, false)]__<nil>__IfNode]"},
		{" let a = 2 \n        if a < 2 >> \n            print('hello')\n        elif a == 2 >> \n            print('world')\n        else >>\n            print('!')\n        <<\n        ", "'ListNode__[IDENTIFIER:a__var_assign_node', \"[(( INTEGER:2__NumberNode LT IDENTIFIER:a__var_access_node ), ListNode__[IDENTIFIER:print__var_access_node__Call_Node], true), (( INTEGER:2__NumberNode EE IDENTIFIER:a__var_access_node ), ListNode__[IDENTIFIER:print__var_access_node__Call_Node], true)]__(ListNode__[IDENTIFIER:print__var_access_node__Call_Node], true)__IfNode\"]'"},
		{" func add(a,b) >>  a + b\n        let z = add(1,2)   \n        ", "ListNode__[functionDefNode__IDENTIFIER:add__( IDENTIFIER:b__var_access_node PLUS IDENTIFIER:a__var_access_node )\", 'IDENTIFIER:z__var_assign_node]"},
		{"let add =  func (a,b) >>  a + b\n        let z = add(1,2)   \n", "ListNode__[IDENTIFIER:add__var_assign_node', 'IDENTIFIER:z__var_assign_node]"},
		{"let add =  func (a,b) >> \n        return a + b\n        <<\n        let z = add(1,2)   \n        ", "ListNode__[IDENTIFIER:add__var_assign_node', 'IDENTIFIER:z__var_assign_node]"},
		{"func add (a,b) >> \n\n            if a > b >>\n                return a+b + 1 \n         else >> \n                return a + b -1\n            <<\n        <<\n        let z = add(1,2)   \n        ", "'ListNode__[functionDefNode__IDENTIFIER:add__ListNode__[\"[(( IDENTIFIER:b__var_access_node GT IDENTIFIER:a__var_access_node ), ListNode__[__ReturnNode__], true)]__(ListNode__[__ReturnNode__], true)__IfNode\"]', 'IDENTIFIER:z__var_assign_node]'"},
		{"for i= 1 -> 5 >> print(i)", "ListNode__[For_Node__IDENTIFIER:print__var_access_node__Call_Node]"},
		{"for i= 1 -> 5 >> let a = i ", "ListNode__[For_Node__IDENTIFIER:a__var_assign_node]"},
		{"for i= 1 -- 5 >> print(i) ", "'<nil>'"},
		{"let i = 0\n        while i < 5 >> i +=  1\n        print(i)\n        ", "ListNode__[IDENTIFIER:i__var_assign_node\", 'While_Node__IDENTIFIER:i__var_assign_node', 'IDENTIFIER:print__var_access_node__Call_Node]"},
		{"let i = 0\n        while i < 10 >> \n            i +=  1\n            if i == 5  >> break\n        <<\n        print(i)\n        ", "'ListNode__[IDENTIFIER:i__var_assign_node', \"While_Node__ListNode__['IDENTIFIER:i__var_assign_node', '[(( INTEGER:5__NumberNode EE IDENTIFIER:i__var_access_node ), __BreakNode__, false)]__<nil>__IfNode]\", 'IDENTIFIER:print__var_access_node__Call_Node]'"},
		{"let counter = 0\n        for i = 0 -> 10 >>\n            if i == 5 | i == 7 >> continue\n            counter += 1\n        <<\n        print(counter)\n        ", "'ListNode__[IDENTIFIER:counter__var_assign_node', \"For_Node__ListNode__['[(( ( INTEGER:7__NumberNode EE IDENTIFIER:i__var_access_node ) KEYWORD:or ( INTEGER:5__NumberNode EE IDENTIFIER:i__var_access_node ) ), __ContinueNode__, false)]__<nil>__IfNode', 'IDENTIFIER:counter__var_assign_node]\", 'IDENTIFIER:print__var_access_node__Call_Node]'"},
		{"let i=0\n        while i < 5 >>\n            print(i) \n            i = 1 + i \n        <<\n        print(i == 4)\n        ", "'ListNode__[IDENTIFIER:i__var_assign_node', \"While_Node__ListNode__['IDENTIFIER:print__var_access_node__Call_Node', 'IDENTIFIER:i__var_assign_node]\", 'IDENTIFIER:print__var_access_node__Call_Node]'"},
		{"let x = 0; print(x+1)", "ListNode__[IDENTIFIER:x__var_assign_node', 'IDENTIFIER:print__var_access_node__Call_Node]"},
		{"let x = \"test_case\"; print(x + \" hello\")", "ListNode__[IDENTIFIER:x__var_assign_node', 'IDENTIFIER:print__var_access_node__Call_Node]"},
		{"let x = 17; print(x*2 + 7 / 3 - 8)", "ListNode__[IDENTIFIER:x__var_assign_node', 'IDENTIFIER:print__var_access_node__Call_Node]"},
	}
	fmt.Println("started Testing")

	for i, Case := range testCases {
		fmt.Println(i)

		runner(i, Case, t)

	}
	fmt.Println(testCases)
}

// wg *sync.WaitGroup
func runner(i int, Case testCase, t *testing.T) {
	// defer wg.Done()
	lex := lexer.CreateLexer("test.hope", Case.expresion)
	tokens, err := lex.Tokenize()

	// fmt.Printf("finsh plexing in %d\n", i)

	par := Parser{Tokens: tokens, idx: 0, currToken: tokens[0]}
	ast := par.Parse()

	got := ast.node.String()

	fmt.Printf("finsh Parsing in %d\n", i)

	if !reflect.DeepEqual(got, Case.want) {
		if err == nil {
			t.Errorf("parser(%q) =\n %v; want \n %v", Case.expresion, got, Case.want)
			t.Errorf("Failed TestCase : %d\n", i)
		} else {
			t.Errorf("lexer returned an error: %v", err)
		}
	} else {
		fmt.Printf("Passed TestCase : %d\n", i)
	}
	fmt.Println("finisjed ")
}
