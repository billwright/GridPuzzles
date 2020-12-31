# small ken-ken

rows = ''
cols = ''


def generate_rows(puzzleSize):
    rows = ''
    for x in range(1, puzzleSize+1):
        rows = rows + (chr(64 + x))
    return rows


def generate_cols(puzzleSize):
    cols = ''
    for x in range(1, puzzleSize+1):
        cols = cols + str(x)

    return cols


def cross(rows, cols):
    return [row + col for row in rows for col in cols]


unit_list = []
units = []
peers = []
boxes = []


def initialize(puzzleSize):
    global rows
    global cols

    rows = generate_rows(puzzleSize)
    cols = generate_cols(puzzleSize)

    global boxes
    boxes = cross(rows, cols)

    row_units = [cross(r, cols) for r in rows]
    column_units = [cross(rows, c) for c in cols]

    global unit_list
    unit_list = row_units + column_units

    global units
    units = dict((s, [u for u in unit_list if s in u]) for s in boxes)
    global peers
    peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


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


def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    print('-----------------')
    width = 1 + max(len(values[s]) for s in boxes)
    for r in rows:
        print(''.join(values[r + c].center(width)
                      for c in cols))
    print('-----------------')
    return


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
    assert len(grid) == input_grid_length, "Input grid must be a string of length " + str(
        input_grid_length) + "(" + str(len(cols)) + "x" + str(len(rows))
    return dict(zip(boxes, [(s if s != '.' else cols) for s in grid]))


def handle_blank(values, value, cell):
    values[cell] = str(value)


def calculate_options(calc_tuple, choices):
    operation = calc_tuple[0]
    if operation not in "+-/x":
        print("Invalid puzzle because of invalid operation: " + operation)
        return None


        # The operator is one of: plus, minus, division, multiplication
        # The choices is a list of lists. One choice from each sublist must
        # be used to form the result. For example, if we call this function
        # with these values:
        #
        #   calculate_operands('+', ['1234', '1234'], 7)
        #
        # Then we return a list of the choices in each position which satisfy
        # this constrain. In this case the answer would be:
        #
        #   ['34', '34']
        #
        # Another example is:
        #
        #   calculate_operands('+', ['1234', '1234', '1234'], 9)
        #
        # return value:
        #
        #   ['1234', '1234', '1234']
        #
        # Another example is:
        #
        #   calculate_operands('*', ['123456', '123456', '123456'], 60)
        #
        # return value:
        #
        #   ['234', '234', '234']
        #
        # Another example is:
        #
        #   calculate_operands('+', ['123456', '123456'], 3)
        #
        # return value:
        #
        #   ['12', '12']


def calculate_operands_top(operator, choices, result):
    solutions = []
    calculate_operands(operator, choices, result, '', solutions)
    # print(solutions)

    # Refine solution strings into reduced set of choices
    reduced_choices = [[] for i in choices]
    for solution in solutions:
        split_options = [solution[i] for i in range(0, len(solution), 2)]
        for i, option in enumerate(split_options):
            reduced_choices[i].append(option)

    # print("reduced choices is", reduced_choices)
    reduced_choices = [set(i) for i in [sorted(j) for j in reduced_choices]]
    # print("reduced choices is", reduced_choices)
    reduced_choices = [''.join(sorted(i)) for i in reduced_choices]
    # print("reduced choices is", reduced_choices)
    return reduced_choices


def calculate_operands(operator, choices, result, value_string, solutions):
    # print("calling calculate_operands with these args", operator, choices, result, value_string, solutions)
    num_operands = len(choices)
    if num_operands == 0:
        value = eval(value_string)
        if value == result or (value < 0 and -value == result) or (
                (value > 0) and (value < 1) and (1.0 / value == result)):
            # print("Adding solution to list:", value_string)
            solutions.append(value_string)
        return

    else:
        for first_operand in choices[0]:
            if len(value_string) == 0:
                new_value_string = first_operand
            else:
                new_value_string = value_string + operator + first_operand
            calculate_operands(operator, choices[1:], result, new_value_string, solutions)


def eliminate_pairs(values):
    for row in rows:
        pairs = [[row+c1, row+c2] for c1 in cols for c2 in cols if c1 != c2]
        for pair in pairs:
            if values[pair[0]] == values[pair[1]] and len(values[pair[0]]) == 2:
                for peer in cell_row_peers(pair[0], peers):
                    if peer != pair[1]:
                        # print("Removing pairs from row peer", peer)
                        for curr_digit in values[pair[0]]:
                            values[peer] = values[peer].replace(curr_digit, '')
    for col in cols:
        pairs = [[r1+col, r2+col] for r1 in rows for r2 in rows if r1 != r2]
        for pair in pairs:
            if values[pair[0]] == values[pair[1]] and len(values[pair[0]]) == 2:
                for peer in cell_col_peers(pair[0], peers):
                    if peer != pair[1]:
                        # print("Removing pairs from row peer", peer)
                        for curr_digit in values[pair[0]]:
                            values[peer] = values[peer].replace(curr_digit, '')


def eliminate_singles(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: KenKen in dictionary form.
    Returns:
        Resulting KenKen in dictionary form after eliminating values.
    """
    for box, possibleValues in values.items():
        if len(possibleValues) == 1:
            for peer in peers[box]:
                values[peer] = values[peer].replace(possibleValues, "")


def eliminate(values):
    eliminate_singles(values)
    eliminate_pairs(values)

    return values


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


def solve_puzzle(values, calc_units):
    stalled = False
    times_through_loop = 0
    current_possibilities = total_possibilities(values)
    print("Total possibilities is ", total_possibilities(values))
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = num_boxes_solved(values)
        print("Squares solved before:", solved_values_before)
        print("This is our", times_through_loop, "time through the loop")

        for calc_unit in calc_units:
            starting_choices = [values[i] for i in calc_unit[2]]
            reduced_choices = calculate_operands_top(calc_unit[0], starting_choices, calc_unit[1])
            for reduced_choice, box in zip(reduced_choices, calc_unit[2]):
                values[box] = reduced_choice
            # print("After getting operands for calc unit ", calc_unit)
            # display(values)

        values = eliminate(values)
        # print("After eliminating taken choices:")
        # display(values)

        if solved(values):
            return values

        values = only_choice(values)
        # display(values)
        if solved(values):
            return values

        # Check how many boxes have a determined value, to compare
        # solved_values_after = num_boxes_solved(values)
        # print("Squares solved after:", solved_values_after)

        times_through_loop = times_through_loop + 1
        # print("Done with loop #", times_through_loop)

        # If no new values were added, stop the loop.
        updated_possibilities = total_possibilities(values)
        if updated_possibilities == current_possibilities:
            stalled = True
        else:
            current_possibilities = updated_possibilities
            print("We made progress. Now there are this many possibilities: ", current_possibilities)

        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    print("Did", times_through_loop, " iterations through the solver loop")
    return values


def top_search(calc_units, values):
    return search(calc_units, values, 0, 0)


def search(calc_units, values, guesses, backups):
    "Using depth-first search and propagation, create a search tree and solve the puzzle."
    print("Called with guesses=", guesses, "and backups=", backups)

    # First, reduce the puzzle using the previous function
    values = solve_puzzle(values, calc_units)

    if values is False:
        print("Found invalid state, backing up")
        return False, guesses, backups + 1  # Failed earlier

    if solved(values):
        print("Puzzle solved! I had to guess", guesses, "times and I backed up", backups, "times")
        return values, guesses, backups

    # Choose one of the unfilled squares with the fewest possibilities
    smallest_box = get_smallest_box_greater_than_one(values)

    # Use recursion to solve each one of the resulting puzzle. If one returns a value (not False), return that answer!
    for value in values[smallest_box]:
        new_values = values.copy()
        new_values[smallest_box] = value
        print("Selected value", value, "in box", smallest_box, "out of choices", values[smallest_box])
        display(new_values)
        updated_values, guesses, backups = search(calc_units, new_values, guesses + 1, backups)
        if updated_values:
            return updated_values, guesses, backups
        else:
            print("Could not find a solution from this state:")
            display(new_values)
            print("Backing up...")

    return False, guesses, backups


def num_boxes_solved(values):
    return len([box for box in values.keys() if len(values[box]) == 1])


def total_possibilities(values):
    possibilities = ''
    for box, box_possibilities in values.items():
        possibilities += box_possibilities
    return len(possibilities)


def solved(values):
    "Returns True if the puzzle is solved and False otherwise"
    return num_boxes_solved(values) is len(rows)*len(cols)


def get_smallest_box_greater_than_one(values):
    # This is used to find the box where we'll make a guess
    smallest_box_size, smallest_box = min((len(values[box]), box) for box in values.keys() if len(values[box]) > 1)
    return smallest_box


# calculate_operands_top('-', ['1234', '1234'], 3)
# calculate_operands_top('/', ['1234', '1234'], 2)
# calculate_operands_top('*', ['1234', '1234', '1234'], 24)
# calculate_operands_top('*', ['1234', '124', '1234'], 24)
# calculate_operands_top('+', ['1234', '1234', '1234'], 6)
# calculate_operands_top('+', ['1234', '1234', '1234'], 11)
# calculate_operands_top('+', ['1234', '1234', '1234', '1234'], 11)
# calculate_operands_top('', ['1234'], 3)

# calculate_operands_top('+', ['123456', '123456'], 3)
# calculate_operands_top('-', ['123456', '123456'], 1)
# calculate_operands_top('+', ['123456', '123456'], 11)
# calculate_operands_top('+', ['123456', '123456'], 5)
# calculate_operands_top('*', ['123456', '123456', '123456'], 60)
# calculate_operands_top('/', ['123456', '123456'], 2)
# calculate_operands_top('*', ['123456', '123456', '123456'], 24)
# calculate_operands_top('*', ['123456', '123456', '123456'], 10)
# calculate_operands_top('*', ['123456', '123456'], 10)

# calc_units = [
#     ('*', 24, ['A1', 'A2', 'B1']),
#     ('/', 2, ['A3', 'A4']),
#     ('-', 2, ['B2', 'C2']),
#     ('', 1, ['B3']),
#     ('+', 9, ['B4', 'C3', 'C4']),
#     ('', 4, ['C1']),
#     ('+', 3, ['D1', 'D2']),
#     ('-', 1, ['D3', 'D4']),
# ]

calc_units4 = [
    ('*', 24, ['A1', 'A2', 'B1']),
    ('', 3, ['A3']),
    ('-', 3, ['A4', 'B4']),
    ('/', 2, ['B2', 'B3']),
    ('+', 6, ['C1', 'C2', 'D1']),
    ('+', 11, ['C3', 'C4', 'D3', 'D4']),
    ('', 3, ['D2']),
]

calc_units6 = [
    ('-', 1, ['A1', 'A2']),
    ('', 2, ['A3']),
    ('+', 11, ['A4', 'A5']),
    ('+', 5, ['A6', 'B6']),
    ('*', 60, ['B1', 'C1', 'C2']),
    ('', 1, ['B2']),
    ('/', 2, ['B3', 'B4']),
    ('*', 24, ['B5', 'C5', 'C6']),
    ('-', 1, ['C3', 'D3']),
    ('+', 3, ['C4', 'D4']),
    ('+', 14, ['D1', 'D2', 'E2']),
    ('*', 10, ['D5', 'D6', 'E6']),
    ('-', 3, ['E1', 'F1']),
    ('+', 7, ['E3', 'E4']),
    ('', 6, ['E5']),
    ('/', 2, ['F2', 'F3']),
    ('', 5, ['F4']),
    ('/', 2, ['F5', 'F6']),
]

calc_units8 = [
    ('-', 2, ['A1', 'B1']),
    ('+', 17, ['A2', 'A3', 'B3']),
    ('-', 7, ['A4', 'A5']),
    ('*', 40, ['A6', 'A7', 'A8']),
    ('+', 16, ['B2', 'C2', 'C3']),
    ('', 6, ['B4']),
    ('*', 180, ['B5', 'C4', 'C5', 'C6']),
    ('+', 16, ['B6', 'B7', 'C7']),
    ('*', 10, ['B8', 'C8']),
    ('*', 24, ['C1', 'D1', 'D2']),
    ('+', 11, ['D3', 'D4', 'D5']),
    ('+', 13, ['D6', 'D7']),
    ('/', 3, ['D8', 'E8']),
    ('+', 14, ['E1', 'E2', 'F1']),
    ('+', 21, ['E3', 'E4', 'E5']),
    ('/', 4, ['E6', 'E7']),
    ('*', 40, ['F2', 'F3', 'G2']),
    ('+', 6, ['F4', 'F5', 'F6']),
    ('+', 13, ['F7', 'G6', 'G7']),
    ('-', 2, ['F8', 'G8']),
    ('-', 2, ['G1', 'H1']),
    ('+', 7, ['G3', 'H2', 'H3']),
    ('+', 11, ['G4', 'G5']),
    ('*', 30, ['H4', 'H5']),
    ('+', 17, ['H6', 'H7', 'H8'])
]


def solve():
    initialize(8)

    grid1 = '.' * len(rows) * len(cols)

    test1 = grid_values(grid1)

    display(test1)

    # test1 = solve_puzzle(test1, calc_units8)
    test1, guesses, backups = top_search(calc_units8, test1)

    display(test1)

solve()