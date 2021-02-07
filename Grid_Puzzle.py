from Reducing_Group import Reducing_Group
from grid_utils import cross


class Grid_Puzzle(object):

    def __init__(self, puzzle_definition):
        self.definition = puzzle_definition
        self.validate()
        self.size = self.calculate_size()

        self.column_names = [chr(ord('A') + col_number) for col_number in range(self.size)]
        self.row_names = [str(row_number + 1) for row_number in range(self.size)]

        self.puzzle_dict = self.create_puzzle()
        self.row_groups = self.create_row_groups()
        self.column_groups = self.create_column_groups()

    def validate(self):
        raise NotImplementedError('Subclass must implement this method!')

    def create_column_groups(self):
        groups = []
        for col_name in self.column_names:
            col_cells = []
            for row_name in self.row_names:
                col_cells.append(self.get_cell(col_name + row_name))
            groups.append(Reducing_Group(f'Column {col_name}', col_cells))
        return groups

    def create_row_groups(self):
        groups = []
        for row_name in self.row_names:
            row_cells = []
            for col_name in self.column_names:
                row_cells.append(self.get_cell(col_name + row_name))
            groups.append(Reducing_Group(f'Row {row_name}', row_cells))
        return groups

    def possible_candidates(self):
        return '1234567890ABCDEF'[0:self.size]

    def get_all_group_candidates(self):
        all_group_candidates = []
        for group in self.get_all_groups():
            all_group_candidates.append(group.get_all_candidates())
        return all_group_candidates

    def get_all_cell_addresses(self):
        return cross(self.column_names, self.row_names)

    def get_cell(self, cell_address):
        return self.puzzle_dict[cell_address]

    def get_cell_to_right(self, cell):
        # We add one because otherwise we'd get 0 for the column number of column A
        column_number = ord(cell.address[0]) - ord('A') + 1
        if column_number == self.size:
            return None
        row = cell.address[1:]

        # Here we increment the column, but we don't need to add one, since we already did this above
        column = chr(column_number + ord('A'))
        return self.get_cell(column + row)

    def get_cell_beneath(self, cell):
        row = int(cell.address[1:])
        if row == self.size:
            return None
        column = cell.address[0]
        return self.get_cell(column + str(row+1))

    def get_all_cells(self):
        return self.puzzle_dict.values()

    def get_max_cell_candidate_width(self):
        return max(cell.get_size() for cell in self.get_all_cells())

    def get_display_cell_width(self):
        return self.get_max_cell_candidate_width() + 2

    def get_display_header(self):
        heading_string = '    |'
        for col_name in self.column_names:
            heading_string += col_name.center(self.get_display_cell_width())
            heading_string += '|'
        return heading_string

    def get_horizontal_puzzle_boundary(self):
        line = '----‖'
        for i in range(1, self.size+1):
            line += '='*(self.get_max_cell_candidate_width()+2) + '‖'
        return line


