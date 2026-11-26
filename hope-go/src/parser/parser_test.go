package parser

import (
	"errors"
	"fmt"
	"reflect"
	"testing"

	LangErr "github.com/Ali-Al-Hadi-Al-Husseini/Hope-Language/hope-go/src/LangErr"
	"github.com/Ali-Al-Hadi-Al-Husseini/Hope-Language/hope-go/src/lexer"
)

type testCase struct {
	expresion string
	want      string
}

var testCases = []testCase{
	{"1.731", "ListNode__[FLOAT:1.731__NumberNode]"},
	{"123 ", "ListNode__[INTEGER:123__NumberNode]"},
	{"!true", "ListNode__[(NOT, IDENTIFIER:true__var_access_node)]"},
	{"[]", "ListNode__[ListNode__[]]"},
	{"[1,2,3,4]", "ListNode__[ListNode__[INTEGER:1__NumberNode, INTEGER:2__NumberNode, INTEGER:3__NumberNode, INTEGER:4__NumberNode]]"},
	{"let x= [1,2,3,4]; x[0]", "ListNode__[IDENTIFIER:x__var_assign_node, __x__0__ListacssesNode]"},
	{"not true", "ListNode__[(KEYWORD:not, IDENTIFIER:true__var_access_node)]"},
	{"(2 ^ 1)", "ListNode__[( INTEGER:1__NumberNode POW INTEGER:2__NumberNode )]"},
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
	{" let a = 2 \n        if a < 2 >> \n            print('hello')\n        elif a == 2 >> \n            print('world')\n        else >>\n            print('!')\n        <<\n        ", "ListNode__[IDENTIFIER:a__var_assign_node, [(( INTEGER:2__NumberNode LT IDENTIFIER:a__var_access_node ), ListNode__[IDENTIFIER:print__var_access_node__Call_Node], true) (( INTEGER:2__NumberNode EE IDENTIFIER:a__var_access_node ), ListNode__[IDENTIFIER:print__var_access_node__Call_Node], true)]__(ListNode__[IDENTIFIER:print__var_access_node__Call_Node], true)__IfNode]"},
	{" func add(a,b) >>  a + b\n        let z = add(1,2)   \n        ", "ListNode__[functionDefNode__IDENTIFIER:add__( IDENTIFIER:b__var_access_node PLUS IDENTIFIER:a__var_access_node ), IDENTIFIER:z__var_assign_node]"},
	{"let add =  func (a,b) >>  a + b\n        let z = add(1,2)   \n", "ListNode__[IDENTIFIER:add__var_assign_node, IDENTIFIER:z__var_assign_node]"},
	{"let add =  func (a,b) >> \n        return a + b\n        <<\n        let z = add(1,2)   \n        ", "ListNode__[IDENTIFIER:add__var_assign_node, IDENTIFIER:z__var_assign_node]"},
	{"func add (a,b) >> \n\n            if a > b >>\n                return a+b + 1 \n         else >> \n                return a + b -1\n            <<\n        <<\n        let z = add(1,2)   \n        ", "ListNode__[functionDefNode__IDENTIFIER:add__ListNode__[[(( IDENTIFIER:b__var_access_node GT IDENTIFIER:a__var_access_node ), ListNode__[__ReturnNode__], true)]__(ListNode__[__ReturnNode__], true)__IfNode], IDENTIFIER:z__var_assign_node]"},
	{"for i= 1 -> 5 >> print(i)", "ListNode__[For_Node__IDENTIFIER:print__var_access_node__Call_Node]"},
	{"for i= 1 -> 5 >> let a = i ", "ListNode__[For_Node__IDENTIFIER:a__var_assign_node]"},
	{"let i = 0\n        while i < 5 >> i +=  1\n        print(i)\n        ", "ListNode__[IDENTIFIER:i__var_assign_node, While_Node__IDENTIFIER:i__var_assign_node, IDENTIFIER:print__var_access_node__Call_Node]"},
	{"let i = 0\n        while i < 10 >> \n            i +=  1\n            if i == 5  >> break\n        <<\n        print(i)\n        ", "ListNode__[IDENTIFIER:i__var_assign_node, While_Node__ListNode__[IDENTIFIER:i__var_assign_node, [(( INTEGER:5__NumberNode EE IDENTIFIER:i__var_access_node ), __BreakNode__, false)]__<nil>__IfNode], IDENTIFIER:print__var_access_node__Call_Node]"},
	{"let counter = 0\n        for i = 0 -> 10 >>\n            if i == 5 | i == 7 >> continue\n            counter += 1\n        <<\n        print(counter)\n        ", "ListNode__[IDENTIFIER:counter__var_assign_node, For_Node__ListNode__[[(( ( INTEGER:7__NumberNode EE IDENTIFIER:i__var_access_node ) KEYWORD:or ( INTEGER:5__NumberNode EE IDENTIFIER:i__var_access_node ) ), __ContinueNode__, false)]__<nil>__IfNode, IDENTIFIER:counter__var_assign_node], IDENTIFIER:print__var_access_node__Call_Node]"},
	{"let i=0\n        while i < 5 >>\n            print(i) \n            i = 1 + i \n        <<\n        print(i == 4)\n        ", "ListNode__[IDENTIFIER:i__var_assign_node, While_Node__ListNode__[IDENTIFIER:print__var_access_node__Call_Node, IDENTIFIER:i__var_assign_node], IDENTIFIER:print__var_access_node__Call_Node]"},
	{"let x = 0; print(x+1)", "ListNode__[IDENTIFIER:x__var_assign_node, IDENTIFIER:print__var_access_node__Call_Node]"},
	{"let x = test_case; print(x +  hello)", "ListNode__[IDENTIFIER:x__var_assign_node, IDENTIFIER:print__var_access_node__Call_Node]"},
	{"let x = 17; print(x*2 + 7 / 3 - 8)", "ListNode__[IDENTIFIER:x__var_assign_node, IDENTIFIER:print__var_access_node__Call_Node]"},
	{"for i = 1 -> 6 skip 2  >> print('i')", "ListNode__[For_Node__IDENTIFIER:print__var_access_node__Call_Node]"},
	{"func suba(a,b,c) >> \n \n  let sub = a - b \n  \n sub -= c \n \n << ", "ListNode__[functionDefNode__IDENTIFIER:suba__ListNode__[IDENTIFIER:sub__var_assign_node, IDENTIFIER:sub__var_assign_node]]"},

	// test cases that produced errors
	{"for i= 1 -- 5 >> print(i) ", "Expected '->' found UNTIL ''"},
	{"for i= 1 -> 5 >> \n print(i) ", "Expected '<<' found EOF '' "},
	{"for 1 -> 5 >> print(i) ", "Expected Identifier after For loop declartion found INTEGER '1'"},
	{"for i > 1 -> 5 >> \n print(i) ", "Expected '=' after identifier found  GT ''"},

	{"x[0}", "Expected ']' after index 0"},
	{"x['test']", "Expected index (integer or identifier) after [ "},
	{"if true ", "Expected '>>' found EOF '' "},
	{"if true {", "Expected '>>' found LCURLY '' "},
	{"while true ", "Expected '>>' found EOF '' "},
	{"[1,2,3", "Expected ',' or ']' found EOF '' "},
	{"[", "Expected ']' , keyword, identifier  or values found EOF '' "},
	{"[,", "Expected ']' , keyword, identifier  or values found  COMMA '' "},
	{"['abs',  , ] ", "Expected int, float, identifier, '+', '-' , '('  or '[' "},
	{"while true  >> \n print('1') \n ", "Expected '<<' found EOF '' "},
	{"for i = 1 -> 5  \n print('i')", "Expected '>>' found NEWLINE '' "},
	{"func suba ,b,c) >> a - b - c ", "Expected '(' after function declaration found  COMMA '' "},
	{"func sub(1,b,c) >> a - b - c ", "Expected ')' or  identifier after function declaration found INTEGER '1' "},
	{"func suba(a,7.91,c) >> a - b - c ", "Expected identifier after found FLOAT '7.91' "},
	{"func suba(a,b 77 >> a - b - c ", "Expected ')' or ','  after function declaration found INTEGER '77' "},
	{"func suba(a,b,h)  a - b - h ", "Expected '>>' after function declaration found IDENTIFIER 'a' "},
	{"func suba(a,b,h) >> \n return  a - b - h ", "Expected '<<' found EOF '' "},
	{"let mul = func (x,y) \n ", "Expected '>>' after function declaration found NEWLINE '' "},
	{"func add (a,b) >> \n\n            if a > b >>\n                return a+b + 1 \n         else  \n                return a + b -1\n            <<\n        <<\n        let z = add(1,2)   \n        ", "Expected '>>' found NEWLINE '' "},
	{"func add (a,b) >> \n\n            if a > b >>\n                return a+b + 1 \n         else  >>\n     print('hello world') \n        ", "Expected '<<' found EOF '' "},
	{"func add (a,b) >> \n\n            if a > b >>\n                return a+b + 1 \n         else  >> print('hello world') \n        ", "Expected '<<' found EOF '' "},
	{"let 123 = 8 ", "Expected identifier found INTEGER '123'"},
	{"let abc  8 ", "Expected '=' found INTEGER '8'"},
	{"let abc  = 8 ;  >> ", "Expected  '+', '-', '*' , '/'  or any other operation"},
	{"let a = (1 * 3", "Expected ')' "},
	{"sub(7,10,1 ", "Expected ',' or ')'"},
}

func TestParser(t *testing.T) {

	fmt.Println("started Testing")
	for i, Case := range testCases {
		name := fmt.Sprintf("case_%02d", i)
		t.Run(name, func(t *testing.T) {
			runner(Case, t)
		})
	}
}

// wg *sync.WaitGroup
func runner(Case testCase, t *testing.T) {
	// defer wg.Done()
	lex := lexer.CreateLexer("test.hope", Case.expresion)
	tokens, err := lex.Tokenize()
	if err != nil {
		t.Errorf("lexer returned an error: %v", err)
	}

	par := Parser{Tokens: tokens, idx: 0, currToken: tokens[0]}
	ast := par.Parse()
	if ast.Err != nil {
		var targetErr *LangErr.LangError

		if errors.As(ast.Err, &targetErr) {
			if !reflect.DeepEqual(targetErr.Details, Case.want) {
				t.Errorf("Parser(%q) = %v; want %v", targetErr.Details, err, Case.want)
			}
		}
		return
	}
	var got string
	if ast.node != nil {
		got = ast.node.String()
	} else {
		got = "<nil>"
	}

	if !reflect.DeepEqual(got, Case.want) {
		if err == nil {
			t.Errorf("parser(%q) =\n %v; want \n %v", Case.expresion, got, Case.want)
		} else {
			t.Errorf("lexer returned an error: %v", err)
		}
	}

}
