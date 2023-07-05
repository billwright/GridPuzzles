from Path import Path
from Numbrix import Numbrix


def generate_possible_routes_for_path(numbrix, path):
    """This method always returns a list of (puzzle, route) tuples. The puzzle is a deep-copied
       instance of Numbrix that contains the populated route. The route is the second element in
       the tuple and only used for reporting."""

    if path.is_already_connected():
        # Remember, this method returns a list of tuples, so here we return a list that contains just
        # one tuples, which has the puzzle (self) and the list of two cells
        new_routes = [(numbrix, [path.start, path.end])]
        path.set_routes(new_routes)
        # self.verify_routes_for_path(path)
        yield new_routes

    # Test whether it is possible to get from one cell to the other
    if not path.is_possible():
        # logging.debug('This path is not possible')
        return None

    # Start from start cell and iterate over all open neighbors
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