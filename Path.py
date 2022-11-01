import logging

from NumbrixCell import NumbrixCell
from RoutesIsNoneException import RoutesIsNoneException


# A Path is one possible path between two cells. Two cells might only have one possible
# path between them, but they might have many. For example, take this puzzle:
#
#     |  A  |  B  |  C  |  D  |  E  |  F  |  G  |  H  |  I  |
# ----‖=====‖=====‖=====‖=====‖=====‖=====‖=====‖=====‖=====‖
#   1 |  3  |  4  |  9  |     |  17 |     |  21 |  22 |  23 |
#   2 |  2  |  5  |     |     |     |     |     |  25 |  24 |
#   3 |  1  |     |     |     |     |     |     |  26 |  27 |
#   4 |  58 |  57 |     |     |     |     |     |  29 |  28 |
#   5 |  59 |  60 |     |     |     |     |     |     |  43 |
#   6 |  62 |  61 |     |     |     |     |     |     |     |
#   7 |  63 |  64 |     |     |     |     |     |     |  81 |
#   8 |  66 |  65 |     |     |     |     |     |     |  80 |
#   9 |  67 |  68 |  69 |     |  73 |     |  77 |  78 |  79 |
# ----‖=====‖=====‖=====‖=====‖=====‖=====‖=====‖=====‖=====‖
#
# There are two paths between cell B2 and cell C1:
#       - B3(6) -> C3(7) -> C2(8)
#       - C2(6) -> D2(7) -> D1(8)   (this is invalid, though, as it forms a hole)

# Paths always start with the lower value and end on the higher value


class Path:

    @staticmethod
    def print_path_info(paths):
        print("Path           Value Distance   # of Routes")
        print("-------------------------------------------")
        for path in paths:
            num_routes = 'NA'
            if path.routes is not None:
                num_routes = len(path.routes)
            print(f'{path}    {path.value_distance}               {num_routes}')

    @staticmethod
    def sort_by_least_routes(paths):
        path_with_routes = [path for path in paths if path.routes is not None]
        path_with_routes_set_to_none = [path for path in paths if path.routes is None]
        path_with_routes.sort(key=lambda x: (len(x.routes), -x.value_distance))
        path_with_routes_set_to_none.sort(key=lambda x: x.value_distance)

        return path_with_routes + path_with_routes_set_to_none

    def __init__(self, start_cell, end_cell, list_of_routes=None):
        self.start = start_cell
        self.end = end_cell
        self.value_distance = abs(self.start.get_value() - self.end.get_value())
        self.minimum_address_distance = self.start.min_address_distance_to_cell(self.end)
        assert self.start.get_value() < self.end.get_value()
        self.routes = list_of_routes

    def __repr__(self):
        return f'Path:{self.value_distance}({self.start.address}->{self.end.address})-{self.num_routes_string()}'

    # def value_distance(self):
    #     return abs(self.start.get_value() - self.end.get_value())
    #
    # def minimum_address_distance(self):
    #     return self.start.min_address_distance_to_cell(self.end)

    def is_already_connected(self):
        return self.value_distance == 1 and self.minimum_address_distance == 1

    #     |  A  |  B  |  C  |  D  |
    # ----‖=====‖=====‖=====‖=====‖
    #   1 |  3  |     |  4  |     |
    #   2 |  2  |  1  |     |     |
    # In the above puzzle the path from 3 to 4 is not possible because
    # the value distance is 1, but the minimum address distance is 2.
    def is_possible(self):
        return self.value_distance >= self.minimum_address_distance

    def set_routes(self, list_of_routes):
        if list_of_routes is None:
            raise Exception('Setting routes to None')
        self.routes = list_of_routes

    def num_routes(self):
        if self.routes is None:
            raise RoutesIsNoneException('Routes is None')
        # Routes are tuples: (puzzle, [list of cells])
        return len(self.routes)

    def num_routes_string(self):
        if self.routes is None:
            return 'NA'
        else:
            return str(len(self.routes))

    # Returns the puzzle containing the first route populated
    def get_first_route_puzzle(self):
        return self.routes[0][0]

    def get_first_route(self):
        return self.routes[0][1]

    def has_just_one_route(self):
        return self.routes is not None and self.num_routes() == 1
