package lexer

import (
	"reflect"
	"testing"
)

func TestLexer(t *testing.T) {
	tests := []struct {
		expresion string
		want      []string
	}{
		{"", []string{}},
	}

	for _, tt := range tests {
		t.Run(tt.expresion, func(t *testing.T) {
			got := lexer(tt.expresion)
			if !reflect.DeepEqual(got, tt.want) {
				t.Errorf("lexer(%q) = %v; want %w", tt.expresion, got, tt.want)
			}
		})
	}
}
