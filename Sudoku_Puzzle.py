import math


class Sudoku_Puzzle(object):

    def __init__(self, puzzle_string):
        self.size = int(math.sqrt(len(puzzle_string)))
        self.box_group_size = int(math.sqrt(self.size))

        self.column_names = ''.join(chr(ord('A') + col_number) for col_number in range(self.size))
        self.row_names = ''.join(str(row_number + 1) for row_number in range(self.size))

        self.puzzle = self.create_puzzle(puzzle_string)

    def possible_values(self):
        return self.row_names

    def cross(self, cols, rows):
        # We want the addresses ordered by rows, meaning all the addresses in the first row
        # before going on to the second row. But, we use the column header first in the address.
        # This addressing mimics spreadsheets
        return [c + r for r in rows for c in cols]

    def box_groupings(self):
        col_name_groups = [self.column_names[i:i + self.box_group_size] for i in range(0, self.size, self.box_group_size)]
        row_name_groups = [self.row_names[i:i + self.box_group_size] for i in range(0, self.size, self.box_group_size)]
        # groups = []
        # for col_name_group in col_name_groups:
        #     for row_name_group in row_name_groups:
        #         groups.append(cross(col_name_group, row_name_group))
        # return groups
        return [self.cross(col_name_group, row_name_group) for col_name_group in col_name_groups
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
        addresses = self.cross(self.column_names, self.row_names)
        values = [(value if value != '.' else self.possible_values()) for value in puzzle_string]

        return dict(zip(addresses, values))

    def display(self):
        width = 1 + max(len(s) for s in self.puzzle.values())

        # Print column headings
        print('   ' + ''.join(col_name.center(width, ' ') for col_name in list(self.column_names)))

        # Print each row
        for row_name in self.row_names:
            row_values = (self.puzzle[col_name + row_name].center(width) for col_name in self.column_names)
            print(row_name + ' |' + ''.join(row_values))
