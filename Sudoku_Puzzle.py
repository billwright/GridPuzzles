import math
from termcolor import colored


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
        self.column_boundaries = ''.join(
            [chr(ord('A') + i * self.box_group_size - 1) for i in range(1, self.box_group_size + 1)])
        self.row_boundaries = ''.join([str(i * self.box_group_size) for i in range(1, self.box_group_size + 1)])
        self.column_names = ''.join(chr(ord('A') + col_number) for col_number in range(self.size))
        self.row_names = ''.join(str(row_number + 1) for row_number in range(self.size))

        self.puzzle_dict = self.create_puzzle(puzzle_string)

    def possible_values(self):
        return self.row_names

    def box_groupings(self):
        col_name_groups = [self.column_names[i:i + self.box_group_size] for i in
                           range(0, self.size, self.box_group_size)]
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
                col_group.append(col_name + row_name)
            groups.append(col_group)
        return groups

    def row_groupings(self):
        groups = []
        for row_name in self.row_names:
            row_group = []
            for col_name in self.column_names:
                row_group.append(col_name + row_name)
            groups.append(row_group)
        return groups

    def get_all_groups(self):
        return self.row_groupings() + self.column_groupings() + self.box_groupings()

    def get_all_group_values(self):
        all_group_values = []
        for group in self.get_all_groups():
            all_group_values.append([self.get_cell_value(address) for address in group])
        return all_group_values

    def get_all_cell_addresses(self):
        return cross(self.column_names, self.row_names)

    def create_puzzle(self, puzzle_string):
        addresses = self.get_all_cell_addresses()
        values = [(value if value != '.' else self.possible_values()) for value in puzzle_string]

        return dict(zip(addresses, values))

    def get_cell_value(self, cell_address):
        return self.puzzle_dict[cell_address]

    def get_max_cell_width(self):
        return 1 + max(len(s) for s in self.puzzle_dict.values())

    def get_horizontal_grid_line(self):
        return '  |' + '+'.join(
            ['-' * (self.get_max_cell_width() * self.box_group_size) + '-'] * self.box_group_size) + '|'

    def get_display_header(self):
        heading_string = '  |'
        for col_name in self.column_names:
            heading_string += col_name.center(self.get_max_cell_width(), ' ')
            if col_name in self.column_boundaries:
                heading_string += ' |'
        return heading_string

    def get_display_row(self, row_name):
        doubles = self.get_double_addresses()

        row_string = ''
        for col_name in self.column_names:
            cell_address = col_name + row_name
            cell_color = 'blue' if (cell_address in doubles) else 'green'
            row_string += colored(self.get_cell_value(cell_address).center(self.get_max_cell_width()), cell_color)
            if col_name in self.column_boundaries:
                row_string += ' |'
        return row_name + ' |' + row_string

    def display(self):
        # Print column headings
        print()
        print(self.get_display_header())
        print(self.get_horizontal_grid_line())

        # Print each row
        for row_name in self.row_names:
            print(self.get_display_row(row_name))
            if row_name in self.row_boundaries:
                print(self.get_horizontal_grid_line())
        print('The current puzzle count is', self.get_current_puzzle_count())
        print()

    def is_solved(self):
        for cell in self.puzzle_dict.values():
            if len(cell) != 1:
                return False
        for group in self.get_all_group_values():
            if len(set(group)) != self.size:
                return False
        return True

    def get_groups_for_cell(self, cell_address):
        return [group for group in self.get_all_groups() if cell_address in group]

    def get_associated_cells(self, cell_address):
        groups = self.get_groups_for_cell(cell_address)
        associated_cells = []
        for group in groups:
            for address in group:
                if address != cell_address:
                    associated_cells.append(address)
        return set(associated_cells)

    def remove_from_values(self, cell_address, value):
        current_cell_values = self.get_cell_value(cell_address)
        self.puzzle_dict[cell_address] = current_cell_values.replace(value, '')

    def remove_value_from_cell_associates(self, cell_address, value):
        associated_cells = self.get_associated_cells(cell_address)
        for address in associated_cells:
            self.remove_from_values(address, value)

    def get_current_puzzle_count(self):
        # This is a metric indicating how close the puzzle is to being solved.
        # A solved puzzle has a size of nxn, as it has only one value in each cell.
        # The maximum value would be n x n x n, but that would never occur as it
        # would correspond to a completely empty puzzle.
        # values_sizes = [(len(self.get_cell_value(address)) for address in self.get_all_cell_addresses()]
        value_sizes = [len(self.get_cell_value(address)) for address in self.get_all_cell_addresses()]
        return sum(value_sizes)

    def get_cells_with_value_size(self, value_size):
        return [address for address in self.get_all_cell_addresses() if len(self.get_cell_value(address)) == value_size]

    def find_singletons(self):
        return self.get_cells_with_value_size(1)

    def find_doubles(self):
        doubles = []
        for possible_double_address in self.get_cells_with_value_size(2):
            cell_value = self.get_cell_value(possible_double_address)
            cell_associates = self.get_associated_cells(possible_double_address)
            for potential_match in cell_associates:
                if cell_value == self.get_cell_value(potential_match):
                    # Check if the reverse of this tuple is already in our list
                    if (potential_match, possible_double_address) not in doubles:
                        doubles.append((possible_double_address, potential_match))
        return doubles

    def get_double_addresses(self):
        addresses = []
        for double in self.find_doubles():
            addresses.append(double[0])
            addresses.append(double[1])
        return set(addresses)

    def remove_values_from_cell(self, address, values):
        for value in values:
            self.remove_from_values(address, value)

    def search_and_reduce_singletons(self):
        for address in self.find_singletons():
            self.remove_value_from_cell_associates(address, self.get_cell_value(address))

    def search_and_reduce_doubles(self):
        for double in self.find_doubles():
            # Get groups of first address in the double (it doesn't matter which address we use)
            common_groups = [group for group in self.get_groups_for_cell(double[0]) if double[1] in group]
            for group in common_groups:
                for address in group:
                    if address not in double:
                        self.remove_values_from_cell(address, self.get_cell_value(double[0]))

    def solve(self):
        while True:
            current_puzzle_size = self.get_current_puzzle_count()
            print('Looking to reduce singletons... The current puzzle size is', current_puzzle_size)

            self.search_and_reduce_singletons()
            self.search_and_reduce_doubles()
            if current_puzzle_size == self.get_current_puzzle_count():
                # Break out of the loop, since there was no change in the puzzle size
                break
