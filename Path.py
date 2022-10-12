import logging

from Numbrix_Cell import Numbrix_Cell

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

    def __init__(self, start_cell, end_cell, list_of_routes=[]):
        self.start = start_cell
        self.end = end_cell
        self.value_distance = abs(self.start.get_value() - self.end.get_value())
        self.minimum_address_distance = self.start.min_address_distance_to_cell(self.end)
        assert self.start.get_value() < self.end.get_value()
        self.routes = list_of_routes

    def __repr__(self):
        return f'Path:{self.value_distance}({self.start.address}->{self.end.address})'

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
        self.routes = list_of_routes
