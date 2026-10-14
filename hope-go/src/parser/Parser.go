package parser

import (
	"fmt"

	LangErr "github.com/Ali-Al-Hadi-Al-Husseini/Hope-Language/hope-go/src/langErr"
	"github.com/Ali-Al-Hadi-Al-Husseini/Hope-Language/hope-go/src/lexer"
)

type Parser struct {
	Tokens    []lexer.Token
	idx       int
	currToken lexer.Token
}

func (par *Parser) advance() lexer.Token {
	par.idx += 1
	if par.idx >= 0 && par.idx < len(par.Tokens) {
		par.currToken = par.Tokens[par.idx]
	}
	return par.currToken
}

func (par *Parser) RegisterAdvancement(res ParserResult) {
	res.RegisterAdvancement()
	par.advance()
}

func (par *Parser) reverse(amount int) lexer.Token {
	par.idx -= amount
	if par.idx >= 0 && par.idx < len(par.Tokens) {
		par.currToken = par.Tokens[par.idx]
	}
	return par.currToken
}

func (par *Parser) Parse() ParserResult {
	result := par.GetStatments()
	if result.Err != nil && par.currToken.Type != lexer.TOKEN_EOF {
		return *result.Failure(&LangErr.LangError{
			Name:     "InvalidSyntaxErorr",
			Details:  "Expected  '+', '-', '*' , '/'  or any other operation",
			StartPos: &par.currToken.Pos,
			EndPos:   &par.currToken.Pos,
		})
	}

	return result
}

func (par *Parser) GetStatments() ParserResult {
	res := ParserResult{}
	stmts := []Node{}
	startPos := par.currToken.Pos

	for par.currToken.Type == lexer.TOKEN_NEWLINE {
		par.RegisterAdvancement(res)
	}

	statement := res.Register(par.statement())
	if res.Err != nil {
		return res
	}
	stmts = append(stmts, statement)
	moreStatements := true

	for true {
		newLineCount := 0
		for par.currToken.Type == lexer.TOKEN_NEWLINE {
			par.RegisterAdvancement(res)
			newLineCount += 1
		}

		if newLineCount == 0 {
			moreStatements = false
		}

		if !moreStatements {
			break
		}
		statement = res.Register(par.statement())
		if statement == nil {
			par.reverse(res.reverseCount)
			moreStatements = false
			continue
		}
		stmts = append(stmts, statement)
	}
	return *res.Succses(&ListNode{
		Elements: stmts,
		BaseNode: BaseNode{
			StartPos: &startPos,
			EndPos:   &par.currToken.Pos,
		},
	})

}

func (par *Parser) statement() ParserResult {
	res := ParserResult{}
	startPos := par.currToken.Pos

	if par.currToken.Matches(lexer.TOKEN_KEYWORD, "return") {
		par.RegisterAdvancement(res)
		expr, err := res.TryRegister(par.Expression())
		if err != nil {
			par.reverse(res.reverseCount)
		}
		return *res.Succses(&ReturnNode{
			node:     expr,
			BaseNode: BaseNode{StartPos: &startPos, EndPos: &par.currToken.EndPos},
		})
	}
	if par.currToken.Matches(lexer.TOKEN_KEYWORD, "continue") {
		par.RegisterAdvancement(res)

		return *res.Succses(&ContinueNode{
			BaseNode: BaseNode{StartPos: &startPos, EndPos: &par.currToken.EndPos},
		})
	}
	if par.currToken.Matches(lexer.TOKEN_KEYWORD, "break") {
		par.RegisterAdvancement(res)

		return *res.Succses(&BreakNode{
			BaseNode: BaseNode{StartPos: &startPos, EndPos: &par.currToken.EndPos},
		})
	}

	expr := res.Register(par.Expression())
	if res.Err != nil {
		return *res.Failure(&LangErr.LangError{
			Name:     "InvalidSyntaxErorr",
			Details:  "Expected 'let', int, float, identifier, keyword,  '+', '-' or '(' ",
			StartPos: &par.currToken.Pos,
			EndPos:   &par.currToken.Pos,
		})
	}
	return *res.Succses(expr)
}

func (par *Parser) Expression() ParserResult {
	res := ParserResult{}

	for par.currToken.Type == lexer.TOKEN_NEWLINE {
		par.RegisterAdvancement(res)
	}

	if par.currToken.Matches(lexer.TOKEN_IDENTIFIER, "let") {
		par.RegisterAdvancement(res)

		if par.currToken.Type != lexer.TOKEN_IDENTIFIER {
			return *res.Failure(&LangErr.LangError{
				Name:    "InvalidSyntaxErorr",
				Details: fmt.Sprintf("Expected identifier found %s '%s'", par.currToken.Type, par.currToken.Value),
			})
		}

		varName := par.currToken
		par.RegisterAdvancement(res)

		if par.currToken.Type != lexer.TOKEN_EQ {
			return *res.Failure(&LangErr.LangError{
				Name:     "InvalidSyntaxErorr",
				Details:  fmt.Sprintf("Expected '=' found %s '%s'", par.currToken.Type, par.currToken.Value),
				StartPos: &par.currToken.Pos,
				EndPos:   &par.currToken.EndPos,
			})
		}

		par.RegisterAdvancement(res)
		expr := res.Register(par.Expression())

		if res.Err != nil {
			return res
		}
		return *res.Succses(&VarAssignNode{
			NameToken: varName,
			ValueNode: expr,
		})
	}
	node := res.Register(par.BinOperation(par.ComparisonExpression, []string{"and", "or"}))
	if res.Err != nil {
		return *res.Failure(&LangErr.LangError{
			Name:     "InvalidSyntaxErorr",
			Details:  "Expected 'let', int, float, identifier, '+', '-' or '(' ",
			StartPos: &par.currToken.Pos,
			EndPos:   &par.currToken.EndPos,
		})
	}
	return *res.Succses(node)
}

func (par *Parser) BinOperation(operationFunc func() ParserResult, operations []string) ParserResult {
	res := ParserResult{}
	left := res.Register(operationFunc())
	if res.Err != nil {
		return res
	}
	for {
		matched := false

		for _, op := range operations {
			if par.currToken.Type == "KEYWORD" {
				if par.currToken.Value == op {
					matched = true
					break
				}

			} else if par.currToken.Type == op {
				matched = true
				break
			}
		}
		if !matched {
			break
		}
		opToken := par.currToken
		res.RegisterAdvancement()
		right := res.Register(operationFunc())

		left = &BinOpertaionNode{
			LeftNode:  left,
			RightNode: right,
			Operation: opToken,
		}
	}

	return *res.Succses(left)
}

func (par *Parser) ComparisonExpression() ParserResult {
	res := ParserResult{}

	if par.currToken.Matches(lexer.TOKEN_KEYWORD, "not") {
		opToken := par.currToken
		par.RegisterAdvancement(res)
		node := res.Register((par.ComparisonExpression()))
		if res.Err != nil {
			return res
		}
		return *res.Succses(&UnaryOperationNode{
			OpToken: opToken,
			Node:    node,
		})

	}
	node := res.Register(par.BinOperation(par.ArithmeticExpression, []string{lexer.TOKEN_EE, lexer.TOKEN_NE, lexer.TOKEN_LT, lexer.TOKEN_GT, lexer.TOKEN_GTE, lexer.TOKEN_LTE}))
	if res.Err != nil {
		return *res.Failure(&LangErr.LangError{
			Name:     "InvalidSyntaxErorr",
			Details:  "Expected int, float, identifier, keyword, function call, '+', '-' , '(' , '[' or 'not' ",
			StartPos: &par.currToken.Pos,
			EndPos:   &par.currToken.EndPos,
		})
	}
	return *res.Succses(node)
}

func (par *Parser) ArithmeticExpression() ParserResult {
	return par.BinOperation(par.Term, []string{lexer.TOKEN_PLUS, lexer.TOKEN_MINUS})
}
func (par *Parser) Factor() ParserResult {
	res := ParserResult{}
	token := par.currToken

	if par.currToken.Type == lexer.TOKEN_PLUS || par.currToken.Type == lexer.TOKEN_MINUS {
		par.RegisterAdvancement(res)
		factor := res.Register(par.Factor())
		if res.Err != nil {
			return res
		}
		return *res.Succses(
			&UnaryOperationNode{
				OpToken: token,
				Node:    factor,
			})
	}

	return par.Power()
}

func (par *Parser) Term() ParserResult {
	return par.BinOperation(par.Factor, []string{lexer.TOKEN_MUL, lexer.TOKEN_DIV, lexer.TOKEN_MODULE})

}
func (par *Parser) Power() ParserResult {
	res := ParserResult{}
	left := res.Register(par.Call())
	if res.Err != nil {
		return res
	}

	if par.currToken.Type == lexer.TOKEN_POW {

		opToken := par.currToken
		res.RegisterAdvancement()
		right := res.Register(par.Factor())

		left = &BinOpertaionNode{
			LeftNode:  left,
			RightNode: right,
			Operation: opToken,
		}
	}

	return *res.Succses(left)
}

// atom
func (par *Parser) Most() ParserResult {
	res := ParserResult{}
	token := par.currToken

	switch token.Type {
	case lexer.TOKEN_FLOAT, lexer.TOKEN_INT:
		par.RegisterAdvancement(res)
		return *res.Succses(&NumberNode{BaseNode: BaseNode{
			Token: &token},
		})

	case lexer.TOKEN_STRING:
		par.RegisterAdvancement(res)
		return *res.Succses(&StringNode{
			BaseNode: BaseNode{Token: &token}})

	case lexer.TOKEN_LSQUARE:
		expr := res.Register(par.ListExpression())
		if res.Err != nil {
			return res
		}
		return *res.Succses(expr)

	case lexer.TOKEN_LPAREN:
		par.RegisterAdvancement(res)
		expr := res.Register(par.Expression())
		if res.Err != nil {
			return res
		}

		if par.currToken.Type == lexer.TOKEN_RPARENT {
			par.RegisterAdvancement(res)
			return *res.Succses(expr)
		} else {
			return *res.Failure(&LangErr.LangError{
				Name:     "InvalidSyntaxErorr",
				Details:  "Expected ')' ",
				StartPos: &par.currToken.Pos,
				EndPos:   &par.currToken.EndPos,
			})
		}

	case lexer.TOKEN_IDENTIFIER:

	default:
		switch {
		case token.Matches(lexer.TOKEN_KEYWORD, "if"):
			expr := res.Register(par.IfExpression())
			if res.Err != nil {
				return res
			}
			return *res.Succses(expr)

		case token.Matches(lexer.TOKEN_KEYWORD, "while"):
			expr := res.Register(par.WhileExpression())
			if res.Err != nil {
				return res
			}
			return *res.Succses(expr)
		case token.Matches(lexer.TOKEN_KEYWORD, "for"):
			expr := res.Register(par.ForExpression())
			if res.Err != nil {
				return res
			}
			return *res.Succses(expr)
		case token.Matches(lexer.TOKEN_KEYWORD, "func"):
			expr := res.Register(par.FuncExpression())
			if res.Err != nil {
				return res
			}
			return *res.Succses(expr)

		}

	}
	return *res.Failure(&LangErr.LangError{
		Name:     "InvalidSyntaxErorr",
		Details:  "Expected int, float, identifier, '+', '-' , '('  or '[' ",
		StartPos: &token.Pos,
		EndPos:   &token.EndPos,
	})
}
func (par *Parser) Call() ParserResult {
	res := ParserResult{}
	most := res.Register(par.Most())
	if res.Err != nil {
		return res
	}

	if par.currToken.Type == lexer.TOKEN_LPAREN {
		par.RegisterAdvancement(res)
		var arguments []Node

		if par.currToken.Type == lexer.TOKEN_RPARENT {
			par.RegisterAdvancement(res)
		} else {
			arguments = append(arguments, res.Register(par.Expression()))
			if res.Err != nil {
				return res
			}

			for par.currToken.Type == lexer.TOKEN_COMMA {
				par.RegisterAdvancement(res)
				arguments = append(arguments, res.Register(par.Expression()))
				if res.Err != nil {
					return res
				}

			}
			if par.currToken.Type != lexer.TOKEN_RPARENT {
				return *res.Failure(&LangErr.LangError{
					Name:     "InvalidSyntaxErorr",
					Details:  "Expected ',' or ')'",
					StartPos: &par.currToken.Pos,
					EndPos:   &par.currToken.Pos,
				})
			}
			return *res.Succses(&CallNode{
				NodeToCall: most,
				ArgNodes:   arguments,
			})

		}
	}

	return *res.Succses(most)
}

func (par *Parser) IfElifMaker() ParserResult
func (par *Parser) IfExpression() ParserResult
func (par *Parser) ElseExpression() ParserResult
func (par *Parser) ElifElseExpression() ParserResult
func (par *Parser) ListCallExpression() ParserResult
func (par *Parser) ForExpression() ParserResult
func (par *Parser) WhileExpression() ParserResult
func (par *Parser) FuncExpression() ParserResult
func (par *Parser) ListExpression() ParserResult
