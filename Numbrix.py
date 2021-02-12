from Grid_Puzzle import Grid_Puzzle
from Numbrix_Cell import Numbrix_Cell
from termcolor import colored

import logging

logging.basicConfig(format='%(message)s', filename='grid-puzzle.log', filemode='w', level=logging.INFO)

# TODO: Create Reducing_Grid_Puzzle subclass, of which this is NOT one
# There are no groups to reduce in this puzzle, but there is reducing. But we do have a grid and we do want to search recursively, if we have to


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
                cell_dictionary[address] = Numbrix_Cell(address, candidates)
                cell_position_in_definition += 1
        if len(cell_dictionary) != len(self.definition):
            raise ValueError("Puzzle definition did not map correctly!")
        return cell_dictionary

    def get_display_row(self, row_name):
        row_string = ''
        for col_name in self.column_names:
            cell_address = col_name + row_name
            cell = self.get_cell(cell_address)
            cell_color = 'green'
            if cell.is_link_endpoint(self.get_cell_neighbors(cell)):
                cell_color = 'blue'
            row_string += colored(cell.candidates_string().center(self.get_display_cell_width()), cell_color)
            row_string += '|'
        return row_name.rjust(3) + ' |' + row_string

    def display(self):
        print()
        print(self.get_display_header())
        print(self.get_horizontal_puzzle_boundary())

        for row_name in self.row_names:
            print(self.get_display_row(row_name))
        print(self.get_horizontal_puzzle_boundary())

    def reduce(self):
        current_puzzle_size = self.get_current_puzzle_count()
        logging.info(current_puzzle_size)
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
            logging.debug(f"Reduced puzzle from {current_puzzle_size} down to {updated_puzzle_size}")
            current_puzzle_size = updated_puzzle_size

    def get_chain_endpoints(self):
        endpoints = []
        for cell in self.get_all_cells():
            if cell.is_link_endpoint(self.get_cell_neighbors(cell)):
                endpoints.append(cell)
        return endpoints

    def fill_1_cell_gaps(self):
        chain_endpoints = self.get_chain_endpoints()
        for cell in chain_endpoints:
            for other_cell in chain_endpoints:
                if cell.distance_to_cell(other_cell) == 2:
                    between_cell = self.get_cell_between(cell, other_cell)
                    if cell.get_value() - other_cell.get_value() > 0:
                        between_cell.set_value(other_cell.get_value() + 1)
                    else:
                        between_cell.set_value(cell.get_value() + 1)
                    # Once one cell has been updated, we have to break out of this loop
                    # because our list of chain endpoints is no longer valid and our
                    # code assumes this to be so.
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

    def get_guessing_cell(self):
        chain_endpoints = self.get_chain_endpoints()
        guessing_cell = chain_endpoints[0]
        # It might be handy to have a Chain_Endpoint_Cell, which has additional information like it's neighbor cells,
        # shortest gap to other chains, value to put in neighbor cells.