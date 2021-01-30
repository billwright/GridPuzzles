import math
from termcolor import colored
from Cell import Cell
import copy
from Blanking_Cell_Exception import Blanking_Cell_Exception


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
        self.column_boundaries = [chr(ord('A') + i * self.box_group_size - 1) for i in range(1, self.box_group_size + 1)]
        self.row_boundaries = [str(i * self.box_group_size) for i in range(1, self.box_group_size + 1)]
        self.column_names = [chr(ord('A') + col_number) for col_number in range(self.size)]
        self.row_names = [str(row_number + 1) for row_number in range(self.size)]

        self.puzzle_dict = self.create_puzzle(puzzle_string)

    def possible_values(self):
        return '1234567890ABCDEF'[0:self.size]

    def box_groupings(self):
        col_name_groups = [self.column_names[i:i + self.box_group_size] for i in
                           range(0, self.size, self.box_group_size)]
        row_name_groups = [self.row_names[i:i + self.box_group_size] for i in range(0, self.size, self.box_group_size)]
        groups = []
        for col_name_group in col_name_groups:
            for row_name_group in row_name_groups:
                group = [self.get_cell(address) for address in cross(col_name_group, row_name_group)]
                groups.append(group)
        return groups

    def column_groupings(self):
        groups = []
        for col_name in self.column_names:
            col_group = []
            for row_name in self.row_names:
                col_group.append(self.get_cell(col_name + row_name))
            groups.append(col_group)
        return groups

    def row_groupings(self):
        groups = []
        for row_name in self.row_names:
            row_group = []
            for col_name in self.column_names:
                row_group.append(self.get_cell(col_name + row_name))
            groups.append(row_group)
        return groups

    def get_all_groups(self):
        return self.row_groupings() + self.column_groupings() + self.box_groupings()

    def get_all_group_values(self):
        all_group_values = []
        for group in self.get_all_groups():
            all_group_values.append([cell.values for cell in group])
        return all_group_values

    def get_all_cell_addresses(self):
        return cross(self.column_names, self.row_names)

    def create_puzzle(self, puzzle_string):
        addresses = self.get_all_cell_addresses()
        values = [(value if value != '.' else self.possible_values()) for value in puzzle_string]

        puzzle_dictionary = {}
        for (address, values) in zip(addresses, values):
            puzzle_dictionary[address] = Cell(address, values)
        return puzzle_dictionary

    def get_cell(self, cell_address):
        return self.puzzle_dict[cell_address]

    def get_max_cell_width(self):
        return 1 + max(cell.get_size() for cell in self.get_all_cells())

    def get_horizontal_grid_line(self):
        return '    |' + '+'.join(
            ['-' * (self.get_max_cell_width() * self.box_group_size) + '-'] * self.box_group_size) + '|'

    def get_display_header(self):
        heading_string = '    |'
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
            row_string += colored(self.get_cell(cell_address).values.center(self.get_max_cell_width()), cell_color)
            if col_name in self.column_boundaries:
                row_string += ' |'
        return row_name.center(3) + ' |' + row_string

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
        for cell in self.get_all_cells():
            if cell.get_size() != 1:
                return False
        for group in self.get_all_group_values():
            if len(set(group)) != self.size:
                return False
        return True

    def get_groups_for_cell(self, cell):
        return [group for group in self.get_all_groups() if cell in group]

    def get_associated_cells(self, cell):
        groups = self.get_groups_for_cell(cell)
        associated_cells = []
        for group in groups:
            for current_cell in group:
                if current_cell != cell:
                    associated_cells.append(current_cell)
        return set(associated_cells)

    def remove_value_from_cell_associates(self, cell):
        associated_cells = self.get_associated_cells(cell)
        for curr_cell in associated_cells:
            curr_cell.remove_values(cell.values)

    def get_current_puzzle_count(self):
        # This is a metric indicating how close the puzzle is to being solved.
        # A solved puzzle has a size of nxn, as it has only one value in each cell.
        # The maximum value would be n x n x n, but that would never occur as it
        # would correspond to a completely empty puzzle.
        # values_sizes = [(len(self.get_cell_value(address)) for address in self.get_all_cell_addresses()]
        value_sizes = [cell.get_size() for cell in self.get_all_cells()]
        return sum(value_sizes)

    def get_all_cells(self):
        return self.puzzle_dict.values()

    def get_all_cells_sorted_by_size(self):
        return sorted(self.get_all_cells())

    def get_guessing_cell(self):
        for cell in self.get_all_cells_sorted_by_size():
            if cell.get_size() > 1:
                return cell
        self.display()
        raise Exception('We should never get here. If all cells are of size 1, then we should not be guessing')

    def get_cells_with_value_size(self, value_size):
        return [cell for cell in self.get_all_cells() if cell.get_size() == value_size]

    def find_singletons(self):
        return self.get_cells_with_value_size(1)

    def find_doubles(self):
        doubles = []
        for possible_double_cell in self.get_cells_with_value_size(2):
            cell_associates = self.get_associated_cells(possible_double_cell)
            for potential_match in cell_associates:
                if possible_double_cell.values == potential_match.values:
                    # Check if the reverse of this tuple is already in our list
                    if (potential_match, possible_double_cell) not in doubles:
                        doubles.append((possible_double_cell, potential_match))
        return doubles

    def find_matchlets(self):
        matchlets = []  # This is a list of matchlets, which are always tuples
        all_matched_cells = []  # A flat list to remember all matches cells to avoid duplicates

        for possible_match_cell in self.get_all_cells():
            for cell_group in self.get_groups_for_cell(possible_match_cell):
                matchlet = [cell for cell in cell_group if cell.values == possible_match_cell.values]
                # Check to make sure this is a matchlet, meaning the size of the values has to equal the number of cells
                if len(matchlet) == len(possible_match_cell.values):
                    previously_matched_cells = [cell for cell in matchlet if cell in all_matched_cells]
                    if len(previously_matched_cells) == 0:
                        matchlets.append(tuple(matchlet))
                        for cell in matchlet:
                            all_matched_cells.append(cell)
        matchlets.sort(key=len, reverse=True)
        return matchlets

    def get_double_addresses(self):
        addresses = []
        for double in self.find_doubles():
            addresses.append(double[0])
            addresses.append(double[1])
        return set(addresses)

    def search_and_reduce_singletons(self):
        for cell in self.find_singletons():
            self.remove_value_from_cell_associates(cell)

    def search_and_reduce_doubles(self):
        for double in self.find_doubles():
            # Get groups of first address in the double (it doesn't matter which address we use)
            common_groups = [group for group in self.get_groups_for_cell(double[0]) if double[1] in group]
            for group in common_groups:
                for cell in group:
                    if cell not in double:
                        cell.remove_values(double[0].values)

    def search_and_reduce_matchlets(self, sizes_to_reduce=None):
        """This method finds and reduces matchlets in the puzzle

        Attributes:
            - (list) sizes_to_reduce:  This is optional and if left off, it reduces everything
                                If specified, it should be a list of matchlet sizes to reduce"""

        for matchlet in self.find_matchlets():
            if sizes_to_reduce is not None and len(matchlet) not in sizes_to_reduce:
                print(f'Per the configuration passed to this method, skipping matchlets of size {len(matchlet)}')
                continue    # Skip this group

            for group in self.get_groups_for_cell(matchlet[0]):
                all_cells_in_group = True
                for cell in matchlet:
                    if cell not in group:
                        all_cells_in_group = False   # This cell isn't in this group, then this is NOT the common group. Go to next group
                if all_cells_in_group:
                    # Reduce other cells in the group
                    for cell in group:
                        if cell not in matchlet:
                            cell.remove_values(matchlet[0].values)

    @staticmethod
    def search_and_reduce_exclusions_in_group(group):
        candidate_cell_map = dict()    # Here we keep track of each candidate and which cells it appears in
        for cell in group:
            if cell.get_size() > 1:
                for candidate in cell.values:
                    if candidate not in candidate_cell_map.keys():
                        candidate_cell_map[candidate] = []
                    candidate_cell_map[candidate].append(cell)
        exclusions = [(candidate, exclusion_cells) for (candidate, exclusion_cells) in candidate_cell_map.items() if len(exclusion_cells) == 1]
        for (candidate, exclusion_cells) in exclusions:
            exclusion_cells[0].set_values(candidate)

    def reduce(self):
        while True:
            current_puzzle_size = self.get_current_puzzle_count()
            print("Puzzle size is currently:", current_puzzle_size)

            # print('Looking to reduce singletons... The current puzzle size is', current_puzzle_size)
            self.search_and_reduce_singletons()
            # print('Looking to reduce doublets... The current puzzle size is', current_puzzle_size)
            self.search_and_reduce_doubles()
            # self.search_and_reduce_matchlets([1, 2])
            # self.search_and_reduce_matchlets()
            updated_puzzle_size = self.get_current_puzzle_count()
            if current_puzzle_size == updated_puzzle_size:
                # Break out of the loop, since there was no change in the puzzle size
                break

    def search(self):
        """Using depth-first search to solve the sudoku.
        This methods returns True if the puzzle is solved, otherwise False"""

        # Solve as much as we can using singletons, doublets, etc.
        self.reduce()

        if self.is_solved():
            print("Puzzle is solved!")
            return self

        # We are stuck and need to guess. Let's choose one of the unfilled cells with the fewest possibilities
        cell_to_guess = self.get_guessing_cell()
        # print("I'm guessing the value of cell:", cell_to_guess)

        # We'll guess each value of the possible values until we find a solution
        for current_guess_value in cell_to_guess.values:
            # print("I'm guessing value:", current_guess_value)
            puzzle_with_guess = copy.deepcopy(self)
            cell_to_guess_in_copied_puzzle = puzzle_with_guess.get_cell(cell_to_guess.address)
            cell_to_guess_in_copied_puzzle.set_values(current_guess_value)

            # Here's the tricky part, recursively call this same method, but we're calling it on a different object
            # Note that this is NOT self.search(), but puzzle_with_guess.search().
            try:
                solved_puzzle = puzzle_with_guess.search()
                if solved_puzzle is not None:
                    return solved_puzzle
                else:
                    print(f'Our guess of {current_guess_value} for Cell {cell_to_guess.address} was wrong.')
            except Blanking_Cell_Exception as error:
                print(error.message, error.cell)

        # print(f"Could not find a solution when guessing values for Cell {cell_to_guess}. Backing up...")
        return None
