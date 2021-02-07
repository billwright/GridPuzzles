from Grid_Puzzle import Grid_Puzzle
import copy
import math
import logging
from termcolor import colored

from Blanking_Cell_Exception import Blanking_Cell_Exception
from Duplicate_Cell_Exception import Duplicate_Cell_Exception
from Cell import Cell
from Reducing_Group import Reducing_Group
from grid_utils import cross

logging.basicConfig(format='%(message)s', filename='sudoku.log', filemode='w', level=logging.INFO)


class Sudoku_Puzzle(Grid_Puzzle):
    # TODO: Rename this class to just Sudoku
    number_of_guesses = 0  # This is a class or static variable
    number_of_backtracks = 0  # This is a class or static variable

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
        return self.row_groups + self.column_groups + self.box_groups

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
            row_string += colored(self.get_cell(cell_address).candidates.center(self.get_display_cell_width()), cell_color)
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
        print(f'Number of guesses: {Sudoku_Puzzle.number_of_guesses}')
        print(f'Number of backtracks: {Sudoku_Puzzle.number_of_backtracks}')
        print()

    def is_solved(self):
        self.check_consistency()
        for cell in self.get_all_cells():
            if cell.get_size() != 1:
                return False
        # Check to make sure each group only consists of unique values
        for group in self.get_all_groups():
            all_group_candidates = group.get_all_candidates()
            if len(set(all_group_candidates)) != self.size:
                raise Exception(f'ERROR! I found a group with a duplicated value: {group}')
        return True

    def check_consistency(self):
        for group in self.get_all_groups():
            group.check_consistency()

    def get_groups_for_cell(self, cell):
        return [group for group in self.get_all_groups() if cell in group]

    def get_associated_cells(self, cell):
        groups = self.get_groups_for_cell(cell)
        associated_cells = []
        for group in groups:
            associated_cells.extend(group.get_associated_cells(cell))
        return set(associated_cells)

    def remove_candidates_from_cell_associates(self, cell):
        if len(cell.candidates) != 1:
            raise Exception("We should only call this method with a singleton cell")

        associated_cells = self.get_associated_cells(cell)
        for curr_cell in associated_cells:
            curr_cell.remove_candidates(cell.candidates)

    def get_current_puzzle_count(self):
        # This is a metric indicating how close the puzzle is to being solved.
        # A solved puzzle has a size of nxn, as it has only one value in each cell.
        # The maximum value would be n x n x n, but that would never occur as it
        # would correspond to a completely empty puzzle.
        # values_sizes = [(len(self.get_cell_value(address)) for address in self.get_all_cell_addresses()]
        candidates_sizes = [cell.get_size() for cell in self.get_all_cells()]
        return sum(candidates_sizes)

    def get_all_cells_sorted_by_size(self):
        return sorted(self.get_all_cells())

    def get_guessing_cell(self):
        for cell in self.get_all_cells_sorted_by_size():
            if cell.get_size() > 1:
                return cell
        raise Exception('We should never get here. If all cells are of size 1, then we should not be guessing')

    def get_cells_with_candidates_size(self, candidates_size):
        return [cell for cell in self.get_all_cells() if cell.get_size() == candidates_size]

    def find_singlets(self):
        return self.get_cells_with_candidates_size(1)

    def find_doubles(self):
        doubles = []
        for possible_double_cell in self.get_cells_with_candidates_size(2):
            cell_associates = self.get_associated_cells(possible_double_cell)
            for potential_match in cell_associates:
                if possible_double_cell.candidates == potential_match.candidates:
                    # Check if the reverse of this tuple is already in our list
                    if (potential_match, possible_double_cell) not in doubles:
                        doubles.append((possible_double_cell, potential_match))
        return doubles

    def find_matchlets(self):
        matchlets = []
        for group in self.get_all_groups():
            matchlets.extend(group.find_matchlets())

        matchlets.sort(key=len, reverse=True)
        return matchlets

    def get_double_addresses(self):
        addresses = []
        for double in self.find_doubles():
            addresses.append(double[0])
            addresses.append(double[1])
        return set(addresses)

    def search_and_reduce_singlets(self):
        for cell in self.find_singlets():
            self.remove_candidates_from_cell_associates(cell)

    def search_and_reduce_doublets(self):
        for double in self.find_doubles():
            # Get groups of first address in the double (it doesn't matter which address we use)
            common_groups = [group for group in self.get_groups_for_cell(double[0]) if double[1] in group]
            for group in common_groups:
                for cell in group:
                    if cell not in double:
                        cell.remove_candidates(double[0].candidates)

    def search_and_reduce_matchlets(self, sizes_to_reduce=None):
        """This method finds and reduces matchlets in the puzzle

        Attributes:
            - (list) sizes_to_reduce:  This is optional and if left off, it reduces everything
                                If specified, it should be a list of matchlet sizes to reduce"""

        for matchlet in self.find_matchlets():
            if sizes_to_reduce is not None and len(matchlet) not in sizes_to_reduce:
                logging.debug(
                    f'Per the configuration passed to this method, skipping matchlets of size {len(matchlet)}')
                continue  # Skip this group

            matchlet.reduce()

            # for group in self.get_groups_for_cell(matchlet[0]):
            #     all_cells_in_group = True
            #     for cell in matchlet:
            #         if cell not in group:
            #             all_cells_in_group = False   # This cell isn't in this group, then this is NOT the common group. Go to next group
            #     if all_cells_in_group:
            #         # Reduce other cells in the group
            #         for cell in group:
            #             if cell not in matchlet:
            #                 cell.remove_candidates(matchlet[0].candidates)

    def search_and_reduce_exclusive_cells(self):
        for group in self.get_all_groups():
            logging.debug(f'Looking for exclusions in {group}')
            group.search_and_reduce_exclusions()

    def reduce(self):
        current_puzzle_size = self.get_current_puzzle_count()
        logging.info(current_puzzle_size)
        if self.is_solved():
            raise Exception('We should never get here. The puzzle is already solved or invalid')

        while True:
            self.search_and_reduce_exclusive_cells()
            if self.is_solved():
                return

            self.search_and_reduce_matchlets()

            updated_puzzle_size = self.get_current_puzzle_count()
            if self.is_solved() or current_puzzle_size == updated_puzzle_size:
                # Break out of the loop, since there was no change in the puzzle size
                return
            logging.debug(f"Reduced puzzle from {current_puzzle_size} down to {updated_puzzle_size}")
            current_puzzle_size = updated_puzzle_size

    def search(self):
        """Using depth-first search to solve the sudoku.
        This methods returns True if the puzzle is solved, otherwise False"""
        if self.is_solved():
            raise Exception('We should never get here. The puzzle is already solved or invalid')

        # Solve as much as we can using singlets, doublets, etc.
        self.reduce()

        current_puzzle_size = self.get_current_puzzle_count()
        logging.debug(f"Checking for a solved puzzle. The current count is {current_puzzle_size}")

        if self.is_solved():
            print("Puzzle is solved!")
            logging.info(self.get_current_puzzle_count())
            return self

        # We are stuck and need to guess. Let's choose one of the unfilled cells with the fewest possibilities
        cell_to_guess = self.get_guessing_cell()
        logging.debug("I'm guessing the value of cell:", cell_to_guess)

        # We'll guess each value of the possible values until we find a solution
        for current_guess_candidates in cell_to_guess.candidates[::-1]:
            logging.debug("I'm guessing value:", current_guess_candidates)
            Sudoku_Puzzle.number_of_guesses += 1
            puzzle_with_guess = copy.deepcopy(self)
            cell_to_guess_in_copied_puzzle = puzzle_with_guess.get_cell(cell_to_guess.address)
            cell_to_guess_in_copied_puzzle.set_candidates(current_guess_candidates)

            # Here's the tricky part, recursively call this same method, but we're calling it on a different object
            # Note that this is NOT self.search(), but puzzle_with_guess.search().
            try:
                solved_puzzle = puzzle_with_guess.search()
                if solved_puzzle is not None:
                    return solved_puzzle
                else:
                    logging.debug(
                        f'Our guess of {current_guess_candidates} for Cell {cell_to_guess.address} was wrong.')
            except Blanking_Cell_Exception as error:
                logging.debug(error.message, error.cell)
            except Duplicate_Cell_Exception as error:
                logging.debug(error.message)

        logging.debug(f"Could not find a solution when guessing values for Cell {cell_to_guess}. Backing up...")
        Sudoku_Puzzle.number_of_backtracks += 1
        return None
