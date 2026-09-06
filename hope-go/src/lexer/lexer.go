package lexer

import "fmt"

type Lexer struct {
	CurrChar byte
	Pos      *Position
	File     *CodeFile
}

func (lexer *Lexer) lexer(code string) ([]Token, error) {
	tokens := []Token{}

	for lexer.CurrChar != 0 {

		switch lexer.CurrChar {
		case ' ', '\t':
			lexer.advance(true)
		case '#':
			lexer.advance(true)
			for lexer.CurrChar != '\n' {
				lexer.advance(true)
			}
			lexer.advance(true)
		case ';', '\n':
			lexer.makeNewLine()

		case '"', '\'':
			lexer.makeStr()

		case '+', '-', '/', '*', '%', '^':
			lexer.makeOperationAndEqual()

		case '!':
			lexer.makeNotEqual()

		case '&', '|':
			lexer.makeLogicalGate()

		case '{', '}', '[', ']', '(', ')':
			// add token here
			lexer.advance(true)

		case '=':
			lexer.makeEqual()

		case '>', '<':
			lexer.makeGtLt()

		default:
			switch {
			case isdigit(lexer.CurrChar):
				lexer.makeNumber()

			case isLetter(lexer.CurrChar):
				lexer.makeIdentifier()

			default:
				return []Token{}, fmt.Errorf("IllegalChar")
			}

		}
	}
	return tokens, nil
}

func (lexer *Lexer) advance(advanceChar bool) {
	lexer.Pos.Advance(lexer.CurrChar)
	if !advanceChar {
		return
	}
	if lexer.Pos.Idx < len(lexer.File.Text) {
		lexer.CurrChar = lexer.File.Text[lexer.Pos.Idx]

	} else {
		lexer.CurrChar = 0
	}
}
func (Lexer *Lexer) makeNumber() {

}
func (Lexer *Lexer) makeNewLine() {

}
func (Lexer *Lexer) makeStr() {

}
func (Lexer *Lexer) makeOperationAndEqual() {

}
func (Lexer *Lexer) makeArrowOrMinus() {

}
func (Lexer *Lexer) makeGtLt() {

}
func (Lexer *Lexer) makeEqual() {

}
func (Lexer *Lexer) makeNotEqual() {

}
func (Lexer *Lexer) makeIdentifier() {

}
func (Lexer *Lexer) makeLogicalGate() {

}

func isdigit(ch byte) bool {
	return '0' <= ch && '9' >= ch
}
func isLetter(ch byte) bool {

	return ('a' <= ch && ch <= 'z') || ('A' <= ch && ch <= 'Z')
}
