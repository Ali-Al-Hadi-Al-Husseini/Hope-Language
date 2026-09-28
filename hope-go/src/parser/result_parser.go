package parser

type ParserResult struct {
	Err              error
	node             Node
	lastAdvanceCount int
	advanceCount     int
	reverseCount     int
}

func (res *ParserResult) RegisterAdvancement() {
	res.lastAdvanceCount += 1
	res.advanceCount += 1
}

func (res *ParserResult) Register(newResult ParserResult) Node {
	res.lastAdvanceCount = newResult.advanceCount
	res.advanceCount += newResult.advanceCount

	if newResult.Err != nil {
		res.Err = newResult.Err
	}
	return newResult.node
}

func (res *ParserResult) Succses(node Node) *ParserResult {
	res.node = node
	return res
}

func (res *ParserResult) Failure(err error) *ParserResult {
	if res.Err == nil || res.lastAdvanceCount == 0 {
		res.Err = err
	}
	return res
}
