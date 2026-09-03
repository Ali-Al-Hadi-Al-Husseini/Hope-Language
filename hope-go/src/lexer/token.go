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
