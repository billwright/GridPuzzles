class Matchlet(object):

    def __init__(self, cells_of_matchlet, group_containing_matchlets):
        self.cells = cells_of_matchlet
        self.group = group_containing_matchlets

    def __len__(self):
        return len(self.cells)

    def __repr__(self):
        return f'Matchlet({self.cells})'

    def get_candidates(self):
        return self.cells[0].candidates

    def reduce(self):
        for cell in self.group:
            if cell not in self.cells:
                cell.remove_candidates(self.get_candidates())

