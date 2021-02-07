from Reducing_Group import Reducing_Group
from grid_utils import cross
from Blanking_Cell_Exception import Blanking_Cell_Exception
from Duplicate_Cell_Exception import Duplicate_Cell_Exception
import copy
import logging

logging.basicConfig(format='%(message)s', filename='grid-puzzle.log', filemode='w', level=logging.INFO)


class Grid_Puzzle(object):
    number_of_guesses = 0  # This is a class or static variable
    number_of_backtracks = 0  # This is a class or static variable

    def __init__(self, puzzle_definition):
        self.definition = puzzle_definition
        self.validate()
        self.size = self.calculate_size()

        self.column_names = [chr(ord('A') + col_number) for col_number in range(self.size)]
        self.row_names = [str(row_number + 1) for row_number in range(self.size)]

        self.puzzle_dict = self.create_puzzle()
        self.row_groups = self.create_row_groups()
        self.column_groups = self.create_column_groups()

    def validate(self):
        raise NotImplementedError('Subclass must implement this method!')

    def create_column_groups(self):
        groups = []
        for col_name in self.column_names:
            col_cells = []
            for row_name in self.row_names:
                col_cells.append(self.get_cell(col_name + row_name))
            groups.append(Reducing_Group(f'Column {col_name}', col_cells))
        return groups

    def create_row_groups(self):
        groups = []
        for row_name in self.row_names:
            row_cells = []
            for col_name in self.column_names:
                row_cells.append(self.get_cell(col_name + row_name))
            groups.append(Reducing_Group(f'Row {row_name}', row_cells))
        return groups

    def possible_candidates(self):
        return '1234567890ABCDEF'[0:self.size]

    def get_all_group_candidates(self):
        all_group_candidates = []
        for group in self.get_all_groups():
            all_group_candidates.append(group.get_all_candidates())
        return all_group_candidates

    def get_all_groups(self):
        return self.row_groups + self.column_groups

    def get_all_exclusive_and_matchlet_groups(self):
        return self.row_groups + self.column_groups

    def get_all_cell_addresses(self):
        return cross(self.column_names, self.row_names)

    def get_cell(self, cell_address):
        return self.puzzle_dict[cell_address]

    def get_cell_to_right(self, cell):
        # We add one because otherwise we'd get 0 for the column number of column A
        column_number = ord(cell.address[0]) - ord('A') + 1
        if column_number == self.size:
            return None
        row = cell.address[1:]

        # Here we increment the column, but we don't need to add one, since we already did this above
        column = chr(column_number + ord('A'))
        return self.get_cell(column + row)

    def get_cell_beneath(self, cell):
        row = int(cell.address[1:])
        if row == self.size:
            return None
        column = cell.address[0]
        return self.get_cell(column + str(row+1))

    def get_all_cells(self):
        return self.puzzle_dict.values()

    def get_max_cell_candidate_width(self):
        return max(cell.get_size() for cell in self.get_all_cells())

    def get_display_cell_width(self):
        return self.get_max_cell_candidate_width() + 2

    def get_display_header(self):
        heading_string = '    |'
        for col_name in self.column_names:
            heading_string += col_name.center(self.get_display_cell_width())
            heading_string += '|'
        return heading_string

    def get_horizontal_puzzle_boundary(self):
        line = '----‖'
        for i in range(1, self.size+1):
            line += '='*(self.get_max_cell_candidate_width()+2) + '‖'
        return line

    def is_solved(self):
        self.check_consistency()
        for cell in self.get_all_cells():
            if cell.get_size() != 1:
                return False
        # Check to make sure each group only consists of unique values
        for group in self.get_all_groups():
            all_group_candidates = group.get_all_candidates()
            flat_list = [candidate for group_candidates in all_group_candidates for candidate in group_candidates]
            if len(set(flat_list)) != self.size:
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
        for group in self.get_all_exclusive_and_matchlet_groups():
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
        for group in self.get_all_exclusive_and_matchlet_groups():
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
        """Using depth-first search to solve the puzzle.
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
            Grid_Puzzle.number_of_guesses += 1
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
        Grid_Puzzle.number_of_backtracks += 1
        return None
