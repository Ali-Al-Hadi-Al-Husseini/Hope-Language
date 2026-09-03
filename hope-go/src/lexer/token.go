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
}
