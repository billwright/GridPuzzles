import logging
import copy

# See this page for coloring text in Python:
# https://blog.finxter.com/how-to-print-colored-text-in-python/#:~:text=The%20Most%20Pythonic%20way%20to,%3B5%3B4m%22)%20.
import simple_colors

from termcolor import colored

from GridPuzzle import GridPuzzle
from NumbrixCell import NumbrixCell
from Inconsistent_Puzzle_Exception import Inconsistent_Puzzle_Exception
from Duplicate_Cell_Value_Exception import Duplicate_Cell_Value_Exception
from Already_Solved_Exception import Already_Solved_Exception
from RoutesIsNoneException import RoutesIsNoneException
from grid_utils import flatten_and_de_dup, tuple_cross
from Path import Path

MAX_PATH_LENGTH_TO_SEARCH_FOR_ROUTES = 8


class Numbrix(GridPuzzle):
    debug_cell_count: int = 0
    number_of_guess_branches = 0
    number_of__guesses_in_each_branch = []
    maximum_guess_depth = 0
    maximum_guesses_available = 0

    @staticmethod
    def create_definition_from_string(string_definition):
        list_definition = []
        for cell_def in string_definition.split(','):
            if cell_def == '':
                list_definition.append(None)
            else:
                list_definition.append(int(cell_def))

        return list_definition

    def __init__(self, puzzle_definition, interactive=False, matching_message=None):
        self.last_cell_changed = None
        self.paths = []
        # This is the stack of (descriptive_text, list_of_guess_route_cells) tuples
        self.guessed_routes = []
        self.debug_matching_message = matching_message
        super().__init__(puzzle_definition, interactive)

    def __repr__(self):
        return f'Numbrix({id(self)}): count={self.get_current_puzzle_count()}'

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
                new_cell = NumbrixCell(address, candidates)
                if not new_cell.is_empty():
                    self.given_cells.append(new_cell)
                cell_dictionary[address] = new_cell
                cell_position_in_definition += 1
        if len(cell_dictionary) != len(self.definition):
            raise ValueError("Puzzle definition did not map correctly!")
        return cell_dictionary

    def set_cell_value(self, cell: NumbrixCell, new_value: int):
        """Sets the value of a cell, but also records the cell as the last cell changed.
        This is helpful in debugging and display of the puzzle."""
        self.last_cell_changed = cell
        cell.set_value(new_value)

    @staticmethod
    def print_color_legend():
        print('Given cell:', simple_colors.black('BLACK'))
        print('Latest cell updated:', simple_colors.red('RED', ['reverse']))
        print('Link endpoint:', simple_colors.blue('BLUE', ['reverse']))
        print('Guessed cell:', simple_colors.cyan('CYAN', ['underlined']))
        print('Cell is dead end:', simple_colors.magenta('MAGENTA'))
        print('Calculated cell:', simple_colors.green('GREEN'))

    def get_raw_display_cell(self, cell):
        cell_string = cell.candidates_string().center(self.get_display_cell_width())
        if cell.is_empty() and self.empty_cell_is_possible_final_cell(cell):
            return '++'.center(self.get_display_cell_width())
        elif cell.is_empty() and self.empty_cell_is_a_dead_end_or_hole(cell):
            return '**'.center(self.get_display_cell_width())

        return cell_string

    def get_display_cell(self, cell):
        cell_string = cell.candidates_string().center(self.get_display_cell_width())
        if cell is self.last_cell_changed:
            return simple_colors.red(cell_string, ['bold', 'bright', 'reverse'])
        elif self.is_link_endpoint(cell):
            return simple_colors.blue(cell_string, ['bold', 'bright', 'reverse'])
        elif cell in self.given_cells:
            return simple_colors.black(cell_string, ['bold', 'bright'])
        elif cell in self.get_all_guessed_cells():
            return simple_colors.cyan(cell_string, ['bold', 'bright', 'underlined'])
        elif cell.is_empty() and self.empty_cell_is_possible_final_cell(cell):
            return simple_colors.magenta('++'.center(self.get_display_cell_width()), ['bold', 'bright'])
        elif cell.is_empty() and self.empty_cell_is_a_dead_end_or_hole(cell):
            return simple_colors.magenta('**'.center(self.get_display_cell_width()), ['bold', 'bright'])

        return simple_colors.green(cell_string)

    def get_raw_display_row(self, row_name):
        """"Return a string representation of the specified row"""
        row_string = ''
        for col_name in self.column_names:
            cell_address = col_name + row_name
            cell = self.get_cell(cell_address)
            row_string += self.get_raw_display_cell(cell)
            row_string += '|'
        return row_name.rjust(3) + ' |' + row_string

    def get_display_row(self, row_name):
        """"Return a string representation of the specified row"""
        row_string = ''
        for col_name in self.column_names:
            cell_address = col_name + row_name
            cell = self.get_cell(cell_address)
            row_string += self.get_display_cell(cell)
            row_string += '|'
        return row_name.rjust(3) + ' |' + row_string

    def get_raw_display_string(self):
        puzzle_string = self.get_display_header() + '\n'
        puzzle_string += self.get_horizontal_puzzle_boundary() + '\n'
        for row_name in self.row_names:
            puzzle_string += self.get_raw_display_row(row_name) + '\n'
        puzzle_string += self.get_horizontal_puzzle_boundary() + '\n'
        return puzzle_string

    def display(self, force_display=False):
        if (logging.getLogger().level == logging.DEBUG) or force_display or self.interactive_mode:
            print()
            print(self.get_display_header())
            print(self.get_horizontal_puzzle_boundary())

            for row_name in self.row_names:
                print(self.get_display_row(row_name))
            print(self.get_horizontal_puzzle_boundary())
            print(f'The current puzzle count is {self.get_current_puzzle_count()}')
            print(f'Guessed routes are:')
            for (description, guessed_route) in self.guessed_routes:
                print(f'     Length {len(guessed_route)} ({description}): {guessed_route}')
            print(f'Guessed cells are:')
            for guess in self.guessed_cells:
                print(f'     {guess}')
            print(f'Number of guesses: {GridPuzzle.number_of_guesses}')
            print(f'Number of backtracks: {GridPuzzle.number_of_backtracks}')
            self.print_paths()
            self.print_color_legend()
            # if Numbrix.interactive_mode:
            #     continue_interactive = input(
            #         "\nPress enter to continue interactive mode. Press any other key and enter to exit interactive mode:\n>>> ")
            #     if len(continue_interactive) > 0:
            #         Numbrix.interactive_mode = False

    def display_as_code(self):
        code_string = '['
        for row_name in self.row_names:
            for col_name in self.column_names:
                cell_value = self.get_cell(col_name + row_name).get_value()
                code_string += f'{cell_value}, '
            code_string += '\n'
        print(code_string[0:-3] + ']')

    def reduce_neighbors(self, cell):
        if cell.is_empty():
            return
        neighbors = self.get_cell_neighbors(cell)
        available_neighbor_values = self.get_available_neighbor_values(cell)
        open_neighbors = [neighbor for neighbor in neighbors if neighbor.is_empty()]
        if len(available_neighbor_values) == 1 and len(open_neighbors) == 1:
            self.set_cell_value(open_neighbors[0], available_neighbor_values[0])
            # open_neighbors[0].set_candidates(available_neighbor_values)

    def get_available_neighbor_values(self, cell):
        neighbors = self.get_cell_neighbors(cell)
        already_used_values = self.get_all_values()
        all_neighbor_values = flatten_and_de_dup([neighbor.candidates for neighbor in neighbors])
        return [neighbor_value for neighbor_value in self.get_required_neighbor_values(cell)
                if neighbor_value not in all_neighbor_values and neighbor_value not in already_used_values]

    def debug_pause(self, message):
        if Numbrix.interactive_mode and \
                self.get_current_puzzle_count() != Numbrix.debug_cell_count and \
                (self.debug_matching_message is None or self.debug_matching_message in message):
            Numbrix.debug_cell_count = self.get_current_puzzle_count()
            self.display()
            continue_interactive = input(
                f"{message}\nPress enter to continue interactive mode. Press 'e' to exit interactive mode:\n>>> ")
            if len(continue_interactive) != 0:
                match continue_interactive:
                    case "b":
                        self.display()
                    case "l":
                        self.print_color_legend()
                    case "p":
                        self.print_paths()
                    case 'e':
                        Numbrix.interactive_mode = False
                        print('Exiting interactive mode')
                    case _:
                        print('Continuing in interactive mode')

    def populate_all_forced_cells(self):
        before_puzzle_size = self.get_current_puzzle_count()
        progress_made = True
        while not self.is_solved() and progress_made:
            for cell in self.get_all_cells():
                self.reduce_neighbors(cell)
                self.debug_pause('After reduce_neighbors')
            if self.get_current_puzzle_count() == before_puzzle_size:
                progress_made = False
            else:
                before_puzzle_size = self.get_current_puzzle_count()

    def reduce_forced_cells_only(self):
        if self.is_solved():
            raise Already_Solved_Exception('In reduced_forced_cell_only and puzzle is already solved. We should never get here. The puzzle is already solved or invalid')

        before_puzzle_size = self.get_current_puzzle_count()
        progress_made = True
        while not self.is_solved() and progress_made:
            self.populate_all_forced_cells()
            if self.get_current_puzzle_count() == before_puzzle_size:
                progress_made = False
            else:
                before_puzzle_size = self.get_current_puzzle_count()

    def reduce(self):
        if self.is_solved():
            raise Already_Solved_Exception('In reduce and puzzle is already solved. We should never get here. The puzzle is already solved or invalid')

        before_puzzle_size = self.get_current_puzzle_count()
        progress_made = True
        while not self.is_solved() and progress_made:
            # TODO: Leaving this here now, but I don't think I need this. I think path
            # solving is sufficient.
            self.populate_all_forced_cells()
            # self.reduce_paths_with_one_route_option()
            if self.get_current_puzzle_count() == before_puzzle_size:
                progress_made = False
            else:
                before_puzzle_size = self.get_current_puzzle_count()

    def generate_required_paths_with_routes(self):
        self.paths = self.generate_required_paths()
        for path in self.paths:
            self.generate_possible_routes_for_path(path)
        self.paths = Path.sort_by_least_routes(self.paths)
        self.verify_routes()
        return self.paths

    # Returns a new instance of Numbrix with the solved one-route paths
    def solve_one_path_routes(self, recursive_depth):
        starting_count = self.get_current_puzzle_count()
        new_puzzle = self.solve_next_one_route_path(recursive_depth)

        if not new_puzzle.is_consistent():
            print('Solving a one-route path in this puzzle caused it to become inconsistent')
            return self

        new_count = new_puzzle.get_current_puzzle_count()
        if new_count > starting_count:
            print(f'Before one-route path is solved puzzle (with recursive_depth of {recursive_depth}):')
            self.display()
            print(f'After one-route path is solved puzzle (with recursive_depth of {recursive_depth}):')
            new_puzzle.display()
            self.debug_pause(
                f'I found a puzzle with one-path solved. Above are the before and after. Now I am continuing with the after puzzle.  (with recursive_depth of {recursive_depth})')
            return new_puzzle.solve_one_path_routes(recursive_depth + 1)
        else:
            return new_puzzle

    def solve_next_one_route_path(self, recursive_depth):
        self.paths = self.generate_required_paths()
        if recursive_depth == 0:
            self.debug_pause(f'In solve_next_one_route_path with recursive_depth of {recursive_depth}')
        for path in self.paths:
            # If the path is too long, let's skip it for now, as it will generate too many routes
            # Hopefully we can reduce the length of this path by guessing shorter paths with fewer
            # routes.
            # This could cause the puzzle to never be solved if all the paths in a puzzle have a value
            # distance that is too long.
            if path.value_distance < MAX_PATH_LENGTH_TO_SEARCH_FOR_ROUTES or len(self.paths) == 1:
                if len(self.paths) == 1:
                    print(f'Only one path left: {path}')
                self.generate_possible_routes_for_path(path)
                self.verify_routes_for_path(path)

                try:
                    if path.has_just_one_route():
                        self.debug_pause(
                            f'Found a 1-route path({path}) and I am recursing on that puzzle now with recursive_depth of {recursive_depth}')
                        return path.get_first_route_puzzle().solve_next_one_route_path(recursive_depth + 1)
                except RoutesIsNoneException:
                    print(f'Routes is set to None for path {path}.')
                    print('Puzzle is in this state:')
                    self.display()
            else:
                try:
                    print(f'Skipping route generation for path {path} because of excessive value distance')
                except TypeError:
                    print(f'Got a TypeError...')

            # Check to make sure we have calculated routes for at least one path, regardless of length
            paths_with_routes = [path for path in self.paths if path.routes is not None]
            if len(paths_with_routes) == 0:
                # Then let's calculate the routes for the first path
                print(f'Generating routes for path {self.paths[0]} because we have no paths with routes')
                self.generate_possible_routes_for_path(self.paths[0])

        return self

    def print_paths(self):
        Path.print_path_info(self.paths)

    def sort_paths(self):
        self.paths = Path.sort_by_least_routes(self.paths)

    def search(self):
        """Using depth-first search to solve the puzzle.
        This method returns either the solved puzzle or None"""
        logging.debug("State of the puzzle before reduce:")
        self.display()

        # Solve as much as we can with simple forcing of cells and paths
        # This code, which just fills in forced cells, is not required to solve
        # puzzles, but for the very hard puzzle it made a huge difference. Without
        # the reduce call (just this one line), the puzzle was solved with 3117
        # backtracks. With it, the puzzled was solved with just 27 backtracks.
        self.reduce()

        current_puzzle_size = self.get_current_puzzle_count()
        logging.debug(f"Checking for a solved puzzle. The current count is {current_puzzle_size}")

        if self.is_solved():
            print("Puzzle is solved after reduce!")
            return self

        # Log puzzle size for plotting later
        logging.info(current_puzzle_size)

        # Let's generate a puzzle with all the one-route paths solved.
        self.debug_pause('Moving on to path generation and solving...')
        puzzle_with_one_route_paths_solved = self.solve_one_path_routes(0)

        if puzzle_with_one_route_paths_solved.is_solved():
            print("Puzzle is solved after one-route paths!")
            return puzzle_with_one_route_paths_solved

        puzzle_with_one_route_paths_solved.sort_paths()
        puzzle_with_one_route_paths_solved.display()

        logging.debug("State of the puzzle before selecting route to guess:")
        if len(puzzle_with_one_route_paths_solved.paths) == 0:
            # if number of paths is zero, so we have a puzzle that is missing the end values.
            # So, we need to create a path so that we can continue. We'll first create a complete list of
            # guesses to iterate over. A guess is a tuple of a cell and a value
            guesses = puzzle_with_one_route_paths_solved.generate_guesses_for_final_cells()
            for (guessed_cell, guessed_end_value) in guesses:
                GridPuzzle.number_of_guesses += 1
                puzzle_with_guess = copy.deepcopy(puzzle_with_one_route_paths_solved)
                final_cell = puzzle_with_guess.get_cell(guessed_cell.address)
                puzzle_with_guess.set_cell_value(final_cell, guessed_end_value)
                puzzle_with_guess.guessed_cells.append(final_cell)
                try:
                    solved_puzzle = puzzle_with_guess.search()
                    if solved_puzzle is not None:
                        return solved_puzzle
                    else:
                        logging.debug(
                            f'Our guess of {guessed_end_value} for cell {guessed_cell} was wrong.')
                except Inconsistent_Puzzle_Exception:
                    logging.debug(
                        "Puzzle became inconsistent. Must have been an incorrect guess. Trying a different one...")

        if len(puzzle_with_one_route_paths_solved.paths) == 0:
            print('We should never be here, unless the puzzle is solved...I should check for that. Here is the puzzle:')
            if puzzle_with_one_route_paths_solved.is_solved():
                return None

            puzzle_with_one_route_paths_solved.display_as_code()
            puzzle_with_one_route_paths_solved.display()
            raise Inconsistent_Puzzle_Exception

        path_to_guess = puzzle_with_one_route_paths_solved.paths[0]
        if path_to_guess.routes is None:
            print(f'There are no routes for the first path: {path_to_guess} to guess!')
            puzzle_with_one_route_paths_solved.display()
            return None

        # Since the paths are sorted in order of the least amount of routes,
        # we start with the first path and iterate over the choices there,
        # which are populated Numbrix instances.
        for index, (puzzle_with_guess, route_guess) in enumerate(path_to_guess.routes, start=1):
            GridPuzzle.number_of_guesses += 1
            puzzle_with_guess.guessed_routes.append((f'{index} out of {path_to_guess.num_routes()}', route_guess))
            logging.debug(
                f"I'm guessing route: {route_guess} ({index} out of {path_to_guess.num_routes()} possible guesses)")
            GridPuzzle.number_of_guesses += 1

            # Check that our guess is consistent, otherwise, let's continue to a different guess
            if not puzzle_with_guess.is_consistent():
                logging.debug("Current guess is inconsistent, so moving on to the next guess...")
                puzzle_with_one_route_paths_solved.display()
                # Move on to the next guess -- this jumps back to the start of this for loop
                continue

            # Next, check if the guessed puzzle is already solved
            if puzzle_with_guess.is_solved():
                return puzzle_with_guess

            # Here's the tricky part, recursively call this same method, but we're calling it on a different object
            # Note that this is NOT self.search(), but puzzle_with_guess.search().
            try:
                solved_puzzle = puzzle_with_guess.search()
                if solved_puzzle is not None:
                    return solved_puzzle
                else:
                    logging.debug(
                        f'Our guess of {route_guess} for Path {path_to_guess} was wrong.')
            except Inconsistent_Puzzle_Exception:
                logging.debug(
                    "Puzzle became inconsistent. Must have been an incorrect guess. Trying a different one...")
            except Duplicate_Cell_Value_Exception as error:
                logging.debug(error.message)

        logging.debug(f"Could not find a solution when guessing route for Path {path_to_guess}. Backing up...")
        puzzle_with_one_route_paths_solved.display()
        GridPuzzle.number_of_backtracks += 1
        return None

    def generate_guesses_for_final_cells(self):
        extended_holes = self.get_extended_holes()
        available_ending_values = self.get_remaining_well_bottoms_values()
        if len(extended_holes) != len(available_ending_values):
            # TODO: Shouldn't have called this method. Check for invalid earlier
            print('Puzzle is invalid. Back-up.')
            return []

        # Check if we have the matching number of well bottoms
        well_bottoms = self.get_final_cells()
        print('well bottoms:', well_bottoms)

        # This might not be a valid assertion. If failed for this puzzle state,
        # which is a wrong puzzle, but G5 is a well bottom, but not recognized
        # as such with my current code. So, just not checking this for now.
        #     |  A  |  B  |  C  |  D  |  E  |  F  |  G  |  H  |  I  |
        # ----‖=====‖=====‖=====‖=====‖=====‖=====‖=====‖=====‖=====‖
        #   1 |  59 |  58 |  57 |  56 |  53 |  52 |  49 |  48 |  47 |
        #   2 |  60 |  63 |  64 |  55 |  54 |  51 |  50 |  45 |  46 |
        #   3 |  61 |  62 |  65 |  66 |  41 |  42 |  43 |  44 |     |
        #   4 |  70 |  69 |  68 |  67 |  40 |  39 |     |     |     |
        #   5 |  71 |  72 |  73 |     |  ++ |  38 |     |  2  |  3  |
        #   6 |  30 |  31 |     |     |  36 |  37 |  14 |  13 |  4  |
        #   7 |  29 |  32 |  33 |  34 |  35 |  16 |  15 |  12 |  5  |
        #   8 |  28 |  25 |  24 |  21 |  20 |  17 |  10 |  11 |  6  |
        #   9 |  27 |  26 |  23 |  22 |  19 |  18 |  9  |  8  |  7  |
        # ----‖=====‖=====‖=====‖=====‖=====‖=====‖=====‖=====‖=====‖
        # assert len(well_bottoms) == len(available_ending_values)

        if len(well_bottoms) == 0:
            print('I did not find any well bottoms, so using all the cells in the first hole')
            well_bottoms = extended_holes[0]
        return tuple_cross(well_bottoms, available_ending_values)

    def is_link_endpoint(self, cell):
        """Return true if this is the end of a link and needs to be extended"""
        available_neighbor_values = self.get_available_neighbor_values(cell)
        return len(available_neighbor_values) > 0

    def get_chain_endpoints(self):
        """Chains are an ordered list of cells that are connected via their values. The
        endpoints of these chains are the cells that are only connected by one value and
        so mark the ends of the chains."""
        endpoints = []
        for cell in self.get_all_cells():
            if self.is_link_endpoint(cell):
                endpoints.append(cell)
        endpoints.sort(key=lambda x: x.get_value())
        return endpoints

    def generate_required_paths(self):
        endpoints = self.get_chain_endpoints()
        print('Sorted endpoints are:', endpoints)

        self.paths = []
        for index, endpoint in enumerate(endpoints[0:-1]):
            # Determine if this endpoint can be a starting point by checking if it isn't already
            # connected to the next higher value
            if endpoint.get_value() + 1 not in self.get_neighbor_values(endpoint):
                new_path = Path(endpoint, endpoints[index + 1])
                self.paths.append(new_path)
        self.paths.sort(key=lambda x: x.value_distance)
        return self.paths

    # I don't think I need this special case any longer...
    # def reduce_paths_with_one_route_option(self):
    #     self.paths = self.generate_required_paths()
    #     for path in self.paths:
    #         routes = self.generate_possible_routes_for_path(path)
    #         if len(routes) == 1:
    #             # Populate cells in this puzzle (but not start and finish, since they are already set)
    #             for cell in routes[0][1:-1]:
    #                 self.get_cell(cell.address).set_value(cell.get_value())

    # Well bottoms are cells that will be a dead-end. Wells can only have the value of 1 and the
    # max number of the puzzle (81 for a 9x9 puzzle). A well bottom is an open cell with fully-connected
    # neighbors, save for one open neighbor. This means that putting a value in the well bottom will
    # not connect to any populated neighbor. Here's an example:
    #
    #     |  A  |  B  |  C  |  D  |  E  |  F  |
    # ----‖=====‖=====‖=====‖=====‖=====‖=====‖
    #   1 |  19 |  20 |  25 |  26 |  27 |  28 |
    #   2 |  18 |  21 |  24 |  35 |  36 |  29 |
    #   3 |  17 |  22 |  23 |  34 |  33 |  30 |
    #   4 |  16 |  15 |  8  |  7  |  32 |  31 |
    #   5 |  13 |  14 |  9  |  6  |  5  |     |
    #   6 |  12 |  11 |  10 |     |     |     |
    # ----‖=====‖=====‖=====‖=====‖=====‖=====‖
    #
    # D6 is the well bottom. F5 is not a well bottom because it has a neighbor (E5) that is not
    # fully connected, as it needs to be connected to a cell with a 4 in it. The code here is to be
    # used to find the well bottom and populate it with a 1 or max value. At that point, we can then
    # create a path and fill it in. Paths, by definition in this program, go from one populated cell
    # to another. Hence, the need to populate the well bottoms.
    def get_well_bottoms(self):
        well_bottoms = []
        for possible_well_bottom in self.get_all_empty_cells():
            all_neighbors = self.get_cell_neighbors(possible_well_bottom)
            connected_neighbors = [cell for cell in all_neighbors if self.cell_is_connected(cell)]
            open_neighbors = [cell for cell in all_neighbors if cell.is_empty()]

            # If we have only one open neighbor and all other neighbors are already connected or all but
            # one other neighbor is full connected, then we are a well bottom
            if len(open_neighbors) == 1 and (len(connected_neighbors) >= len(all_neighbors) - 2):
                well_bottoms.append(possible_well_bottom)

        for cell in well_bottoms:
            print(f'{cell} is a well bottom')

        return well_bottoms

    def get_remaining_well_bottoms_values(self):
        return [x for x in [1, self.size * self.size] if x not in self.get_all_values()]

    def get_all_empty_cells(self):
        return [cell for cell in self.get_all_cells() if cell.is_empty()]

    def verify_routes(self):
        # Check to make sure every puzzle associated with a route has more
        # solved cells than the current puzzle. Otherwise, there is no point.
        for path in self.paths:
            self.verify_routes_for_path(path)

    def verify_routes_for_path(self, path):
        current_count = self.get_current_puzzle_count()
        if path.routes is not None:
            for route in path.routes:
                count_difference = route[0].get_current_puzzle_count() - current_count
                if count_difference != (path.value_distance - 1):
                    print(
                        f'Found invalid (puzzle,route) tuple for path {path}. Count increase is only {count_difference}')
                assert count_difference == (path.value_distance - 1)

    # This method always returns a list of (puzzle, route) tuples. The puzzle is a possibly deep-copied
    # instance Numbrix that contains the populated, generated route. The route is the second element in
    # the tuple and only used for reporting.
    def generate_possible_routes_for_path(self, path):
        # Test whether the path is already connected. If so, return the route
        # TODO: Is it possible to do this test BEFORE the recursion? Instead of check for a connected
        # path, maybe check for a 1-cell gap?
        if path.is_already_connected():
            # logging.debug('This path is already connected')
            # Remember, this method returns a list of tuples, so here we return a list that contains just
            # one tuples, which has the puzzle (self) and the list of two cells
            new_routes = [(self, [path.start, path.end])]
            path.set_routes(new_routes)
            self.verify_routes_for_path(path)
            return new_routes

        # Test whether it is possible to get from one cell to the other
        if not path.is_possible():
            # logging.debug('This path is not possible')
            return None

        # 2. Start from start cell and iterate over all open neighbors
        routes = []
        for cell in self.get_empty_neighbors(path.start):
            # Before we set any values in our numbrix puzzle, we need to make a copy so
            # that we don't alter the original puzzle, as we aren't sure what route to take, as yet.
            puzzle_with_guess = copy.deepcopy(self)
            puzzle_with_guess.paths = []
            # Create new path with new cells from our copy
            new_start = puzzle_with_guess.get_cell(cell.address)
            puzzle_with_guess.set_cell_value(new_start, path.start.get_value() + 1)
            new_end = puzzle_with_guess.get_cell(path.end.address)

            # Here we create our new, shorter path in our copied puzzle. This path starts one
            # cell away from the path passed into this method and ends on the same cell, though
            # in our copied puzzle.
            shorter_path = Path(new_start, new_end)

            # We make our recursive call to find the shorter paths
            shorter_routes = puzzle_with_guess.generate_possible_routes_for_path(shorter_path)

            # If a path was found for the shorter path, then we tack on our starting cell
            # and add it to the list of possible routes.
            if shorter_routes is not None:
                for (more_solved_puzzle, shorter_route) in shorter_routes:
                    shorter_route.insert(0, path.start)

                    # Append the (puzzle, route) tuple to our list of routes
                    routes.append((more_solved_puzzle, shorter_route))

        path.set_routes(routes)
        return routes

    def get_empty_neighbors(self, cell):
        return [neighbor for neighbor in self.get_cell_neighbors(cell) if neighbor.is_empty()]

    def get_neighbor_values(self, cell):
        return [neighbor.get_value() for neighbor in self.get_cell_neighbors(cell) if not neighbor.is_empty()]

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

    def empty_cell_is_possible_final_cell(self, possible_final_cell):
        connected_neighbors = [cell for cell in self.get_cell_neighbors(possible_final_cell) if
                               self.cell_is_connected(cell)]
        open_neighbors = [cell for cell in self.get_cell_neighbors(possible_final_cell) if cell.is_empty()]

        # If the cell is empty, with only one open neighbor and all other neighbors are connected,
        # then it is a possible end of the puzzle chain (1 or 81, for a 9x9 puzzle)
        return len(open_neighbors) == 1 and len(connected_neighbors) == 3 and self.cell_can_contain_puzzle_end()

    def get_final_cells(self):
        return [cell for cell in self.get_all_empty_cells() if self.empty_cell_is_possible_final_cell(cell)]
        # Equivalent code without comprehension:
        # final_cells = []
        # for cell in self.get_all_empty_cells():
        #     if self.empty_cell_is_possible_final_cell(cell):
        #         final_cells.append(cell)
        # return final_cells

    def guess_final_cells(self):
        self.generate_required_paths()
        assert len(self.paths) == 0

        extended_holes = self.get_extended_holes()
        available_ending_values = self.get_remaining_well_bottoms_values()
        assert len(extended_holes) == len(available_ending_values)

        # Check if we have the matching number of well bottoms
        well_bottoms = self.get_final_cells()
        print('well bottoms:', well_bottoms)
        assert len(well_bottoms) == len(available_ending_values)

        # Now we'll guess and check
        for possible_end_cell in well_bottoms:
            for possible_end_value in available_ending_values:
                new_puzzle = copy.deepcopy(self)
                end_cell = new_puzzle.get_cell(possible_end_cell.address)
                new_puzzle.set_cell_value(end_cell, possible_end_value)

                new_puzzle.generate_required_paths()
                if len(new_puzzle.paths) == 1:
                    new_routes = new_puzzle.generate_possible_routes_for_path(new_puzzle.paths[0])
                    print('new routes:', new_routes)
                    if new_routes is not None and len(new_routes) > 0:
                        print('Found one!')

    def empty_cell_is_a_dead_end_or_hole(self, empty_cell):
        connected_neighbors = [cell for cell in self.get_cell_neighbors(empty_cell) if self.cell_is_connected(cell)]
        open_neighbors = [cell for cell in self.get_cell_neighbors(empty_cell) if cell.is_empty()]

        # If the cell is empty, with only one open neighbor and all other neighbors are connected,
        # then it is a dead end or the end of the puzzle chain (1 or 81, for a 9x9 puzzle)
        if len(open_neighbors) == 1 and len(connected_neighbors) == 3 and not self.cell_can_contain_puzzle_end():
            logging.debug(
                f'{empty_cell} is empty with only one open neighbor ({open_neighbors}) and all other neighbors are connected ({connected_neighbors}) and this cannot be the end of the puzzle')
            return True

        return self.empty_cell_is_hole(empty_cell)

    def empty_cell_is_hole(self, empty_cell):
        connected_neighbors = [cell for cell in self.get_cell_neighbors(empty_cell) if self.cell_is_connected(cell)]
        # If the cell has no open neighbors, but all its cells are connected, then we have a hole.
        if len(connected_neighbors) == len(
                self.get_cell_neighbors(empty_cell)) and not self.cell_can_contain_puzzle_end():
            logging.debug(
                f'{empty_cell} has no open neighbors, but all its cells are connected, then we have a hole and this cannot be the end of the puzzle')
            return True
        return False

    def get_holes(self):
        return [cell for cell in self.get_all_empty_cells() if self.empty_cell_is_hole(cell)]

    def get_extended_holes(self):
        """Extended holes are connected empty cells. They don't necessarily have to have all
    # connected neighbors."""
        extended_holes = []
        for cell in self.get_all_empty_cells():
            all_hole_cells_found = [empty_cell for extended_hole in extended_holes for empty_cell in extended_hole]
            if cell not in all_hole_cells_found:
                extended_hole = self.get_all_connected_empty_cells(cell, set())
                extended_holes.append(extended_hole)
        return extended_holes

    def get_all_connected_empty_cells(self, cell, empty_cell_set=None):
        if empty_cell_set is None:
            empty_cell_set = set()
        if cell not in empty_cell_set:
            empty_cell_set.add(cell)
            for empty_neighbor in self.get_empty_neighbors(cell):
                self.get_all_connected_empty_cells(empty_neighbor, empty_cell_set)
        return empty_cell_set

    def cell_can_contain_puzzle_end(self):
        return len(self.get_remaining_well_bottoms_values()) > 0
        # cell_penultimate_endpoint_values = [2, self.size ** 2 - 1]
        # neighbor_values = self.get_neighbor_values(candidate_empty_cell)
        # contains_values = [cell in neighbor_values for cell in cell_penultimate_endpoint_values]
        # return True in contains_values

    def is_consistent(self):
        if self.puzzle_has_repeated_values():
            logging.debug("Oops, we must have guessed wrong because puzzle has repeated values")
            return False

        if self.puzzle_has_trapped_cells():
            logging.debug("Oops, we must have guessed wrong because puzzle has trapped cells")
            return False

        if self.puzzle_has_dead_ends():
            logging.debug("Oops, we must have guessed wrong because puzzle has dead-ends")
            return False

        return True

    def check_consistency(self):
        if not self.is_consistent():
            logging.debug("Puzzle is inconsistent. Here's the state:")
            self.display()
            raise Inconsistent_Puzzle_Exception()

    def get_all_guessed_cells(self):
        guessed_cells = self.guessed_cells.copy()
        for (_, route_cells) in self.guessed_routes:
            guessed_cells += route_cells
        return guessed_cells
