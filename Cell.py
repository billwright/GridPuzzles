from Blanking_Cell_Exception import Blanking_Cell_Exception


class Cell(object):

    def __init__(self, cell_address, candidates):
        self.address = cell_address
        if len(candidates) == 0:
            raise Blanking_Cell_Exception(self)
        self._candidates = candidates

    def __eq__(self, other):
        return isinstance(other, Cell) and self.address == other.address

    def __hash__(self):
        return hash(self.address)

    def __len__(self):
        return len(self._candidates)

    # Default sort uses the size of the values attribute
    def __cmp__(self, other):
        if self.get_size() < other.get_size():
            return -1
        else:
            if self.get_size() > other.get_size():
                return 1
            return 0

    def __lt__(self, other):
        return self.get_size() < other.get_size()

    def __repr__(self):
        return f'Cell({self.address}) = {self._candidates}'

    def remove_candidates(self, candidates_to_remove):
        for candidate_to_remove in candidates_to_remove:
            if self._candidates == candidate_to_remove:
                raise Blanking_Cell_Exception(self)
            self._candidates = self._candidates.replace(candidate_to_remove, '')

    def get_size(self):
        return len(self._candidates)

    def set_candidates(self, new_candidates):
        if len(new_candidates) == 0:
            raise Blanking_Cell_Exception(self)
        self._candidates = new_candidates

    # This protects against a client (the Puzzle class) from clearing all values
    # TODO: Probably should protect the address as well.
    @property
    def candidates(self):
        return self._candidates
