import logging

from termcolor import colored

from Chain_Endpoint import Chain_Endpoint
from Grid_Puzzle import Grid_Puzzle
from Numbrix_Cell import Numbrix_Cell
from Two_Neighbor_Values_Exception import Two_Neighbor_Values_Exception
from Duplicate_Cell_Exception import Duplicate_Cell_Exception

logging.basicConfig(format='%(message)s', filename='grid-puzzle.log', filemode='w', level=logging.DEBUG)


class Numbrix(Grid_Puzzle):

    def create_puzzle(self):
        cell_position_in_definition = 0
        cell_dictionary = {}
        for column in self.column_names:
            for row in self.row_names:
                address = column + row
                value = self.definition[cell_position_in_definition]
                if value is None:
                    candidates = []
                else:
                    candidates = [value]
                new_cell = Numbrix_Cell(address, candidates)
                if not new_cell.is_empty():
                    self.given_cells.append(new_cell)
                cell_dictionary[address] = new_cell
                cell_position_in_definition += 1
        if len(cell_dictionary) != len(self.definition):
            raise ValueError("Puzzle definition did not map correctly!")
        return cell_dictionary

    def get_display_cell(self, cell):
        attributes = []
        if cell.is_link_endpoint(self.get_cell_neighbors(cell)):
            cell_color = 'blue'
        elif cell in self.given_cells:
            cell_color = 'white'
            attributes.append('dark')
        # The last cell in the latest it the latest guessed cell
        elif len(self.guessed_cells) > 0 and cell == self.guessed_cells[-1]:
            cell_color = 'red'
            attributes.append('underline')
        elif cell in self.guessed_cells:
            cell_color = 'yellow'
            attributes.append('bold')
        else:
            cell_color = 'green'
        return colored(cell.candidates_string().center(self.get_display_cell_width()), cell_color, attrs=attributes)

    def get_display_row(self, row_name):
        """"Return a string representation of the specified row"""
        row_string = ''
        for col_name in self.column_names:
            cell_address = col_name + row_name
            cell = self.get_cell(cell_address)
            row_string += self.get_display_cell(cell)
            row_string += '|'
        return row_name.rjust(3) + ' |' + row_string

    def display(self, force_display=False):
        if logging.DEBUG or force_display:
            print()
            print(self.get_display_header())
            print(self.get_horizontal_puzzle_boundary())

            for row_name in self.row_names:
                print(self.get_display_row(row_name))
            print(self.get_horizontal_puzzle_boundary())
            print(f'The current puzzle count is {self.get_current_puzzle_count()}')
            print(f'The current guess depth is {len(self.guessed_cells)}')
            print(f'Number of guesses: {Grid_Puzzle.number_of_guesses}')
            print(f'Number of backtracks: {Grid_Puzzle.number_of_backtracks}')

    def reduce(self):
        current_puzzle_size = self.get_current_puzzle_count()
        if self.is_solved():
            raise Exception('We should never get here. The puzzle is already solved or invalid')

        while True:
            for cell in self.get_all_cells():
                cell.reduce_neighbors(self.get_cell_neighbors(cell))
            if self.is_solved():
                return

            self.fill_1_cell_gaps()

            updated_puzzle_size = self.get_current_puzzle_count()
            if self.is_solved() or current_puzzle_size == updated_puzzle_size:
                # Break out of the loop, since there was no change in the puzzle size
                return
            logging.debug(f"Reduced puzzle from {current_puzzle_size} cells solved to {updated_puzzle_size} cells solved")
            current_puzzle_size = updated_puzzle_size

    def get_chain_endpoints(self):
        endpoints = []
        for cell in self.get_all_cells():
            if cell.is_link_endpoint(self.get_cell_neighbors(cell)):
                endpoints.append(cell)
        return endpoints

    def custom_reduce(self):
        self.fill_1_cell_gaps()

    def fill_1_cell_gaps(self):
        chain_endpoints = self.get_chain_endpoints()
        for cell in chain_endpoints:
            for other_cell in chain_endpoints:
                if cell.distance_to_cell(other_cell) == 2:
                    between_cell = self.get_cell_between(cell, other_cell)
                    if between_cell.is_empty():
                        if cell.get_value() - other_cell.get_value() == 2:
                            between_cell.set_value(other_cell.get_value() + 1)
                            # Once one cell has been updated, we have to break out of this loop
                            # because our list of chain endpoints is no longer valid and our
                            # code assumes this to be so.
                            return
                        elif other_cell.get_value() - cell.get_value() == 2:
                            between_cell.set_value(cell.get_value() + 1)
                            return

    def get_cell_between(self, cell, other_cell):
        assert cell.distance_to_cell(other_cell) == 2
        if cell.get_row() == other_cell.get_row():
            if cell.get_column_number() > other_cell.get_column_number():
                return self.get_cell(chr(other_cell.get_column_number() + ord('A')) + cell.get_row())
            else:
                return self.get_cell(chr(other_cell.get_column_number() + ord('A') - 2) + cell.get_row())
        else:
            if cell.get_row_number() > other_cell.get_row_number():
                return self.get_cell(cell.get_column() + str(cell.get_row_number() - 1))
            else:
                return self.get_cell(cell.get_column() + str(cell.get_row_number() + 1))

    def get_empty_neighbors(self, cell):
        return [neighbor for neighbor in self.get_cell_neighbors(cell) if neighbor.is_empty()]

    def calculate_required_neighbor_values_for_chain_endpoint(self, cell):
        possible_neighbors_values = [cell.get_value() - 1, cell.get_value() + 1]
        neighbor_values = [neighbor.get_value() for neighbor in self.get_cell_neighbors(cell) if not neighbor.is_empty()]
        for value in neighbor_values:
            if value in possible_neighbors_values:
                possible_neighbors_values.remove(value)
        return possible_neighbors_values

    def get_guessing_cell(self):
        """This returns a Chain_Endpoint object"""
        guess_candidates = []

        chain_endpoints = self.get_chain_endpoints()
        chain_endpoints.sort(key=len)
        for cell in chain_endpoints:
            empty_neighbors = self.get_empty_neighbors(cell)
            try:
                required_neighbor_value = self.calculate_required_neighbor_values_for_chain_endpoint(cell)
            except Two_Neighbor_Values_Exception:
                print("Skipping chain with two possible neighbor values")
                continue

            # Check that the required value isn't already used elsewhere in the puzzle (indicating a invalid guess)
            if required_neighbor_value in self.get_all_values():
                raise Duplicate_Cell_Exception(f"Invalid puzzle! Cell {cell} requires an empty neighbor to have value {required_neighbor_value}, but it is used elsewhere in the puzzle")

            smallest_difference = self.calculate_smallest_value_difference_to_other_chains(cell)
            guess_candidates.append(Chain_Endpoint(cell, empty_neighbors, required_neighbor_value, smallest_difference))

        sorted_guesses = sorted(guess_candidates, key=lambda x: (len(x), x.required_neighbor_values, x.value_difference_to_another_chain, x.endpoint.get_value()))
        return sorted_guesses[0]

    def get_all_values(self):
        values = []
        for cell in self.puzzle_dict.values():
            values.extend(cell.candidates)
        return values

    def calculate_smallest_value_difference_to_other_chains(self, cell_endpoint):
        minimum_difference = 100  # A number larger than the greatest distance possible
        for current_cell_endpoint in self.get_chain_endpoints():
            difference = abs(cell_endpoint.get_value() - current_cell_endpoint.get_value())
            if difference != 0 and difference < minimum_difference:
                minimum_difference = difference
        return minimum_difference

    def update_with_guess(self, _, current_guess):
        """The parameters here are from the another puzzle, so we need to make changes in our cells"""
        (cell_to_guess, value_to_guess) = current_guess
        my_cell = self.get_cell(cell_to_guess.address)
        my_cell.set_candidates([value_to_guess])
        self.guessed_cells.append(my_cell)

    def is_solved(self):
        # Make sure that all cells are filled
        empty_cells = [cell for cell in self.get_all_cells() if cell.is_empty()]
        if len(empty_cells) > 0:
            return False

        # Check for each cell having just one candidate as a value
        all_values = self.get_all_values()
        if len(all_values) != self.size ** 2:
            return False

        # Check for no repeated values
        if len(all_values) != len(set(all_values)):
            return False

        # Check for no chain endpoints
        if len(self.get_chain_endpoints()) > 0:
            return False

        return True
