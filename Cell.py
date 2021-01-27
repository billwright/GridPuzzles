from Blanking_Cell_Exception import Blanking_Cell_Exception


class Cell(object):

    def __init__(self, cell_address, cell_values):
        self.address = cell_address
        self.values = cell_values

    def __eq__(self, other):
        return isinstance(other, Cell) and self.address == other.address

    def __hash__(self):
        return hash(self.address)

    def __len__(self):
        return len(self.values)

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
        return f'Cell({self.address}) = {self.values}'

    def remove_values(self, values_to_remove):
        for value_to_remove in values_to_remove:
            if self.values == values_to_remove:
                print("Trying to remove all values from cell:", self.address)
                raise Blanking_Cell_Exception(self)
            self.values = self.values.replace(value_to_remove, '')

    def get_size(self):
        return len(self.values)
