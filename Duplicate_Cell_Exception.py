class Duplicate_Cell_Exception(Exception):
    """Exception raised when code tries to remove all values from a Cell.

    Attributes:
        repeated_candidate -- Cell trying to blank
        group -- reason for exception
    """

    def __init__(self, group_candidates, group_name):
        self.group_candidates = group_candidates
        self.group_name = group_name
        self.message = f'There are duplicates candidates in group {group_name}. Candidates are: {group_candidates}'

