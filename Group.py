from Duplicate_Cell_Exception import Duplicate_Cell_Exception
from Matchlet import Matchlet

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
        if len(set(singlet_candidates)) != len(singlet_candidates):
            raise Duplicate_Cell_Exception(singlet_candidates, self.name)

    def search_and_reduce_exclusions(self):
        """This method will modify the cells in the group, if exclusive cells are found."""
        self.check_consistency()
        candidate_cell_map = dict()    # Here we keep track of each candidate and which cells it appears in
        for cell in self.cells:
            for candidate in cell.candidates:
                if candidate not in candidate_cell_map:
                    candidate_cell_map[candidate] = []
                candidate_cell_map[candidate].append(cell)

        exclusions = [(candidate, exclusion_cells) for (candidate, exclusion_cells) in candidate_cell_map.items()
                      if (len(exclusion_cells) == 1 and exclusion_cells[0].is_not_singlet())]

        for (candidate, exclusion_cells) in exclusions:
            if exclusion_cells[0].candidates != candidate:
                exclusion_cells[0].set_candidates(candidate)
            self.check_consistency()

    def find_matchlets(self):
        matchlets = []  # This is a list of matchlets, which are always tuples
        all_matched_cells = []  # A flat list to remember all matches cells to avoid duplicates

        for possible_match_cell in self.cells:
            matchlet = [cell for cell in self.cells if cell.candidates == possible_match_cell.candidates]

            # Check to make sure this is a matchlet, meaning the size of the values has to equal the number of cells
            # Also, make sure the matchlet is smaller than an entire group as there is no point of a matchlet of
            # all cells in a group
            if len(matchlet) == len(possible_match_cell.candidates) and len(matchlet) < len(self):
                previously_matched_cells = [cell for cell in matchlet if cell in all_matched_cells]
                if len(previously_matched_cells) == 0:
                    matchlets.append(Matchlet(tuple(matchlet), self))
                    for cell in matchlet:
                        all_matched_cells.append(cell)
        return matchlets

