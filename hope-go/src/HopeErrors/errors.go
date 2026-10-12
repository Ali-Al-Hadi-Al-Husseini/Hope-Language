package errors

import (
	"fmt"

	lexer "github.com/Ali-Al-Hadi-Al-Husseini/Hope-Language/hope-go/src/lexer"
)

type LangError struct {
	Name     string
	Details  string
	StartPos *lexer.Position
	EndPos   *lexer.Position
}

func (err *LangError) Error() string {
	arrows_string := StringWithArrows(err.StartPos.File.Text, *err.StartPos, *err.EndPos)
	result := fmt.Sprintf("%s: %q \n File %s, line %d \n\n%q", err.Name, err.Details, err.StartPos.File.Name, err.StartPos.Line+1, arrows_string)
	return result
}
