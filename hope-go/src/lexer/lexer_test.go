package lexer

import (
	"errors"
	"fmt"
	"reflect"
	"testing"

	"github.com/Ali-Al-Hadi-Al-Husseini/Hope-Language/hope-go/src/LangErr"
)

type testcase struct {
	expresion string
	want      []string
}

var fuzzEdgeSeeds = []string{
	"",
	"\"\"",
	"''",
	"\"a\"",
	"'a'",
	"'unclosed",
	"\"unclosed",
	"123.",
	".5",
	"0123",
	"123.12.1",
	"+=",
	"-=",
	"*=",
	"/=",
	"%=",
	"^=",
	"->",
	"--",
	">>",
	"<<",
	">=",
	"<=",
	"==",
	"!=",
	"=",
	"!",
	"&",
	"|",
	"# comment without newline",
	"# comment with newline\nlet x = 1",
	";;;\n\n\t  \n",
	"let x = 1; y += 2",
	"+= 1",
	"func f(a, b) >> return a + b\n<<",
	"\x00",
}
var tests = []testcase{
	{"", []string{"EOF"}},
	{"# comment test", []string{"EOF"}},
	{"1.731", []string{"FLOAT:1.731", "EOF"}},
	{"123 ", []string{"INTEGER:123", "EOF"}},
	{"!=", []string{"NE", "EOF"}},
	{"==", []string{"EE", "EOF"}},
	{"!", []string{"NOT", "EOF"}},
	{">=", []string{"GTE", "EOF"}},
	{">", []string{"GT", "EOF"}},
	{"<", []string{"LT", "EOF"}},
	{"<=", []string{"LTE", "EOF"}},
	{"!true", []string{"NOT", "IDENTIFIER:true", "EOF"}},
	{"1 ^ 2", []string{"INTEGER:1", "POW", "INTEGER:2", "EOF"}},
	{"1 != 2", []string{"INTEGER:1", "NE", "INTEGER:2", "EOF"}},
	{"3 == 3", []string{"INTEGER:3", "EE", "INTEGER:3", "EOF"}},
	{"123 \n", []string{"INTEGER:123", "NEWLINE", "EOF"}},
	{"12 + 3 ", []string{"INTEGER:12", "PLUS", "INTEGER:3", "EOF"}},
	{"(2+1) ", []string{"LPAREN", "INTEGER:2", "PLUS", "INTEGER:1", "RPAREN", "EOF"}},
	{"(-2+1) ", []string{"LPAREN", "MINUS", "INTEGER:2", "PLUS", "INTEGER:1", "RPAREN", "EOF"}},
	{"(7 * 2) ", []string{"LPAREN", "INTEGER:7", "MUL", "INTEGER:2", "RPAREN", "EOF"}},
	{"(7 * 3) ", []string{"LPAREN", "INTEGER:7", "MUL", "INTEGER:3", "RPAREN", "EOF"}},
	{"(3 / 3) ", []string{"LPAREN", "INTEGER:3", "DIV", "INTEGER:3", "RPAREN", "EOF"}},
	{"(9 / 3 ) ", []string{"LPAREN", "INTEGER:9", "DIV", "INTEGER:3", "RPAREN", "EOF"}},
	{"(9 / 3  + 1) ", []string{"LPAREN", "INTEGER:9", "DIV", "INTEGER:3", "PLUS", "INTEGER:1", "RPAREN", "EOF"}},
	{"(6 / 3  + 2 ) ", []string{"LPAREN", "INTEGER:6", "DIV", "INTEGER:3", "PLUS", "INTEGER:2", "RPAREN", "EOF"}},
	{"(9 / 3  * 2 ) ", []string{"LPAREN", "INTEGER:9", "DIV", "INTEGER:3", "MUL", "INTEGER:2", "RPAREN", "EOF"}},
	{"(9 / 3  - 1) ", []string{"LPAREN", "INTEGER:9", "DIV", "INTEGER:3", "MINUS", "INTEGER:1", "RPAREN", "EOF"}},
	{"(6 / 3  - 2 ) ", []string{"LPAREN", "INTEGER:6", "DIV", "INTEGER:3", "MINUS", "INTEGER:2", "RPAREN", "EOF"}},
	{"(9 / 3  * -2 ) ", []string{"LPAREN", "INTEGER:9", "DIV", "INTEGER:3", "MUL", "MINUS", "INTEGER:2", "RPAREN", "EOF"}},
	{"((9 / 3)  * 0 ) ", []string{"LPAREN", "LPAREN", "INTEGER:9", "DIV", "INTEGER:3", "RPAREN", "MUL", "INTEGER:0", "RPAREN", "EOF"}},
	{"((9 / 3) / 0 ) ", []string{"LPAREN", "LPAREN", "INTEGER:9", "DIV", "INTEGER:3", "RPAREN", "DIV", "INTEGER:0", "RPAREN", "EOF"}},
	{" 'abc' * 'xyz'  ", []string{"STRING:abc", "MUL", "STRING:xyz", "EOF"}},
	{"if true >> print('i') ", []string{"KEYWORD:if", "IDENTIFIER:true", "UNTIL", "IDENTIFIER:print", "LPAREN", "STRING:i", "RPAREN", "EOF"}},
	{"if false >> print(1) ", []string{"KEYWORD:if", "IDENTIFIER:false", "UNTIL", "IDENTIFIER:print", "LPAREN", "INTEGER:1", "RPAREN", "EOF"}},
	{"if true >> print(1) ", []string{"KEYWORD:if", "IDENTIFIER:true", "UNTIL", "IDENTIFIER:print", "LPAREN", "INTEGER:1", "RPAREN", "EOF"}},
	{" let a = 2 \n        if a < 2 >> \n            print('hello')\n        elif a == 2 >> \n            print('world')\n        else >>\n            print('!')\n        <<\n         ", []string{"KEYWORD:let", "IDENTIFIER:a", "EQ", "INTEGER:2", "NEWLINE", "KEYWORD:if", "IDENTIFIER:a", "LT", "INTEGER:2", "UNTIL", "NEWLINE", "IDENTIFIER:print", "LPAREN", "STRING:hello", "RPAREN", "NEWLINE", "KEYWORD:elif", "IDENTIFIER:a", "EE", "INTEGER:2", "UNTIL", "NEWLINE", "IDENTIFIER:print", "LPAREN", "STRING:world", "RPAREN", "NEWLINE", "KEYWORD:else", "UNTIL", "NEWLINE", "IDENTIFIER:print", "LPAREN", "STRING:!", "RPAREN", "NEWLINE", "SKIP", "NEWLINE", "EOF"}},
	{" func add(a,b) >>  a + b\n        let z = add(1,2)   \n         ", []string{"KEYWORD:func", "IDENTIFIER:add", "LPAREN", "IDENTIFIER:a", " COMMA", "IDENTIFIER:b", "RPAREN", "UNTIL", "IDENTIFIER:a", "PLUS", "IDENTIFIER:b", "NEWLINE", "KEYWORD:let", "IDENTIFIER:z", "EQ", "IDENTIFIER:add", "LPAREN", "INTEGER:1", " COMMA", "INTEGER:2", "RPAREN", "NEWLINE", "EOF"}},
	{"let add =  func (a,b) >>  a + b\n        let z = add(1,2)   \n         ", []string{"KEYWORD:let", "IDENTIFIER:add", "EQ", "KEYWORD:func", "LPAREN", "IDENTIFIER:a", " COMMA", "IDENTIFIER:b", "RPAREN", "UNTIL", "IDENTIFIER:a", "PLUS", "IDENTIFIER:b", "NEWLINE", "KEYWORD:let", "IDENTIFIER:z", "EQ", "IDENTIFIER:add", "LPAREN", "INTEGER:1", " COMMA", "INTEGER:2", "RPAREN", "NEWLINE", "EOF"}},
	{"let add =  func (a,b) >> \n        return a + b\n        <<\n        let z = add(1,2)   \n         ", []string{"KEYWORD:let", "IDENTIFIER:add", "EQ", "KEYWORD:func", "LPAREN", "IDENTIFIER:a", " COMMA", "IDENTIFIER:b", "RPAREN", "UNTIL", "NEWLINE", "KEYWORD:return", "IDENTIFIER:a", "PLUS", "IDENTIFIER:b", "NEWLINE", "SKIP", "NEWLINE", "KEYWORD:let", "IDENTIFIER:z", "EQ", "IDENTIFIER:add", "LPAREN", "INTEGER:1", " COMMA", "INTEGER:2", "RPAREN", "NEWLINE", "EOF"}},
	{"func add (a,b) >> \n\n            if a > b >>\n                return a+b + 1 \n         else >> \n                return a + b -1\n            <<\n        <<\n        let z = add(1,2)   \n         ", []string{"KEYWORD:func", "IDENTIFIER:add", "LPAREN", "IDENTIFIER:a", " COMMA", "IDENTIFIER:b", "RPAREN", "UNTIL", "NEWLINE", "KEYWORD:if", "IDENTIFIER:a", "GT", "IDENTIFIER:b", "UNTIL", "NEWLINE", "KEYWORD:return", "IDENTIFIER:a", "PLUS", "IDENTIFIER:b", "PLUS", "INTEGER:1", "NEWLINE", "KEYWORD:else", "UNTIL", "NEWLINE", "KEYWORD:return", "IDENTIFIER:a", "PLUS", "IDENTIFIER:b", "MINUS", "INTEGER:1", "NEWLINE", "SKIP", "NEWLINE", "SKIP", "NEWLINE", "KEYWORD:let", "IDENTIFIER:z", "EQ", "IDENTIFIER:add", "LPAREN", "INTEGER:1", " COMMA", "INTEGER:2", "RPAREN", "NEWLINE", "EOF"}},
	{"for i= 1 -> 5 >> print(i) ", []string{"KEYWORD:for", "IDENTIFIER:i", "EQ", "INTEGER:1", "ARROW", "INTEGER:5", "UNTIL", "IDENTIFIER:print", "LPAREN", "IDENTIFIER:i", "RPAREN", "EOF"}},
	{"for i= 1 -> 5 >> let a = i  ", []string{"KEYWORD:for", "IDENTIFIER:i", "EQ", "INTEGER:1", "ARROW", "INTEGER:5", "UNTIL", "KEYWORD:let", "IDENTIFIER:a", "EQ", "IDENTIFIER:i", "EOF"}},
	{"for i= 1 -- 5 >> print(i)  ", []string{"KEYWORD:for", "IDENTIFIER:i", "EQ", "INTEGER:1", "MINUS", "MINUS", "INTEGER:5", "UNTIL", "IDENTIFIER:print", "LPAREN", "IDENTIFIER:i", "RPAREN", "EOF"}},
	{"let i = 0\n        while i < 5 >> i +=  1\n        print(i)\n         ", []string{"KEYWORD:let", "IDENTIFIER:i", "EQ", "INTEGER:0", "NEWLINE", "KEYWORD:while", "IDENTIFIER:i", "LT", "INTEGER:5", "UNTIL", "IDENTIFIER:i", "PLUS", "EQ", "INTEGER:1", "NEWLINE", "IDENTIFIER:print", "LPAREN", "IDENTIFIER:i", "RPAREN", "NEWLINE", "EOF"}},
	{"let i = 0\n        while i < 10 >> \n            i +=  1\n            if i == 5  >> break\n        <<\n        print(i)\n         ", []string{"KEYWORD:let", "IDENTIFIER:i", "EQ", "INTEGER:0", "NEWLINE", "KEYWORD:while", "IDENTIFIER:i", "LT", "INTEGER:10", "UNTIL", "NEWLINE", "IDENTIFIER:i", "PLUS", "EQ", "INTEGER:1", "NEWLINE", "KEYWORD:if", "IDENTIFIER:i", "EE", "INTEGER:5", "UNTIL", "KEYWORD:break", "NEWLINE", "SKIP", "NEWLINE", "IDENTIFIER:print", "LPAREN", "IDENTIFIER:i", "RPAREN", "NEWLINE", "EOF"}},
	{"let counter = 0\n        for i = 0 -> 10 >>\n            if i == 5 | i == 7 >> continue\n            counter += 1\n        <<\n        print(counter)\n         ", []string{"KEYWORD:let", "IDENTIFIER:counter", "EQ", "INTEGER:0", "NEWLINE", "KEYWORD:for", "IDENTIFIER:i", "EQ", "INTEGER:0", "ARROW", "INTEGER:10", "UNTIL", "NEWLINE", "KEYWORD:if", "IDENTIFIER:i", "EE", "INTEGER:5", "KEYWORD:or", "IDENTIFIER:i", "EE", "INTEGER:7", "UNTIL", "KEYWORD:continue", "NEWLINE", "IDENTIFIER:counter", "PLUS", "EQ", "INTEGER:1", "NEWLINE", "SKIP", "NEWLINE", "IDENTIFIER:print", "LPAREN", "IDENTIFIER:counter", "RPAREN", "NEWLINE", "EOF"}},
	{"let i=0\n        while i < 5 >>\n            print(i) \n            i = 1 + i \n        <<\n        print(i == 4)\n         ", []string{"KEYWORD:let", "IDENTIFIER:i", "EQ", "INTEGER:0", "NEWLINE", "KEYWORD:while", "IDENTIFIER:i", "LT", "INTEGER:5", "UNTIL", "NEWLINE", "IDENTIFIER:print", "LPAREN", "IDENTIFIER:i", "RPAREN", "NEWLINE", "IDENTIFIER:i", "EQ", "INTEGER:1", "PLUS", "IDENTIFIER:i", "NEWLINE", "SKIP", "NEWLINE", "IDENTIFIER:print", "LPAREN", "IDENTIFIER:i", "EE", "INTEGER:4", "RPAREN", "NEWLINE", "EOF"}},
	{"let x = 0; print(x+1) ", []string{"KEYWORD:let", "IDENTIFIER:x", "EQ", "INTEGER:0", "NEWLINE", "IDENTIFIER:print", "LPAREN", "IDENTIFIER:x", "PLUS", "INTEGER:1", "RPAREN", "EOF"}},
	{"let x = 'test_case'; print(x + ' hello') ", []string{"KEYWORD:let", "IDENTIFIER:x", "EQ", "STRING:test_case", "NEWLINE", "IDENTIFIER:print", "LPAREN", "IDENTIFIER:x", "PLUS", "STRING: hello", "RPAREN", "EOF"}},
	{"let x = 17; print(x*2 + 7 / 3 - 8) ", []string{"KEYWORD:let", "IDENTIFIER:x", "EQ", "INTEGER:17", "NEWLINE", "IDENTIFIER:print", "LPAREN", "IDENTIFIER:x", "MUL", "INTEGER:2", "PLUS", "INTEGER:7", "DIV", "INTEGER:3", "MINUS", "INTEGER:8", "RPAREN", "EOF"}},

	// test case that produces erros
	{"'hola", []string{"expected legal char found: EOF"}},
	{"123.12.1", []string{"Found more than one dot in Float"}},
	{"@", []string{"expected legal char found: @"}},
	{"$", []string{"expected legal char found: $"}},
	{"~", []string{"expected legal char found: ~"}},
}

func TestLexer(t *testing.T) {
	for i, tt := range tests {
		t.Run(tt.expresion, func(t *testing.T) {
			lex := CreateLexer("test.hope", tt.expresion)

			tokens, err := lex.Tokenize()

			if err != nil {
				var targetErr *LangErr.LangError
				if errors.As(err, &targetErr) {
					if !reflect.DeepEqual(targetErr.Details, tt.want[0]) {
						t.Errorf("lexer(%q) = %v; want %v", tt.expresion, err, tt.want)
					}
				} else {
					t.Errorf("lexer(%q) = %v; want %v", tt.expresion, err, tt.want)
				}
				return
			}
			got := make([]string, len(tokens))
			for i, token := range tokens {
				if token.Value != "" {
					got[i] = token.Type + ":" + token.Value
				} else {
					got[i] = token.Type
				}
			}

			if !reflect.DeepEqual(got, tt.want) {
				t.Errorf("lexer(%q) = %v; want %v", tt.expresion, got, tt.want)

			} else {
				fmt.Printf("Passed TestCase : %d\n", i)
			}
		})
	}
}
