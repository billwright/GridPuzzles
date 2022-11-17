from CandidatesCell import CandidatesCell


class TicTacToe_Cell(CandidatesCell):

    def __init__(self, address, value):
        self.address = address
        self.value = value

    def __repr__(self):
        return f"Cell({self.address})={self.value}"

    def is_open(self):
        return self.value == ''
