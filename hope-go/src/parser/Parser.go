package parser

import (
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
