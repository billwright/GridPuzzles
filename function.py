from utils import *


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
    assert len(grid) == input_grid_length, "Input grid must be a string of length " + str(input_grid_length) + "(" + str(len(cols)) + "x" + str(len(rows)) + ")"
    return dict(zip(boxes, [(s if s != '.' else cols) for s in grid]))


def eliminate(values):
    eliminate_singles(values)
    eliminate_pairs(values)
    eliminate_triples(values)

    return values


def eliminate_singles(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    for box, possibleValues in values.items():
        if len(possibleValues) == 1:
            for peer in peers[box]:
                values[peer] = values[peer].replace(possibleValues, "")
    return values


def eliminate_pairs(values):
    for unit in unit_list:
        pairs = [[box1, box2] for box1 in unit for box2 in unit if box1 != box2]
        for pair in pairs:
            if values[pair[0]] == values[pair[1]] and len(values[pair[0]]) == 2:
                for peer in unit:
                    if peer != pair[0] and peer != pair[1]:
                        print("Found pair: " + str(pair) + ", in unit: " + str(unit))
                        for curr_digit in values[pair[0]]:
                            values[peer] = values[peer].replace(curr_digit, '')

def eliminate_triples(values):
    for unit in unit_list:
        triples = [[box1, box2, box3] for box1 in unit for box2 in unit for box3 in unit if (box1 != box2) and (box1 != box3) and (box2 != box3)]
        for triple in triples:
            if values[triple[0]] == values[triple[1]] and (values[triple[0]] == values[triple[2]]) and (values[pair[0]]) == 3:
                for peer in unit:
                    if peer != triple[0] and peer != triple[1] and peer != triple[2]:
                        print("Found triple: " + str(triple) + ", in unit: " + str(unit))
                        for curr_digit in values[triple[0]]:
                            values[peer] = values[peer].replace(curr_digit, '')

def cell_row_peers(cell, peers):
    r_peers = []
    for peer in peers[cell]:
        if peer[0] == cell[0] and peer[1] != cell[1]:
            r_peers.append(peer)
    return r_peers


def cell_col_peers(cell, peers):
    c_peers = []
    for peer in peers[cell]:
        if peer[1] == cell[1] and peer[0] != cell[0]:
            c_peers.append(peer)
    return c_peers


def big_square_peers(cell, peers):
    return peers


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unit_list:
        for digit in cols:
            dBoxes = [box for box in unit if digit in values[box]]
            if len(dBoxes) == 1:
                values[dBoxes[0]] = digit
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = num_boxes_solved(values)
        print("Squares solved before:", solved_values_before)

        # values = eliminate(values)
        if solved(values):
            return values

        values = only_choice(values)
        if solved(values):
            return values

        # Check how many boxes have a determined value, to compare
        solved_values_after = num_boxes_solved(values)
        print("Squares solved after:", solved_values_after)

        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after

        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def top_search(values):
    return search(values, 0, 0)


def search(values, guesses, backups):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    print("Called with guesses=", guesses, "and backups=", backups)

    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    if values is False:
        print("Found invalid state, backing up")
        return False, guesses, backups + 1    # Failed earlier

    if solved(values):
        print("Puzzle solved! I had to guess", guesses, "times and I backed up", backups, "times")
        return values, guesses, backups

    # Choose one of the unfilled squares with the fewest possibilities
    smallest_box = get_smallest_box_greater_than_one(values)

    # Use recursion to solve each one of the resulting sudokus. If one returns a value (not False), return that answer!
    for value in values[smallest_box]:
        new_values = values.copy()
        new_values[smallest_box] = value
        print("Selected value", value, "in box", smallest_box, "out of choices", values[smallest_box])
        display(new_values)
        new_values, guesses, backups = search(new_values, guesses+1, backups)
        if new_values:
            return new_values, guesses, backups

    print("Could not find a solution...")
    return False, guesses, backups


def num_boxes_solved(values):
    return len([box for box in values.keys() if len(values[box]) == 1])


def solved(values):
    "Returns True if the puzzle is solved and False otherwise. For 9x9 puzzle, checks that # of squares solves is 81"
    return num_boxes_solved(values) is len(rows) * len(cols)


def get_smallest_box_greater_than_one(values):
    # This is used to find the box where we'll make a guess
    smallest_box_size, smallest_box = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)
    return smallest_box

def create_puzzle(grid):
    grid_values(grid)

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
    print("Input puzzle is of length " + str(len(grid)))
    assert len(grid) == input_grid_length, "Input grid must be a string of length " + str(input_grid_length) + " (" + str(len(cols)) + "x" + str(len(rows)) + ")"
    return dict(zip(boxes, [(s if s != '.' else cols) for s in grid]))


sudoku_1 = '4...6.8..' + \
           '.754.8...' + \
           '.8..92...' + \
           '5.23..4..' + \
           '..79452..' + \
           '..4..75.3' + \
           '...87..3.' + \
           '...6.394.' + \
           '..3.2...8'

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

nov30 = '8...3..47' + \
        '.6.8...3.' + \
        '...9.5...' + \
        '.2...6.9.' + \
        '1.4...7.6' + \
        '.5.....1.' + \
        '...4.3...' + \
        '.....2.8.' + \
        '3...7...9'

# game_board = grid_values(monster_sudoku)
# game_board = grid_values(sudoku_1)
# game_board = grid_values(nov30)
#
# display(game_board)
#
# final_board, guesses, backups = top_search(game_board)
#
# display(final_board)