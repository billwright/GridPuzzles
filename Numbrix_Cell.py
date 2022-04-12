from Cell import Cell
from Blanking_Cell_Exception import Blanking_Cell_Exception
from grid_utils import flatten_and_de_dup


class Numbrix_Cell(Cell):

    def __init__(self, cell_address, candidates):
        self._candidates = []
        super().__init__(cell_address, candidates)

    def set_candidates(self, new_candidates):
        try:
            super().set_candidates(new_candidates)
        except Blanking_Cell_Exception:
            # Do nothing. This is okay for this subclass
            pass

    def get_value(self):
        if self.is_empty():
            return None
        else:
            return self._candidates[0]

    def set_value(self, value):
        if self.is_empty():
            self._candidates = [value]
        else:
            raise ValueError("Trying to set an already set cell!")

    def candidates_string(self):
        if len(self.candidates) == 1 and self.candidates[0] is None:
            return ''
        return ','.join([str(candidate) for candidate in self.candidates])

    def is_empty(self):
        return not self._candidates

    def is_connected(self, neighbors):
        if self.is_empty():
            return False
        required_neighbor_values = self.get_required_neighbor_values()
        all_neighbor_values = flatten_and_de_dup([neighbor.candidates for neighbor in neighbors])
        for value in required_neighbor_values:
            if value not in all_neighbor_values:
                return False
        return True

    def reduce_neighbors(self, neighbors, already_used_values):
        if self.is_empty():
            return

        available_neighbor_values = self.get_available_neighbor_values(neighbors, already_used_values)
        open_neighbors = [neighbor for neighbor in neighbors if neighbor.is_empty()]
        if len(available_neighbor_values) == 1 and len(open_neighbors) == 1:
            open_neighbors[0].set_candidates(available_neighbor_values)

    def get_available_neighbor_values(self, neighbors, already_used_values):
        all_neighbor_values = flatten_and_de_dup([neighbor.candidates for neighbor in neighbors])
        return [neighbor_value for neighbor_value in self.get_required_neighbor_values()
                if neighbor_value not in all_neighbor_values and neighbor_value not in already_used_values]

    def get_required_neighbor_values(self):
        if self.is_empty():
            return []

        neighbor_values = []
        if self.get_value() > 1:
            neighbor_value = self.get_value() - 1
            neighbor_values.append(neighbor_value)
        if self.get_value() < self.get_size() ** 2:
            neighbor_value = self.get_value() + 1
            neighbor_values.append(neighbor_value)
        return neighbor_values

    def is_link_endpoint(self, neighbors, already_used_values):
        """Return true if this is the end of a link and needs to be extended"""
        return len(self.get_available_neighbor_values(neighbors, already_used_values)) > 0

