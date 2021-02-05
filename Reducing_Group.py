from Matchlet import Matchlet
from Group import Group


class Reducing_Group(Group):

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

