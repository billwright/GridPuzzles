import math

# Use these for regular 9x9 sudoku
rows = 'ABCDEFGHI'
cols = '123456789'
row_bar_boundaries = 'CF'
col_bar_boundaries = '36'
row_box_groupings = ('ABC','DEF','GHI')
col_box_groupings = ('123','456','789')

# Use these for super 16x16 sudoku
# rows = 'abcdefghijklmnop'
# cols = '0123456789ABCDEF'
# row_bar_boundaries = 'dhl'
# col_bar_boundaries = '37B'
# row_box_groupings = ('abcd','efgh','ijkl', 'mnop')
# col_box_groupings = ('0123','4567','89AB','CDEF')

def cross(a, b):
    return [s + t for s in a for t in b]

big_square_size = int(math.sqrt(len(rows)))

boxes = cross(rows, cols)

# List of all the boxes in each row, so a list of lists: [['a1', 'a2', ...], ['b1', 'b2', ...], ...]
row_units = [cross(r, cols) for r in rows]

# List of all the boxes in each col, so a list of lists: [['a1', 'b1', ...], ['a2', 'b2', ...], ...]
column_units = [cross(rows, c) for c in cols]

square_units = [cross(rs, cs) for rs in row_box_groupings for cs in col_box_groupings]

# a "unit" is a collection of boxes that make up either a row, column, or square. This is all of those units, so
# its size is puzzle_size * 3
unit_list = row_units + column_units + square_units

# This is a dictionary, keyed by the box id (e.g. 'a1'), which returns the three units (lists) that box is contained in.
units = dict((s, [u for u in unit_list if s in u]) for s in boxes)

# This is a dictionary, keyed by the box id (e.g. 'a1'), which returns a list of that boxes peers. This list will have
# puzzle_size-1 row peers, puzzle_size-1 column peers, and puzzle_size-1 square peers (with some square peers being
# duplicates of the row and column peers.
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1 + max(len(values[s]) for s in boxes)
    horizontal_grid_line = '   ' + '+'.join(['-' * (width * big_square_size)] * big_square_size)

    # First print header
    print('   ' + ''.join(colName.center(width, ' ') + ('|' if colName in col_bar_boundaries else '') for colName in list(cols)))
    # for colName in cols:
    #     print(colName.center(width))
    print(horizontal_grid_line)

    for r in rows:
        print(r + ' |' + ''.join(values[r+c].center(width)+('|' if c in col_bar_boundaries else '') for c in cols))
        if r in row_bar_boundaries: print(horizontal_grid_line)
    return

print(square_units)
print(row_units)
print(column_units)

