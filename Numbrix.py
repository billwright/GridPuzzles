import logging

from termcolor import colored

from Chain_Endpoint import Chain_Endpoint
from Grid_Puzzle import Grid_Puzzle
from Numbrix_Cell import Numbrix_Cell
from Inconsistent_Puzzle_Exception import Inconsistent_Puzzle_Exception
from Duplicate_Cell_Value_Exception import Duplicate_Cell_Value_Exception
from grid_utils import flatten_and_de_dup


def endpoint_sorting_criteria():
    return lambda x: (
        x.value_difference_to_another_chain,
        len(x.open_neighbors),
        -x.chain_length,
        x.endpoint.get_value())


# Talk about this function vs. an instance method (no need for self here) or a static method (tying to this class as it doesn't make sense as a general function
def sort_chain_endpoints_for_guessing(endpoints):
    """We always want to guess from the endpoint of the chain that is closest to connecting with another chain,
    as that should cause us to fail earlier, if we guess wrong. For instance if we are trying to extend a chain that
    ends in 40 and connect it up to a chain that starts with 43, we can only guess locations for 41 and 42 before
    we'd hit the duplicate cell value inconsistency and know we have to back up and try again. Those endpoints are
    only looking for one, required value, so we look for those first."""

    one_required_value_endpoints = [endpoint for endpoint in endpoints if len(endpoint.required_neighbor_values) == 1]
    if one_required_value_endpoints:
        return sorted(one_required_value_endpoints, key=endpoint_sorting_criteria())
    two_required_value_endpoints = [endpoint for endpoint in endpoints if len(endpoint.required_neighbor_values) == 2]
    if two_required_value_endpoints:
        return sorted(two_required_value_endpoints, key=endpoint_sorting_criteria())
    return sorted(endpoints, key=endpoint_sorting_criteria())


class Numbrix(Grid_Puzzle):

    def create_puzzle(self):
        cell_position_in_definition = 0
        cell_dictionary = {}
        for row in self.row_names:
            for column in self.column_names:
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

    @staticmethod
    def print_color_legend():
        print('Latest guessed cell:', colored('RED', 'red', attrs=['underline']))
        print('Guessed cell:', colored('YELLOW', 'yellow', attrs=['bold']))
        print('Link endpoint:', colored('BLUE', 'blue'))
        print('Given cell:', colored('WHITE', 'white', attrs=['dark']))
        print('Cell is dead end:', colored('MAGENTA', 'magenta'))
        print('Calculated cell:', colored('GREEN', 'green'))

    def get_display_cell(self, cell):
        attributes = []
        cell_string = cell.candidates_string()
        # The last cell in the latest is the latest guessed cell
        if len(self.guessed_cells) > 0 and cell == self.guessed_cells[-1]:
            cell_color = 'red'
            attributes.append('underline')
        elif cell in self.guessed_cells:
            cell_color = 'yellow'
            attributes.append('bold')
        elif cell in self.given_cells:
            cell_color = 'white'
            attributes.append('dark')
        elif self.is_link_endpoint(cell):
            cell_color = 'blue'
        elif cell.is_empty() and self.empty_cell_is_a_dead_end_or_hole(cell):
            cell_color = 'magenta'
            cell_string = '**'
        else:
            cell_color = 'green'
        return colored(cell_string.center(self.get_display_cell_width()), cell_color, attrs=attributes)

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
        if (logging.getLogger().level == logging.DEBUG) or force_display or self.interactive_mode:
            print()
            print(self.get_display_header())
            print(self.get_horizontal_puzzle_boundary())

            for row_name in self.row_names:
                print(self.get_display_row(row_name))
            print(self.get_horizontal_puzzle_boundary())
            self.print_color_legend();
            print(f'The current puzzle count is {self.get_current_puzzle_count()}')
            print(f'Guesses are:')
            for guess in self.guessed_cells:
                print(f'     {guess}')
            print(f'Number of backtracks: {Grid_Puzzle.number_of_backtracks}')
            if Numbrix.interactive_mode:
                continue_interactive = input(
                    "\nPress enter to continue interactive mode. Press any other key and enter to exit interactive mode:\n>>> ")
                if len(continue_interactive) > 0:
                    Numbrix.interactive_mode = False

    def reduce_neighbors(self, cell):
        if cell.is_empty():
            return
        neighbors = self.get_cell_neighbors(cell)
        available_neighbor_values = self.get_available_neighbor_values(cell)
        open_neighbors = [neighbor for neighbor in neighbors if neighbor.is_empty()]
        if len(available_neighbor_values) == 1 and len(open_neighbors) == 1:
            open_neighbors[0].set_candidates(available_neighbor_values)

    def get_available_neighbor_values(self, cell):
        neighbors = self.get_cell_neighbors(cell)
        already_used_values = self.get_all_values()
        all_neighbor_values = flatten_and_de_dup([neighbor.candidates for neighbor in neighbors])
        return [neighbor_value for neighbor_value in self.get_required_neighbor_values(cell)
                if neighbor_value not in all_neighbor_values and neighbor_value not in already_used_values]

    def reduce(self):
        current_puzzle_size = self.get_current_puzzle_count()
        if self.is_solved():
            raise Exception('We should never get here. The puzzle is already solved or invalid')

        while True:
            for cell in self.get_all_cells():
                self.reduce_neighbors(cell)
            if self.is_solved():
                return

            self.fill_1_cell_gaps()

            updated_puzzle_size = self.get_current_puzzle_count()
            if self.is_solved() or current_puzzle_size == updated_puzzle_size:
                # Break out of the loop, since there was no change in the puzzle size
                return
            logging.debug(
                f"Reduced puzzle from {current_puzzle_size} cells solved to {updated_puzzle_size} cells solved")
            current_puzzle_size = updated_puzzle_size

    def is_link_endpoint(self, cell):
        """Return true if this is the end of a link and needs to be extended"""
        return len(self.get_available_neighbor_values(cell)) > 0

    def get_chain_endpoints(self):
        endpoints = []
        for cell in self.get_all_cells():
            if self.is_link_endpoint(cell):
                endpoints.append(cell)
        return endpoints

    def custom_reduce(self):
        self.fill_1_cell_gaps()

    def fill_1_cell_gaps(self):
        chain_endpoints = self.get_chain_endpoints()
        for cell in chain_endpoints:
            for other_cell in chain_endpoints:
                if cell.distance_to_cell(other_cell) == 2:
                    between_cells = self.get_empty_cells_between(cell, other_cell)
                    if len(between_cells) == 1:
                        between_cell = between_cells[0]
                        possible_value = None
                        if cell.get_value() - other_cell.get_value() == 2:
                            possible_value = other_cell.get_value() + 1
                        if other_cell.get_value() - cell.get_value() == 2:
                            possible_value = cell.get_value() + 1
                        if (possible_value is not None) and (possible_value not in set(self.get_all_values())):
                            between_cell.set_value(possible_value)
                            # Once one cell has been updated, we have to break out of this loop
                            # because our list of chain endpoints is no longer valid and our
                            # code assumes this to be so.
                            return

    def get_empty_cells_between(self, cell, other_cell):
        assert cell.distance_to_cell(other_cell) == 2
        between_cells = []
        if cell.get_row() > other_cell.get_row():
            between_cells.append(self.get_cell(cell.get_column() + str(cell.get_row_number() - 1)))
        if cell.get_row() < other_cell.get_row():
            between_cells.append(self.get_cell(cell.get_column() + str(cell.get_row_number() + 1)))
        if cell.get_column_number() > other_cell.get_column_number():
            between_cells.append(self.get_cell(chr(cell.get_column_number() - 2 + ord('A')) + cell.get_row()))
        if cell.get_column_number() < other_cell.get_column_number():
            between_cells.append(self.get_cell(chr(cell.get_column_number() + ord('A')) + cell.get_row()))
        return [cell for cell in between_cells if cell.is_empty()]

    def get_empty_neighbors(self, cell):
        return [neighbor for neighbor in self.get_cell_neighbors(cell) if neighbor.is_empty()]

    def get_neighbor_values(self, cell):
        return [neighbor.get_value() for neighbor in self.get_cell_neighbors(cell) if not neighbor.is_empty()]

    def calculate_required_neighbor_values_for_chain_endpoint(self, cell):
        # Possible neighbor values are the numbers higher and lower for this cell ONLY IF these values
        # haven't already been used.
        possible_neighbors_values = set([cell.get_value() - 1, cell.get_value() + 1])
        reduced_possible_neighbors_values = possible_neighbors_values - set(self.get_all_values())
        if possible_neighbors_values != reduced_possible_neighbors_values:
            logging.debug('Reducing already used neighbor values')
        return reduced_possible_neighbors_values

    def get_guessing_cell(self):
        """This returns a Chain_Endpoint object"""
        guess_candidates = []

        chain_endpoints = self.get_chain_endpoints()
        for cell in chain_endpoints:
            empty_neighbors = self.get_empty_neighbors(cell)
            required_neighbor_values = self.calculate_required_neighbor_values_for_chain_endpoint(cell)

            # Check that the required values aren't already used elsewhere in the puzzle (indicating an invalid guess)
            for required_value in required_neighbor_values:
                if required_value in self.get_all_values():
                    message = f"Invalid puzzle! Cell {cell} requires an empty neighbor to have value {required_neighbor_values}, but it is used elsewhere in the puzzle"
                    self.display()
                    raise Duplicate_Cell_Value_Exception(message)

            # Calculate the length of the chain. If the cell still requires two neighbor values, then it is an
            # unconnected cell, so the chain is of length 1
            chain_length = 1
            if len(required_neighbor_values) == 1:
                if list(required_neighbor_values)[0] > cell.get_value():
                    # If we require a cell higher than our value, then our chain must extend to lower numbers
                    direction = '-'
                else:
                    direction = '+'
                chain_length = self.get_chain_length(cell, 1, direction)

            smallest_difference = self.calculate_smallest_value_difference_to_other_chains(cell)
            guess_candidates.append(
                Chain_Endpoint(cell, empty_neighbors, required_neighbor_values, smallest_difference, chain_length))

        sorted_guesses = sort_chain_endpoints_for_guessing(guess_candidates)
        return sorted_guesses[0]

    def get_chain_length(self, cell_in_chain, current_length, direction):
        """This method calculates the length of a chain, giving one endpoint, the current length,
        and the direction (this argument is either '+' or '-') to go"""
        neighbors = self.get_cell_neighbors(cell_in_chain)
        neighbor_values = [cell.get_value() for cell in neighbors if not cell.is_empty()]
        next_value = eval(str(cell_in_chain.get_value()) + direction + "1")
        if next_value not in neighbor_values:
            return current_length

        next_cell_in_chain = [cell for cell in neighbors if cell.get_value() == next_value][0]
        return self.get_chain_length(next_cell_in_chain, current_length + 1, direction)

    def get_cell_with_value(self, a_value):
        for cell in self.get_all_cells():
            if cell.get_value() == a_value:
                return cell
        return None

    def get_all_values(self):
        values = []
        for cell in self.puzzle_dict.values():
            values.extend(cell.candidates)
        return values

    def calculate_smallest_value_difference_to_other_chains(self, cell_endpoint):
        minimum_difference = self.size * self.size + 1  # A number larger than the greatest distance possible
        for current_cell_endpoint in self.get_chain_endpoints():
            difference = abs(cell_endpoint.get_value() - current_cell_endpoint.get_value())
            if difference != 0 and difference < minimum_difference:
                minimum_difference = difference
        return minimum_difference

    def update_with_guess(self, _, current_guess):
        """The parameters here are from the another puzzle, so we need to make changes in our cells"""
        (cell_to_guess, value_to_guess) = current_guess
        my_cell = self.get_cell(cell_to_guess.address)
        my_cell.set_value(value_to_guess)
        self.guessed_cells.append(my_cell)

    def is_solved(self):
        # First, let's make sure the puzzle is consistent. Otherwise, it can't be solved.
        self.check_consistency()

        # Make sure that all cells are filled
        empty_cells = [cell for cell in self.get_all_cells() if cell.is_empty()]
        if len(empty_cells) > 0:
            return False

        # Check for each cell having just one candidate as a value
        all_values = self.get_all_values()
        if len(all_values) != self.size ** 2:
            return False

        # Check for all cells connected
        for cell in self.get_all_cells():
            if not self.cell_is_connected(cell):
                return False

        # Check for no chain endpoints
        if len(self.get_chain_endpoints()) > 0:
            return False

        return True

    def puzzle_has_repeated_values(self):
        all_values = self.get_all_values()
        counts = {}
        for curr_value in all_values:
            if curr_value in counts:
                counts[curr_value] = counts[curr_value] + 1
                logging.debug(f'Found duplicate value: {curr_value}')
            else:
                counts[curr_value] = 1

        if len(all_values) != len(set(all_values)):
            return True
        return False

    def puzzle_has_trapped_cells(self):
        for cell in self.get_all_cells():
            neighbors = self.get_cell_neighbors(cell)
            connected_neighbors = [neighbor for neighbor in neighbors if self.cell_is_connected(neighbor)]

            # If the cell is not connected (to its two chain links), but all its neighbors are connected,
            # then puzzle is invalid
            if not self.cell_is_connected(cell) and len(connected_neighbors) == len(neighbors):
                logging.debug(f'{cell} is trapped because it is not fully connected, but all its neighbors are.')
                return True
        return False

    def puzzle_has_dead_ends(self):
        empty_cells = [cell for cell in self.get_all_cells() if cell.is_empty()]
        for empty_cell in empty_cells:
            if self.empty_cell_is_a_dead_end_or_hole(empty_cell):
                logging.debug(f'Oops, we have a dead-end or hole at cell {empty_cell}')
                return True
        return False

    def cell_is_connected(self, cell):
        if cell.is_empty():
            return False

        neighbors = self.get_cell_neighbors(cell)
        required_neighbor_values = self.get_required_neighbor_values(cell)
        all_neighbor_values = flatten_and_de_dup([neighbor.candidates for neighbor in neighbors])
        for value in required_neighbor_values:
            if value not in all_neighbor_values:
                return False
        return True

    def get_required_neighbor_values(self, cell):
        if cell.is_empty():
            return []

        neighbor_values = []
        if cell.get_value() > 1:
            neighbor_value = cell.get_value() - 1
            neighbor_values.append(neighbor_value)
        if cell.get_value() < self.size ** 2:
            neighbor_value = cell.get_value() + 1
            neighbor_values.append(neighbor_value)
        return neighbor_values

    def empty_cell_is_a_dead_end_or_hole(self, empty_cell):
        connected_neighbors = [cell for cell in self.get_cell_neighbors(empty_cell) if self.cell_is_connected(cell)]
        open_neighbors = [cell for cell in self.get_cell_neighbors(empty_cell) if cell.is_empty()]

        # If the cell is empty, with only one open neighbor and all other neighbors are connected,
        # then it is a dead end or the end of the puzzle chain (1 or 81, for a 9x9 puzzle)
        if len(open_neighbors) == 1 and len(connected_neighbors) == 3 and not self.cell_can_contain_puzzle_end(empty_cell):
            logging.debug(
                f'{empty_cell} is empty with only one open neighbor ({open_neighbors}) and all other neighbors are connected ({connected_neighbors}) and this cannot be the end of the puzzle')
            return True

        # If the cell has no open neighbors, but all its cells are connected, then we have a hole.
        if len(connected_neighbors) == len(self.get_cell_neighbors(empty_cell)) and not self.cell_can_contain_puzzle_end(
                empty_cell):
            logging.debug(
                f'{empty_cell} has no open neighbors, but all its cells are connected, then we have a hole and this cannot be the end of the puzzle')
            return True
        return False

    def cell_can_contain_puzzle_end(self, candidate_empty_cell):
        cell_penultimate_endpoint_values = [2, self.size ** 2 - 1]
        neighbor_values = self.get_neighbor_values(candidate_empty_cell)
        contains_values = [cell in neighbor_values for cell in cell_penultimate_endpoint_values]
        return True in contains_values

    def puzzle_is_consistent(self):
        if self.puzzle_has_repeated_values():
            logging.debug("Oops, we must have guessed wrong because puzzle has repeated values")
            return False

        if self.puzzle_has_trapped_cells():
            logging.debug("Oops, we must have guessed wrong because puzzle has trapped cells")
            return False

        if self.puzzle_has_dead_ends():
            logging.debug("Oops, we must have guessed wrong because puzzle has deadends")
            return False

        return True

    def check_consistency(self):
        if not self.puzzle_is_consistent():
            logging.debug("Puzzle is inconsistent. Here's the state:")
            self.display()
            raise Inconsistent_Puzzle_Exception()
