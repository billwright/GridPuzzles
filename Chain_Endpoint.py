from Numbrix_Cell import Numbrix_Cell
from grid_utils import tuple_cross


class Chain_Endpoint(object):

    def __init__(self, endpoint_cell, open_neighbors, required_neighbor_value, value_difference_to_another_chain, chain_length):
        self.endpoint = endpoint_cell
        self.open_neighbors = open_neighbors
        self.required_neighbor_values = required_neighbor_value
        self.value_difference_to_another_chain = value_difference_to_another_chain
        self.chain_length = chain_length

    def __len__(self):
        return len(self.open_neighbors)

    def __repr__(self):
        return f"Chain({self.endpoint}); " + \
               f"distance={self.value_difference_to_another_chain}, " + \
               f"len:{self.chain_length}, " + \
               f"required neighbor values= {self.required_neighbor_values}, " + \
               f"open neighbors={self.open_neighbors}"

    def __eq__(self, other):
        return self.endpoint.address == other.endpoint.address and \
               self.required_neighbor_values == other.required_neighbor_values and \
               self.value_difference_to_another_chain == other.value_difference_to_another_chain

    def get_guesses(self):
        return tuple_cross(self.open_neighbors, self.required_neighbor_values)
