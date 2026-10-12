package parser

import (
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
	return res
}

func (par *Parser) Expression() ParserResult {

}
