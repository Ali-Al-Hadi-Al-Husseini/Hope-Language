package lexer

type Token struct {
	Type   string
	Value  string
	Pos    Position
	EndPos Position
}

func (tok Token) Matches(_type string, value string) bool {
	return tok.Type == _type && tok.Value == value
}

type Position struct {
	Idx  int
	Line int
	Col  int
	File *CodeFile
}

func (pos *Position) Advance(currChar byte) Position {
	pos.Idx += 1
	pos.Col += 1

	if currChar == '\n' {
		pos.Line += 1
		pos.Col += 1
	}
	return *pos
}

type CodeFile struct {
	Name string
	Text string
}
