import unittest

from Cell import Cell
from Matchlet import Matchlet


class TestMatchlet(unittest.TestCase):
    singlet_cell = Cell('A1', '1')
    A2 = Cell('A2', '12')
    A3 = Cell('A3', '123')
    A4 = Cell('A4', '1234')
    group = [singlet_cell, A2, A3, A4]

    def test_creation(self):
        matchlet = Matchlet((self.singlet_cell,), self.group)

        self.assertIsNotNone(matchlet)
        self.assertEqual('1', matchlet.get_candidates())

    def test_reduce(self):
        matchlet = Matchlet((self.singlet_cell,), self.group)
        matchlet.reduce()

        self.assertEqual('1', self.singlet_cell.candidates)
        self.assertEqual('2', self.A2.candidates)
        self.assertEqual('23', self.A3.candidates)
        self.assertEqual('234', self.A4.candidates)


if __name__ == '__main__':
    unittest.main()
