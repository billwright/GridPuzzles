import math


def cross(cols, rows):
    # We want the addresses ordered by rows, meaning all the addresses in the first row
    # before going on to the second row. But, we use the column header first in the address.
    # This addressing mimics spreadsheets
    return [c + r for r in rows for c in cols]


class Sudoku_Puzzle(object):

    def __init__(self, puzzle_string):
        puzzle_square_root = math.sqrt(len(puzzle_string))
        if puzzle_square_root != int(puzzle_square_root):
            error_string = f'ERROR: Puzzle string was of length {len(puzzle_string)}, which is not a perfect square'
            print(error_string)
            raise ValueError(error_string)

        self.size = int(math.sqrt(len(puzzle_string)))
        self.box_group_size = int(math.sqrt(self.size))
        self.column_boundaries = ''.join([chr(ord('A') + i * self.box_group_size - 1) for i in range(1, self.box_group_size+1)])
        self.row_boundaries = ''.join([str(i * self.box_group_size) for i in range(1, self.box_group_size+1)])
        self.column_names = ''.join(chr(ord('A') + col_number) for col_number in range(self.size))
        self.row_names = ''.join(str(row_number + 1) for row_number in range(self.size))

        self.puzzle_dict = self.create_puzzle(puzzle_string)

    def possible_values(self):
        return self.row_names

    def box_groupings(self):
        col_name_groups = [self.column_names[i:i + self.box_group_size] for i in range(0, self.size, self.box_group_size)]
        row_name_groups = [self.row_names[i:i + self.box_group_size] for i in range(0, self.size, self.box_group_size)]
        # groups = []
        # for col_name_group in col_name_groups:
        #     for row_name_group in row_name_groups:
        #         groups.append(cross(col_name_group, row_name_group))
        # return groups
        return [cross(col_name_group, row_name_group) for col_name_group in col_name_groups
                for row_name_group in row_name_groups]

    def column_groupings(self):
        groups = []
        for col_name in self.column_names:
            col_group = []
            for row_name in self.row_names:
                col_group.append(col_name+row_name)
            groups.append(col_group)
        return groups

    def row_groupings(self):
        groups = []
        for row_name in self.row_names:
            row_group = []
            for col_name in self.col_names:
                row_group.append(col_name+row_name)
            groups.append(row_group)
        return groups

    def create_puzzle(self, puzzle_string):
        addresses = cross(self.column_names, self.row_names)
        values = [(value if value != '.' else self.possible_values()) for value in puzzle_string]

        return dict(zip(addresses, values))

    def get_cell_value(self, cell_address):
        return self.puzzle_dict[cell_address]

    def display(self):
        max_cell_width = 1 + max(len(s) for s in self.puzzle_dict.values())

        # horizontal_grid_line = '   ' + '+'.join(['-' * (width * 3)] * 3)
        horizontal_grid_line = '  |' + '+'.join(['-' * (max_cell_width * self.box_group_size) + '-'] * self.box_group_size) + '|'

        # Print column headings
        heading_string = '  |'
        for col_name in self.column_names:
            heading_string += col_name.center(max_cell_width, ' ')
            if col_name in self.column_boundaries:
                heading_string += ' |'
        print(heading_string)
        print(horizontal_grid_line)

        # Print each row
        for row_name in self.row_names:
            row_string = ''
            for col_name in self.column_names:
                row_string += self.puzzle_dict[col_name + row_name].center(max_cell_width)
                if col_name in self.column_boundaries:
                    row_string += ' |'
            print(row_name + ' |' + row_string)
            if row_name in self.row_boundaries:
                print(horizontal_grid_line)
        print()

    def is_solved(self):
        for cell in self.puzzle_dict.values():
            if len(cell) != 1:
                return False
        return True
