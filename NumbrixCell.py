from CandidatesCell import CandidatesCell
from Blanking_Cell_Exception import Blanking_Cell_Exception


class NumbrixCell(CandidatesCell):
# TODO: NumbrixCell should not be a subclass of CandidatesCell. It has no candidates concept
    def __init__(self, cell_address, candidates):
        self._candidates = []
        super().__init__(cell_address, candidates)

    def set_candidates(self, new_candidates):
        try:
            super().set_candidates(new_candidates)
        except Blanking_Cell_Exception:
            # Do nothing. This is okay for this subclass
            pass

    def get_value(self):
        if self.is_empty():
            return None
        else:
            return self._candidates[0]

    def set_value(self, value):
        if self.is_empty():
            self._candidates = [value]
        else:
            raise ValueError("Trying to set an already set cell!")

    def candidates_string(self):
        if len(self.candidates) == 1 and self.candidates[0] is None:
            return ''
        return ','.join([str(candidate) for candidate in self.candidates])

    def is_empty(self):
        return not self._candidates
