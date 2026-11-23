package lexer

import (
	"fmt"

	"github.com/Ali-Al-Hadi-Al-Husseini/Hope-Language/hope-go/src/LangErr"
	position "github.com/Ali-Al-Hadi-Al-Husseini/Hope-Language/hope-go/src/Position"
)

type lexer struct {
	currChar byte
	pos      *position.Position
	File     *position.CodeFile
}

func CreateLexer(fileName string, code string) lexer {
	fl := position.CodeFile{Name: fileName, Text: code}
	pos := position.Position{Idx: -1, Line: -1, Col: -1, File: &fl}
	return lexer{currChar: '0', pos: &pos, File: &fl}
}
func (lex *lexer) Tokenize() ([]Token, error) {
	tokens := []Token{}

	lex.advance()
	for lex.pos.Idx < len(lex.File.Text) {

		switch lex.currChar {
		case ' ', '\t':
			lex.advance()
		case '#':
			lex.advance()
			for lex.currChar != '\n' && len(lex.File.Text) > lex.pos.Idx {
				lex.advance()
			}
			lex.advance()
		case ';', '\n':
			tokens = append(tokens, lex.makeNewLine())

		case '"', '\'':
			tok, err := lex.makeStr()
			if err != nil {
				return tokens, err
			}
			tokens = append(tokens, tok)

		case '-':
			tok, err := lex.makeArrowOrMinus(&tokens)
			if err != nil {
				return []Token{}, err
			}
			tokens = append(tokens, tok)

		case '+', '/', '*', '%', '^':
			opType, _ := symbols[lex.currChar]
			tok, _ := lex.makeOperationAndEqual(&tokens, opType, true)

			tokens = append(tokens, tok)

		case '!':
			tokens = append(tokens, lex.makeNotEqual())

		case '&', '|':
			tokens = append(tokens, lex.makeLogicalGate())

		case '{', '}', '[', ']', '(', ')', ',':
			tokens = append(tokens,
				Token{
					Type: symbols[lex.currChar],
					Pos:  *lex.pos,
				})
			lex.advance()

		case '=':
			tokens = append(tokens, lex.makeEqual())

		case '>', '<':
			tokens = append(tokens, lex.makeGtLt())

		default:
			switch {
			case isdigit(lex.currChar):
				currToken, err := lex.makeNumber()
				if err != nil {
					return []Token{}, err
				}
				tokens = append(tokens, currToken)

			case isLetter(lex.currChar):
				tokens = append(tokens, lex.makeIdentifier())

			default:

				return []Token{}, &LangErr.LangError{
					Name:     "IllegalChar",
					Details:  fmt.Sprintf("expected legal char found: %c", lex.currChar),
					StartPos: lex.pos,
				}
			}

		}
	}
	tokens = append(tokens, Token{Type: TOKEN_EOF, Pos: *lex.pos})
	return tokens, nil
}

func (lex *lexer) advance() {
	lex.pos.Advance(lex.currChar)
	if lex.pos.Idx < len(lex.File.Text) {
		lex.currChar = lex.File.Text[lex.pos.Idx]

	} else {
		lex.currChar = 0
	}
}
func (lex *lexer) makeNumber() (Token, error) {
	dotCount := 0
	start_pos := *lex.pos
	idx := start_pos.Idx

	for idx < len(lex.pos.File.Text) && (isdigit(lex.currChar) || lex.currChar == '.') {
		if lex.currChar == '.' {
			if dotCount > 0 {
				return Token{}, &LangErr.LangError{
					Name:     "IllegalChar",
					Details:  fmt.Sprintf("expected more numbers found: %c", lex.currChar),
					StartPos: lex.pos,
				}
			}
			dotCount += 1
		}
		idx += 1
		lex.advance()
	}
	if dotCount == 0 {
		return Token{
			Type:   TOKEN_INT,
			Value:  string(lex.File.Text[start_pos.Idx:idx]),
			Pos:    start_pos,
			EndPos: *lex.pos,
		}, nil
	}

	return Token{
		Type:   TOKEN_FLOAT,
		Value:  string(lex.File.Text[start_pos.Idx:idx]),
		Pos:    start_pos,
		EndPos: *lex.pos,
	}, nil

}
func (lex *lexer) makeNewLine() Token {
	tok := Token{Type: TOKEN_NEWLINE, Pos: *lex.pos}
	lex.advance()

	for (lex.currChar == '\n' || lex.currChar == ';') && lex.currChar != 0 {
		lex.advance()
	}
	return tok
}
func (lex *lexer) makeStr() (Token, error) {
	startPos := *lex.pos
	strStart := lex.pos.Idx + 1
	currQuotes := lex.currChar
	lex.advance()

	for (lex.currChar != currQuotes) && lex.pos.Idx < len(lex.File.Text) {
		lex.advance()

	}

	if lex.currChar != currQuotes {
		return Token{}, &LangErr.LangError{
			Name:     "IllegalChar",
			Details:  fmt.Sprintf("expected legal char found: %c", lex.currChar),
			StartPos: lex.pos,
		}
	}
	lex.advance()
	val := lex.File.Text[strStart : lex.pos.Idx-1]
	return Token{Type: TOKEN_STRING, Value: val, Pos: startPos, EndPos: *lex.pos}, nil
}

// create tokens for op or op=
func (lex *lexer) makeOperationAndEqual(tokens *[]Token, opType string, advance bool) (Token, error) {
	startPos := *lex.pos

	if advance {
		lex.advance()
	}
	// optimzation here might be needed to use less tokens
	if lex.currChar == '=' {
		*tokens = append(*tokens, Token{Type: TOKEN_EQ, Pos: startPos})
		if len(*tokens) > 2 {
			previous := (*tokens)[len(*tokens)-2].Value
			*tokens = append(*tokens, Token{Type: TOKEN_IDENTIFIER, Value: previous, Pos: startPos})
		}
		lex.advance()
		return Token{Type: opType, Pos: *lex.pos}, nil

	}

	return Token{Type: opType, Pos: startPos}, nil
}

// if a Token starts with - so it might an arrow , minus or -=
func (lex *lexer) makeArrowOrMinus(tokens *[]Token) (Token, error) {
	startPos := *lex.pos
	lex.advance()

	if lex.currChar == '>' {
		lex.advance()
		return Token{Type: TOKEN_ARROW, Pos: startPos, EndPos: *lex.pos}, nil
	}
	return lex.makeOperationAndEqual(tokens, TOKEN_MINUS, false)
}

// a function  that checks if '>' or '<'  are followed by and equals sign '=' to change its type
func (lex *lexer) makeGtLt() Token {
	startPos := *lex.pos
	tokType, _ := symbols[lex.currChar]
	lex.advance()

	if lex.currChar == '>' && tokType == TOKEN_GT {
		lex.advance()
		return Token{Type: TOKEN_START, Pos: startPos, EndPos: *lex.pos}
	} else if lex.currChar == '<' && tokType == TOKEN_LT {
		lex.advance()
		return Token{Type: TOKEN_END, Pos: startPos, EndPos: *lex.pos}
	}
	if lex.currChar == '=' {
		tokType += "E"
		lex.advance()
	}
	return Token{Type: tokType, Pos: startPos, EndPos: *lex.pos}
}
func (lex *lexer) makeEqual() Token {
	startPos := *lex.pos
	lex.advance()
	if lex.currChar == '=' {
		lex.advance()
		return Token{Type: TOKEN_EE, Pos: startPos, EndPos: *lex.pos}
	}
	return Token{Type: TOKEN_EQ, Pos: startPos, EndPos: *lex.pos}
}
func (lex *lexer) makeNotEqual() Token {
	startPos := *lex.pos
	lex.advance()
	if lex.currChar == '=' {
		lex.advance()
		return Token{Type: TOKEN_NE, Pos: startPos, EndPos: *lex.pos}
	}

	return Token{Type: TOKEN_NOT, Pos: startPos, EndPos: *lex.pos}
}
func (lex *lexer) makeIdentifier() Token {
	identIdx := lex.pos.Idx
	startPos := *lex.pos

	for lex.currChar != 0 && (isLetter(lex.currChar) || isdigit(lex.currChar)) {
		lex.advance()
	}

	identfier := lex.File.Text[identIdx:lex.pos.Idx]
	_, ok := KEYWORDS[identfier]
	if !ok {
		return Token{Type: TOKEN_IDENTIFIER, Value: identfier, Pos: startPos, EndPos: *lex.pos}
	}
	return Token{Type: TOKEN_KEYWORD, Value: identfier, Pos: startPos, EndPos: *lex.pos}
}
func (lex *lexer) makeLogicalGate() Token {
	startPos := *lex.pos
	currSymbol, _ := symbols[lex.currChar]
	lex.advance()
	return Token{Type: TOKEN_KEYWORD, Value: currSymbol, Pos: startPos, EndPos: *lex.pos}
}

func isdigit(ch byte) bool {
	return '0' <= ch && '9' >= ch
}
func isLetter(ch byte) bool {

	return ('a' <= ch && ch <= 'z') || ('A' <= ch && ch <= 'Z') || (ch == '_')
}
