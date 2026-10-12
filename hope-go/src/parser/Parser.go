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

	return res

}
