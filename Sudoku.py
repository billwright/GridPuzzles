from Grid_Puzzle import Grid_Puzzle
import math
from termcolor import colored

from Cell import Cell
from Reducing_Group import Reducing_Group
from grid_utils import cross


class Sudoku(Grid_Puzzle):

    def __init__(self, puzzle_string):
        super().__init__(puzzle_string)
        self.box_group_size = int(math.sqrt(self.size))
        self.column_boundaries = self.calculate_column_boundaries()
        self.row_boundaries = self.calculate_row_boundaries()
        self.box_groups = self.create_box_groups()

    def validate(self):
        puzzle_square_root = math.sqrt(len(self.definition))
        if puzzle_square_root != int(puzzle_square_root):
            error_string = f'ERROR: Puzzle string was of length {len(self.definition)}, which is not a perfect square'
            print(error_string)
            raise ValueError(error_string)

    def calculate_size(self):
        return int(math.sqrt(len(self.definition)))

    def calculate_column_boundaries(self):
        return [chr(ord('A') + i * self.box_group_size - 1) for i in
                range(1, self.box_group_size + 1)]

    def calculate_row_boundaries(self):
        return [str((row_number + 1) * self.box_group_size) for row_number in range(0, self.box_group_size)]

    def create_box_groups(self):
        col_name_groups = [self.column_names[i:i + self.box_group_size] for i in
                           range(0, self.size, self.box_group_size)]
        row_name_groups = [self.row_names[i:i + self.box_group_size] for i in range(0, self.size, self.box_group_size)]
        groups = []
        for col_name_group in col_name_groups:
            for row_name_group in row_name_groups:
                group_cells = [self.get_cell(address) for address in cross(col_name_group, row_name_group)]
                group_name = f'Box {col_name_group}-{row_name_group}'
                groups.append(Reducing_Group(group_name, group_cells))
        return groups

    def get_all_groups(self):
        return super().get_all_groups() + self.box_groups

    def get_all_exclusive_and_matchlet_groups(self):
        return super().get_all_exclusive_and_matchlet_groups() + self.box_groups

    def create_puzzle(self):
        addresses = self.get_all_cell_addresses()
        candidates = [(candidate if candidate != '.' else self.possible_candidates()) for candidate in self.definition]

        puzzle_dictionary = {}
        for (address, candidates) in zip(addresses, candidates):
            puzzle_dictionary[address] = Cell(address, candidates)
        return puzzle_dictionary

    def get_horizontal_grid_line(self):
        return '    |' + '+'.join(
            ['-' * (self.get_display_cell_width() * self.box_group_size) + '-'*(self.box_group_size-1)] * self.box_group_size) + '|'

    def get_display_row(self, row_name):
        doubles = self.get_double_addresses()

        row_string = ''
        for col_name in self.column_names:
            cell_address = col_name + row_name
            cell_color = 'blue' if (cell_address in doubles) else 'green'
            row_string += colored(self.get_cell(cell_address).candidates_string().center(self.get_display_cell_width()), cell_color)
            if col_name in self.column_boundaries:
                row_string += '|'
            else:
                row_string += ' '
        return row_name.rjust(3) + ' |' + row_string

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
        print(f'The current puzzle count is {self.get_current_puzzle_count()}')
        print(f'Number of guesses: {Sudoku.number_of_guesses}')
        print(f'Number of backtracks: {Sudoku.number_of_backtracks}')
        print()


