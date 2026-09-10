package lexer

import "fmt"

type lexer struct {
	currChar byte
	pos      *position
	File     *CodeFile
}

func CreateLexer(fileName string, code string) lexer {
	fl := CodeFile{Name: fileName, Text: code}
	pos := position{Idx: -1, Line: -1, Col: -1, File: &fl}
	return lexer{currChar: '0', pos: &pos, File: &fl}
}
func (lex *lexer) Tokenize() ([]token, error) {
	tokens := []token{}

	lex.advance(true)
	for lex.pos.Idx < len(lex.File.Text) {

		switch lex.currChar {
		case ' ', '\t':
			lex.advance(true)
		case '#':
			lex.advance(true)
			for lex.currChar != '\n' {
				lex.advance(true)
			}
			lex.advance(true)
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
				return []token{}, fmt.Errorf("%v", err)
			}
			tokens = append(tokens, tok)

		case '+', '/', '*', '%', '^':
			opType, ok := symbols[lex.currChar]
			if !ok {
				return []token{}, fmt.Errorf("expected symbol found: %c", lex.currChar)

			}
			tok, err := lex.makeOperationAndEqual(&tokens, opType, true)
			if err != nil {
				return []token{}, fmt.Errorf("IllegalChar")
			}
			tokens = append(tokens, tok)

		case '!':
			tokens = append(tokens, lex.makeNotEqual())

		case '&', '|':
			tokens = append(tokens, lex.makeLogicalGate())

		case '{', '}', '[', ']', '(', ')', ',':
			tokens = append(tokens,
				token{
					Type: symbols[lex.currChar],
					Pos:  *lex.pos,
				})
			lex.advance(true)

		case '=':
			tokens = append(tokens, lex.makeEqual())

		case '>', '<':
			tokens = append(tokens, lex.makeGtLt())

		default:
			switch {
			case isdigit(lex.currChar):
				currToken, err := lex.makeNumber()
				if err != nil {
					return []token{}, err
				}
				tokens = append(tokens, currToken)

			case isLetter(lex.currChar):
				tokens = append(tokens, lex.makeIdentifier())

			default:
				return []token{}, fmt.Errorf("IllegalChar")
			}

		}
	}
	tokens = append(tokens, token{Type: TOKEN_EOF, Pos: *lex.pos})
	return tokens, nil
}

func (lex *lexer) advance(advanceChar bool) {
	lex.pos.Advance(lex.currChar)
	if !advanceChar {
		return
	}
	if lex.pos.Idx < len(lex.File.Text) {
		lex.currChar = lex.File.Text[lex.pos.Idx]

	} else {
		lex.currChar = 0
	}
}
func (lex *lexer) makeNumber() (token, error) {
	dotCount := 0
	start_pos := *lex.pos
	idx := start_pos.Idx

	for idx < len(lex.pos.File.Text) && isdigit(lex.currChar) {
		if lex.currChar == '.' {
			if dotCount > 0 {
				return token{}, fmt.Errorf("IllegalChar")
			}
			dotCount += 1
		}
		idx += 1
		lex.advance(true)
	}
	if dotCount == 0 {
		return token{
			Type:   TOKEN_INT,
			Value:  string(lex.File.Text[start_pos.Idx:idx]),
			Pos:    start_pos,
			EndPos: *lex.pos,
		}, nil
	}

	return token{
		Type:   TOKEN_FLOAT,
		Value:  string(lex.File.Text[start_pos.Idx:idx]),
		Pos:    start_pos,
		EndPos: *lex.pos,
	}, nil

}
func (lex *lexer) makeNewLine() token {
	tok := token{Type: TOKEN_NEWLINE, Pos: *lex.pos}
	lex.advance(true)

	if lex.currChar == 0 {
		return tok
	}

	for lex.currChar == '\n' || lex.currChar == ';' {
		lex.advance(true)
		if lex.currChar == 0 {
			return tok
		}
	}

	return tok
}
func (lex *lexer) makeStr() (token, error) {
	startPos := *lex.pos
	strStart := lex.pos.Idx + 1
	currQuotes := lex.currChar
	lex.advance(true)

	for (lex.currChar != currQuotes) && lex.pos.Idx < len(lex.File.Text) {
		lex.advance(true)

	}

	if lex.currChar != currQuotes {
		return token{}, fmt.Errorf("illgal char")
	}
	lex.advance(true)
	val := lex.File.Text[strStart : lex.pos.Idx-1]
	return token{Type: TOKEN_STRING, Value: val, Pos: startPos, EndPos: *lex.pos}, nil
}

// create tokens for op or op=
func (lex *lexer) makeOperationAndEqual(tokens *[]token, opType string, advance bool) (token, error) {
	startPos := *lex.pos

	if advance {
		lex.advance(true)
	}
	// optimzation here might be needed to use less tokens
	if lex.currChar == '=' {
		*tokens = append(*tokens, token{Type: TOKEN_EQ, Pos: startPos})
		if len(*tokens) > 2 {
			previous := (*tokens)[len(*tokens)-2].Value
			*tokens = append(*tokens, token{Type: TOKEN_IDENTIFIER, Value: previous, Pos: startPos})
		}
		lex.advance(true)
		return token{Type: opType, Pos: *lex.pos}, nil

	}

	return token{Type: opType, Pos: startPos}, nil
}

// if a token starts with - so it might an arrow , minus or -=
func (lex *lexer) makeArrowOrMinus(tokens *[]token) (token, error) {
	startPos := *lex.pos
	lex.advance(true)

	if lex.currChar == '>' {
		lex.advance(true)
		return token{Type: TOKEN_ARROW, Pos: startPos, EndPos: *lex.pos}, nil
	}
	return lex.makeOperationAndEqual(tokens, TOKEN_MINUS, false)
}

// a function  that checks if '>' or '<'  are followed by and equals sign '=' to change its type
func (lex *lexer) makeGtLt() token {
	startPos := *lex.pos
	tokType, _ := symbols[lex.currChar]
	lex.advance(true)

	if lex.currChar == '>' && tokType == TOKEN_GT {
		return token{Type: TOKEN_START, Pos: startPos, EndPos: *lex.pos}
	} else if lex.currChar == '<' && tokType == TOKEN_LT {
		return token{Type: TOKEN_END, Pos: startPos, EndPos: *lex.pos}
	}
	if lex.currChar == '=' {
		tokType += "E"
		lex.advance(true)
	}
	return token{Type: tokType, Pos: startPos, EndPos: *lex.pos}
}
func (lex *lexer) makeEqual() token {
	startPos := *lex.pos
	lex.advance(true)
	if lex.currChar == '=' {
		lex.advance(true)
		return token{Type: TOKEN_EE, Pos: startPos, EndPos: *lex.pos}
	}
	return token{Type: TOKEN_EQ, Pos: startPos, EndPos: *lex.pos}
}
func (lex *lexer) makeNotEqual() token {
	startPos := *lex.pos
	lex.advance(true)
	if lex.currChar == '=' {
		lex.advance(true)
		return token{Type: TOKEN_NE, Pos: startPos, EndPos: *lex.pos}
	}

	return token{Type: TOKEN_EQ, Pos: startPos, EndPos: *lex.pos}
}
func (lex *lexer) makeIdentifier() token {
	identIdx := lex.pos.Idx
	startPos := *lex.pos

	for lex.currChar != 0 && (isLetter(lex.currChar) || isdigit(lex.currChar)) {
		lex.advance(true)
	}

	identfier := lex.File.Text[identIdx:lex.pos.Idx]
	_, ok := KEYWORDS[identfier]
	if !ok {
		return token{Type: TOKEN_IDENTIFIER, Value: identfier, Pos: startPos, EndPos: *lex.pos}
	}
	return token{Type: TOKEN_KEYWORD, Value: identfier, Pos: startPos, EndPos: *lex.pos}
}
func (lex *lexer) makeLogicalGate() token {
	startPos := *lex.pos
	currSymbol, _ := symbols[lex.currChar]
	lex.advance(true)
	return token{Type: TOKEN_KEYWORD, Value: currSymbol, Pos: startPos, EndPos: *lex.pos}
}

func isdigit(ch byte) bool {
	return '0' <= ch && '9' >= ch
}
func isLetter(ch byte) bool {

	return ('a' <= ch && ch <= 'z') || ('A' <= ch && ch <= 'Z') || (ch == '_')
}
