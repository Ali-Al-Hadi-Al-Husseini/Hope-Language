from ..Tokenizer_tools.Position import Position

def string_with_arrows(text, start_pos: Position, end_pos: Position) -> str:

    result = ''

    # Calculate indices
    idx_start = max(text.rfind('\n', 0, start_pos.idx), 0)
    idx_end = text.find('\n', idx_start + 1)
    if idx_end < 0: idx_end = len(text)
    
    # Generate each line
    line_count = end_pos.line - start_pos.line + 1
    for i in range(line_count):
        # Calculate line columns
        line = text[idx_start:idx_end]
        col_start = start_pos.col if i == 0 else 0
        col_end = end_pos.col if i == line_count - 1 else len(line) - 1

        # Append to result
        result += line + '\n'
        result += ' ' * col_start + '^' * (col_end - col_start)

        # Re-calculate indices
        idx_start = idx_end
        idx_end = text.find('\n', idx_start + 1)
        if idx_end < 0: idx_end = len(text)

    return result.replace('\t', '')