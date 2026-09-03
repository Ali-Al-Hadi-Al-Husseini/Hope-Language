package lexer

type Token struct {
	Type  string
	Value string
	Position
}

type Position struct {
	Idx  int
	Line int
	Col  int
	CodeFile
}
type CodeFile struct {
	Name string
	Text string
}

func (pos *Position) Advance(currChar string) Position {
	pos.Idx += 1
	pos.Col += 1

	if currChar == "\n" {
		pos.Line += 1
		pos.Col += 1
	}
	return *pos
}
func (pos Position) Copy() Position {
	return pos
}
