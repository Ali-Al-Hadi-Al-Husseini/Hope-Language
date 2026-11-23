package position

type CodeFile struct {
	Name string
	Text string
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
