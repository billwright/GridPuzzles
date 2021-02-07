from math import sqrt

from Calculation_Group import Calculation_Group
from Grid_Puzzle import Grid_Puzzle
from termcolor import colored

# TODO: Solve KenKen
# TODO: Revisit switch to a list of one-character strings for candidates instead of just a string


class Kenken(Grid_Puzzle):
    def __init__(self, puzzle_group_definitions):
        self.calculation_groups = []
        super().__init__(puzzle_group_definitions)

    def create_puzzle(self):
        """This method is called by the superclass and must return a dictionary that contains all the cells of the puzzle"""
        self.calculation_groups = self.create_calculation_groups()
        puzzle_dictionary = {}
        for group in self.calculation_groups:
            for cell in group:
                puzzle_dictionary[cell.address] = cell
        return puzzle_dictionary

    def create_calculation_groups(self):
        return [Calculation_Group(group_def, self.size) for group_def in self.definition]

    def get_addresses_from_definition(self):
        addresses = []
        for (_, _, cell_addresses) in self.definition:
            addresses.extend(cell_addresses)
        return addresses

    def validate(self):
        # Assume addresses are of this form: A1 -- with first character the column and the second the row
        addresses = self.get_addresses_from_definition()
        columns = set([address[0] for address in addresses])
        rows = set([address[1] for address in addresses])

        if len(rows) != len(columns):
            raise ValueError("Cell addresses do not form a square")

        puzzle_square_root = sqrt(len(addresses))
        if puzzle_square_root != int(puzzle_square_root):
            raise ValueError(f'Only {len(addresses)} cells were defined, which is not a perfect square.')

    def calculate_size(self):
        addresses = self.get_addresses_from_definition()
        return int(sqrt(len(addresses)))

    def get_all_groups(self):
        return super().get_all_groups() + self.calculation_groups

    def get_calculation_group_for_cell(self, cell):
        for group in self.calculation_groups:
            if cell in group:
                return group

    def get_puzzle_display_string(self):
        """Each cell in the puzzle will have a width of max_candidate_width + 2.
           Each cell will have a height of two rows. One for the operation and then the
           candidates on the next line. The puzzle should display like this:
              |  A  |  B  |  C  |
              ‖=====|=====|=====‖
              ‖3/   ‖1-   |     ‖
            1 ‖  1  ‖  2  |  3  ‖
              ‖-----‖=====|=====‖
              ‖     ‖3/   ‖2/   ‖
            2 ‖  3  ‖  1  ‖  2  ‖
              ‖=====‖-----‖-----‖
              ‖2    ‖     ‖     ‖
            3 ‖  2  ‖  3  ‖  1  ‖
              ‖=====+=====+=====‖
           """
        display_string = self.get_display_header() + '\n'
        display_string += self.get_horizontal_puzzle_boundary() + '\n'
        for row in self.row_names:
            display_string += self.get_top_display_line_of_cell(row) + '\n'
            display_string += self.get_bottom_display_line_of_row(row) + '\n'
            display_string += self.get_line_separator_between_row(row) + '\n'
        return display_string

    def display(self):
        print(self.get_puzzle_display_string())

    def write_puzzle_to_file(self, filename):
        file = open(filename, "w")
        file.write(self.get_puzzle_display_string())
        file.close()

    def get_line_separator_between_row(self, row):
        line = "----‖"
        for column in self.column_names:
            line += self.get_bottom_of_cell_display(column, row)
        return line

    def get_bottom_display_line_of_row(self, row):
        line = row.ljust(3) + " ‖"
        for column in self.column_names:
            line += self.get_cell_display(column, row, False)
        return line

    def get_top_display_line_of_cell(self, row):
        line = "    ‖"
        for column in self.column_names:
            line += self.get_cell_display(column, row, True)
        return line

    def get_cell_display(self, column, row, first_row):
        """Returns the first row of the string representation of the cell if first_row is true. Else the second row"""
        cell_width = self.get_display_cell_width()

        current_cell = self.get_cell(column + row)
        current_group = self.get_calculation_group_for_cell(current_cell)
        line = ''
        # If this is the first cell in the group, print the result and operation
        if first_row:
            if current_cell == current_group.cells[0]:
                result_and_op = str(current_group.required_result) + current_group.operator
                line += colored(result_and_op.ljust(cell_width), 'red')
            else:
                line += ' '*cell_width
        else:
            line += colored(current_cell.candidates_string().center(cell_width), 'green')
        cell_to_the_right = self.get_cell_to_right(current_cell)
        if current_group == self.get_calculation_group_for_cell(cell_to_the_right):
            line += '|'
        else:
            line += "‖"
        return line

    def get_bottom_of_cell_display(self, column, row):
        cell_width = self.get_display_cell_width()

        current_cell = self.get_cell(column + row)
        current_group = self.get_calculation_group_for_cell(current_cell)
        cell_beneath = self.get_cell_beneath(current_cell)
        line = ''
        if current_group == self.get_calculation_group_for_cell(cell_beneath):
            line += '-'*cell_width
        else:
            line += '='*cell_width
        cell_to_the_right = self.get_cell_to_right(current_cell)
        if current_group == self.get_calculation_group_for_cell(cell_to_the_right):
            line += '|'
        else:
            line += "‖"
        return line

    def custom_reduce(self):
        for group in self.calculation_groups:
            group.reduce()
