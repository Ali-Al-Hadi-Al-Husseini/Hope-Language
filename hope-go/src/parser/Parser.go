package parser

import (
	"fmt"

	LangErr "github.com/Ali-Al-Hadi-Al-Husseini/Hope-Language/hope-go/src/langErr"
	"github.com/Ali-Al-Hadi-Al-Husseini/Hope-Language/hope-go/src/lexer"
)

type Parser struct {
	Tokens    []lexer.Token
	idx       int
	currToken lexer.Token
}

func (par *Parser) advance() lexer.Token {
	par.idx += 1
	if par.idx >= 0 && par.idx < len(par.Tokens) {
		par.currToken = par.Tokens[par.idx]
	}
	return par.currToken
}

func (par *Parser) RegisterAdvancement(res ParserResult) {
	res.RegisterAdvancement()
	par.advance()
}

func (par *Parser) reverse(amount int) lexer.Token {
	par.idx -= amount
	if par.idx >= 0 && par.idx < len(par.Tokens) {
		par.currToken = par.Tokens[par.idx]
	}
	return par.currToken
}

func (par *Parser) Parse() ParserResult {
	result := par.GetStatments()
	if result.Err != nil && par.currToken.Type != lexer.TOKEN_EOF {
		return *result.Failure(&LangErr.LangError{
			Name:     "InvalidSyntaxErorr",
			Details:  "Expected  '+', '-', '*' , '/'  or any other operation",
			StartPos: &par.currToken.Pos,
			EndPos:   &par.currToken.Pos,
		})
	}

	return result
}

func (par *Parser) GetStatments() ParserResult {
	res := ParserResult{}
	stmts := []Node{}
	startPos := par.currToken.Pos

	for par.currToken.Type == lexer.TOKEN_NEWLINE {
		par.RegisterAdvancement(res)
	}

	statement := res.Register(par.statement())
	if res.Err != nil {
		return res
	}
	stmts = append(stmts, statement)
	moreStatements := true

	for true {
		newLineCount := 0
		for par.currToken.Type == lexer.TOKEN_NEWLINE {
			par.RegisterAdvancement(res)
			newLineCount += 1
		}

		if newLineCount == 0 {
			moreStatements = false
		}

		if !moreStatements {
			break
		}
		statement = res.Register(par.statement())
		if statement == nil {
			par.reverse(res.reverseCount)
			moreStatements = false
			continue
		}
		stmts = append(stmts, statement)
	}
	return *res.Succses(&ListNode{
		Elements: stmts,
		BaseNode: BaseNode{
			StartPos: &startPos,
			EndPos:   &par.currToken.Pos,
		},
	})

}

func (par *Parser) statement() ParserResult {
	res := ParserResult{}
	startPos := par.currToken.Pos

	if par.currToken.Matches(lexer.TOKEN_KEYWORD, "return") {
		par.RegisterAdvancement(res)
		expr, err := res.TryRegister(par.Expression())
		if err != nil {
			par.reverse(res.reverseCount)
		}
		return *res.Succses(&ReturnNode{
			node:     expr,
			BaseNode: BaseNode{StartPos: &startPos, EndPos: &par.currToken.EndPos},
		})
	}
	if par.currToken.Matches(lexer.TOKEN_KEYWORD, "continue") {
		par.RegisterAdvancement(res)

		return *res.Succses(&ContinueNode{
			BaseNode: BaseNode{StartPos: &startPos, EndPos: &par.currToken.EndPos},
		})
	}
	if par.currToken.Matches(lexer.TOKEN_KEYWORD, "break") {
		par.RegisterAdvancement(res)

		return *res.Succses(&BreakNode{
			BaseNode: BaseNode{StartPos: &startPos, EndPos: &par.currToken.EndPos},
		})
	}

	expr := res.Register(par.Expression())
	if res.Err != nil {
		return *res.Failure(&LangErr.LangError{
			Name:     "InvalidSyntaxErorr",
			Details:  "Expected 'let', int, float, identifier, keyword,  '+', '-' or '(' ",
			StartPos: &par.currToken.Pos,
			EndPos:   &par.currToken.Pos,
		})
	}
	return *res.Succses(expr)
}

func (par *Parser) Expression() ParserResult {
	res := ParserResult{}

	for par.currToken.Type == lexer.TOKEN_NEWLINE {
		par.RegisterAdvancement(res)
	}

	if par.currToken.Matches(lexer.TOKEN_IDENTIFIER, "let") {
		par.RegisterAdvancement(res)

		if par.currToken.Type != lexer.TOKEN_IDENTIFIER {
			return *res.Failure(&LangErr.LangError{
				Name:    "InvalidSyntaxErorr",
				Details: fmt.Sprintf("Expected identifier found %s '%s'", par.currToken.Type, par.currToken.Value),
			})
		}

		varName := par.currToken
		par.RegisterAdvancement(res)

		if par.currToken.Type != lexer.TOKEN_EQ {
			return *res.Failure(&LangErr.LangError{
				Name:     "InvalidSyntaxErorr",
				Details:  fmt.Sprintf("Expected '=' found %s '%s'", par.currToken.Type, par.currToken.Value),
				StartPos: &par.currToken.Pos,
				EndPos:   &par.currToken.EndPos,
			})
		}

		par.RegisterAdvancement(res)
		expr := res.Register(par.Expression())

		if res.Err != nil {
			return res
		}
		return *res.Succses(&VarAssignNode{
			NameToken: varName,
			ValueNode: expr,
		})
	}
	node := res.Register(par.BinOperation(par.Comparison_expression, []string{"and", "or"}))
	if res.Err != nil {
		return *res.Failure(&LangErr.LangError{
			Name:     "InvalidSyntaxErorr",
			Details:  "Expected 'let', int, float, identifier, '+', '-' or '(' ",
			StartPos: &par.currToken.Pos,
			EndPos:   &par.currToken.EndPos,
		})
	}
	return *res.Succses(node)
}

func (par *Parser) BinOperation(operationFunc func() ParserResult, operations []string) ParserResult {
	res := ParserResult{}
	left := res.Register(operationFunc())
	if res.Err != nil {
		return res
	}
	for {
		matched := false

		for _, op := range operations {
			if par.currToken.Type == "KEYWORD" {
				if par.currToken.Value == op {
					matched = true
					break
				}

			} else if par.currToken.Type == op {
				matched = true
				break
			}
		}
		if !matched {
			break
		}
		opToken := par.currToken
		res.RegisterAdvancement()
		right := res.Register(operationFunc())

		left = &BinOpertaionNode{
			LeftNode:  left,
			RightNode: right,
			Operation: opToken,
		}
	}

	return *res.Succses(left)
}

func (par *Parser) Comparison_expression() ParserResult {
	res := ParserResult{}
	return res
}
