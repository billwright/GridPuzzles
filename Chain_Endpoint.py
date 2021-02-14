from Numbrix_Cell import Numbrix_Cell
from grid_utils import tuple_cross


class Chain_Endpoint(object):

    def __init__(self, endpoint_cell, open_neighbors, required_neighbor_value, value_difference_to_another_chain):
        self.endpoint = endpoint_cell
        self.open_neighbors = open_neighbors
        self.required_neighbor_values = required_neighbor_value
        self.value_difference_to_another_chain = value_difference_to_another_chain

    def __len__(self):
        return len(self.open_neighbors)

    def __repr__(self):
        return f"Chain Endpoint({self.endpoint}); open neighbors={self.open_neighbors}, " + \
               f"required neighbor values= {self.required_neighbor_values}, distance={self.value_difference_to_another_chain}"

    def __eq__(self, other):
        return self.endpoint.address == other.endpoint.address and \
               self.required_neighbor_values == other.required_neighbor_values and \
               self.value_difference_to_another_chain == other.value_difference_to_another_chain

    def get_guesses(self):
        return tuple_cross(self.open_neighbors, self.required_neighbor_values)
