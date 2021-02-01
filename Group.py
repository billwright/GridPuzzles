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
