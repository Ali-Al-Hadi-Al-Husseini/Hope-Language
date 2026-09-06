package lexer

type Lexer struct {
	CurrChar string
	Pos      *Position
	File     *CodeFile
}

func (lexer *Lexer) lexer(code string) []string {
	return []string{}
}

func (lexer *Lexer) advance(advanceChar bool) {
	lexer.Pos.Advance(lexer.CurrChar)
	if !advanceChar {
		return
	}
	if lexer.Pos.Idx < len(lexer.File.Text) {
		lexer.CurrChar = string(lexer.File.Text[lexer.Pos.Idx])

	} else {
		lexer.CurrChar = ""
	}
}
