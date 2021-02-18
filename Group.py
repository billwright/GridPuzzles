from Duplicate_Cell_Value_In_Group_Exception import Duplicate_Cell_Value_In_Group_Exception
from grid_utils import flatten_and_de_dup


class Group(object):

    def __init__(self, name, cells):
        self.name = name
        self.cells = cells

    def __repr__(self):
        return f'Group {self.name}'

    def __hash__(self):
        return hash(self.name)

    def __len__(self):
        return len(self.cells)

    def __contains__(self, cell):
        return cell in self.cells

    def __iter__(self):
        return self.cells.__iter__()

    def get_all_candidates(self):
        return [cell.candidates for cell in self.cells]

    def get_associated_cells(self, cell):
        return [associate for associate in self.cells if associate != cell]

    def check_consistency(self):
        singlet_candidates = [cell.candidates for cell in self.cells if len(cell) == 1]
        unique_singlets = flatten_and_de_dup(singlet_candidates)
        if len(unique_singlets) != len(singlet_candidates):
            raise Duplicate_Cell_Value_In_Group_Exception(singlet_candidates, self.name)
