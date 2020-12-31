def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '.' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
    """
    input_grid_length = len(cols) * len(rows)
    assert len(grid) == input_grid_length, "Input grid must be a string of length " + str(input_grid_length) + "(" + str(len(cols)) + "x" + str(len(rows))
    return dict(zip(boxes, [(s if s != '.' else cols) for s in grid]))


sudoku_1 = '' + \
           '' + \
           '' + \
           '' + \
           '' + \
           '' + \
           '' + \
           '' + \
           ''

monster_sudoku = '261.D9.A.....7..' + \
                 '5...F...0E......' + \
                 '.B.7C6...D...0.9' + \
                 'CDE.3..B5F......' + \
                 '6....D.4C3E.8..A' + \
                 '....B0...6...F23' + \
                 '.FD...A9..0....E' + \
                 '9..C...E4..B.1..' + \
                 '..4.1..6B...A..7' + \
                 '7....F..24...95.' + \
                 'BA2...9...1E....' + \
                 'E..9.C70A.3....4' + \
                 '......2D7..F.E8B' + \
                 'D.6...5...839.C.' + \
                 '......3C...0...2' + \
                 '..A.....6.C4.370'
