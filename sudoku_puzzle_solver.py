import math


def column_names(puzzle_string):
    puzzle_size = int(math.sqrt(len(puzzle_string)))
    # 65 is the ASCII number for a capital A
    return ''.join(chr(ord('A') + col_number) for col_number in range(puzzle_size))


def row_names(puzzle_string):
    puzzle_size = int(math.sqrt(len(puzzle_string)))
    return ''.join(str(row_number + 1) for row_number in range(puzzle_size))


def possible_values(puzzle_string):
    return row_names(puzzle_string)


def cross(cols, rows):
    # We want the addresses ordered by rows, meaning all the addresses in the first row
    # before going on to the second row. But, we use the column header first in the address.
    # This addressing mimics spreadsheets
    return [s + t for t in rows for s in cols]


def box_groupings(col_names, row_names):
    box_group_size = int(math.sqrt(len(col_names)))
    col_name_groups = [col_names[i:i + box_group_size] for i in range(0, len(col_names), box_group_size)]
    row_name_groups = [row_names[i:i + box_group_size] for i in range(0, len(row_names), box_group_size)]
    # groups = []
    # for col_name_group in col_name_groups:
    #     for row_name_group in row_name_groups:
    #         groups.append(cross(col_name_group, row_name_group))
    # return groups
    return [cross(col_name_group, row_name_group) for col_name_group in col_name_groups for row_name_group in row_name_groups]


def column_groupings(col_names, row_names):
    groups = []
    for col_name in col_names:
        col_group = []
        for row_name in row_names:
            col_group.append(col_name+row_name)
        groups.append(col_group)
    return groups


def row_groupings(col_names, row_names):
    groups = []
    for row_name in row_names:
        row_group = []
        for col_name in col_names:
            row_group.append(col_name+row_name)
        groups.append(row_group)
    return groups


def ordered_cell_addresses(puzzle_string):
    # addresses = []
    # for row in row_names(puzzle_string):
    #     for col in column_names(puzzle_string):
    #         addresses.append(col + row)
    # return addresses
    return cross(column_names(puzzle_string), row_names(puzzle_string))


def create_ordered_values_from_puzzle_string_2(puzzle_string):
    values = []
    for value in puzzle_string:
        if value != '.':
            values.append(value)
        else:
            values.append(possible_values(puzzle_string))
    return values


def create_ordered_values_from_puzzle_string(puzzle_string):
    return [(value if value != '.' else possible_values(puzzle_string)) for value in puzzle_string]


def create_puzzle(sudoku_puzzle_string):
    addresses = ordered_cell_addresses(sudoku_puzzle_string)
    values = create_ordered_values_from_puzzle_string(sudoku_puzzle_string)
    return dict(zip(addresses, values))


def display_puzzle_simple(puzzle, row_names, column_names):
    width = 1 + max(len(s) for s in puzzle.values())
    print('   ' + ''.join(col_name.center(width, ' ') for col_name in list(column_names)))
    for row_name in row_names:
        row_values = (puzzle[col_name + row_name].center(width) for col_name in column_names)
        print(row_name + ' |' + ''.join(row_values))


def display_puzzle(puzzle):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1 + max(len(s) for s in puzzle.values())
    horizontal_grid_line = '   ' + '+'.join(['-' * (width * 3)] * 3)

    # First print header
    # print('   ' + ''.join(colName.center(width, ' ') + ('|' if colName in col_bar_boundaries else '') for colName in list(cols)))
    # for colName in cols:
    #     print(colName.center(width))
    # print(horizontal_grid_line)

    for r in column_names:
        print(r + ' |' + ''.join(puzzle[r + c].center(width) for c in row_names))
        # print(r + ' |' + ''.join(puzzle[r+c].center(width)+('|' if c in col_bar_boundaries else '') for c in column_names))
        # if r in row_bar_boundaries: print(horizontal_grid_line)
    return
