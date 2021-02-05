from Calculation_Group import Calculation_Group


class Kenken(object):

    def __init__(self, puzzle_group_definitions):
        self.size = self.calculate_size(puzzle_group_definitions)
        self.calculation_groups = [Calculation_Group(group_def, self.size) for group_def in puzzle_group_definitions]

    def calculate_size(self, puzzle_group_definitions):
        addresses = []
        for (_, _, cell_addresses) in puzzle_group_definitions:
            addresses.extend(cell_addresses)
        # Assume addresses are of this form: A1 -- with first character the column and the second the row
        self.columns = list(set([address[0] for address in addresses]))
        self.rows = list(set([address[1] for address in addresses]))
        self.columns.sort()
        self.rows.sort()

        if len(self.rows) != len(self.columns):
            raise ValueError("Cell addresses do not form a square")

        return len(self.columns)

    def display(self):
        print('TODO')
