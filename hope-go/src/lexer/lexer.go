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
			tokens = append(tokens, lexer.makeNewLine())

		case '"', '\'':
			tokens = append(tokens, lexer.makeStr())

		case '+', '-', '/', '*', '%', '^':
			tokens = append(tokens, lexer.makeOperationAndEqual())

		case '!':
			tokens = append(tokens, lexer.makeNotEqual())

		case '&', '|':
			tokens = append(tokens, lexer.makeLogicalGate())

		case '{', '}', '[', ']', '(', ')', ',':
			tokens = append(tokens,
				Token{
					Type:  symbols[lexer.CurrChar],
					Value: "",
					Pos:   *lexer.Pos,
				})
			lexer.advance(true)

		case '=':
			tokens = append(tokens, lexer.makeEqual())

		case '>', '<':
			tokens = append(tokens, lexer.makeGtLt())

		default:
			switch {
			case isdigit(lexer.CurrChar):
				tokens = append(tokens, lexer.makeNumber())

			case isLetter(lexer.CurrChar):
				tokens = append(tokens, lexer.makeIdentifier())

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
func (Lexer *Lexer) makeNumber() Token {
	return Token{}
}
func (Lexer *Lexer) makeNewLine() Token {
	return Token{}
}
func (Lexer *Lexer) makeStr() Token {
	return Token{}
}
func (Lexer *Lexer) makeOperationAndEqual() Token {
	return Token{}
}
func (Lexer *Lexer) makeArrowOrMinus() Token {
	return Token{}
}
func (Lexer *Lexer) makeGtLt() Token {
	return Token{}
}
func (Lexer *Lexer) makeEqual() Token {
	return Token{}
}
func (Lexer *Lexer) makeNotEqual() Token {
	return Token{}
}
func (Lexer *Lexer) makeIdentifier() Token {
	return Token{}
}
func (Lexer *Lexer) makeLogicalGate() Token {
	return Token{}
}

func isdigit(ch byte) bool {
	return '0' <= ch && '9' >= ch
}
func isLetter(ch byte) bool {

	return ('a' <= ch && ch <= 'z') || ('A' <= ch && ch <= 'Z') || (ch == '_')
}
