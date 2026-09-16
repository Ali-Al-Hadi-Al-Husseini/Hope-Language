package errors

import (
	"strings"

	lexer "github.com/Ali-Al-Hadi-Al-Husseini/Hope-Language/hope-go/src/lexer"
)

func StringWithArrows(text string, startPos lexer.Position, endPos lexer.Position) string {
	var result strings.Builder

	// Calculate indices
	idxStart := lastIndexBefore(text, "\n", startPos.Idx)
	if idxStart < 0 {
		idxStart = 0
	}
	idxEnd := indexFrom(text, "\n", idxStart+1)
	if idxEnd < 0 {
		idxEnd = len(text)
	}

	// Generate each line
	lineCount := endPos.Line - startPos.Line + 1
	for i := 0; i < lineCount; i++ {
		// Calculate line columns
		line := text[idxStart:idxEnd]

		colStart := 0
		if i == 0 {
			colStart = startPos.Col
		}

		colEnd := len(line) - 1
		if i == lineCount-1 {
			colEnd = endPos.Col
		}

		// Append to result
		result.WriteString(line)
		result.WriteString("\n")
		result.WriteString(strings.Repeat(" ", clampNonNegative(colStart)))
		result.WriteString(strings.Repeat("^", clampNonNegative(colEnd-colStart)))

		// Re-calculate indices
		idxStart = idxEnd
		idxEnd = indexFrom(text, "\n", idxStart+1)
		if idxEnd < 0 {
			idxEnd = len(text)
		}
	}

	return strings.ReplaceAll(result.String(), "\t", "")
}

func lastIndexBefore(text, sep string, before int) int {
	if before < 0 {
		before = 0
	}
	if before > len(text) {
		before = len(text)
	}
	return strings.LastIndex(text[:before], sep)
}

func indexFrom(text, sep string, start int) int {
	if start < 0 {
		start = 0
	}
	if start > len(text) {
		return -1
	}
	i := strings.Index(text[start:], sep)
	if i < 0 {
		return -1
	}
	return i + start
}

func clampNonNegative(n int) int {
	if n < 0 {
		return 0
	}
	return n
}
