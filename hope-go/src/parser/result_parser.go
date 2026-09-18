package parser

type ParserResult struct {
	Err              error
	lastAdvanceCount int
	advanceCount     int
	reverseCount     int
}

func (res *ParserResult) RegisterAdvancement() {
	res.lastAdvanceCount += 1
	res.advanceCount += 1
}
