import unittest
from Cell import Cell
from Blanking_Cell_Exception import Blanking_Cell_Exception


class TestCell(unittest.TestCase):

    def test_cell_creation(self):
        cell = Cell('A1', '1234')
        self.assertIsNotNone(cell)

        self.assertEqual('A1', cell.address)
        self.assertEqual('1234', cell.candidates)

    def test_remove_candidates(self):
        cell = Cell('A1', '1234')
        cell.remove_candidates('4')
        self.assertEqual('123', cell.candidates)
        cell.remove_candidates('13')
        self.assertEqual('2', cell.candidates)
        
    def test_size(self):
        cell = Cell('A1', '1234')
        self.assertEqual(4, cell.get_size())
        cell = Cell('A1', '3')
        self.assertEqual(1, cell.get_size())

    def test_protection_against_no_candidates(self):
        with self.assertRaises(Blanking_Cell_Exception):
            Cell('A1', '')

        cell = Cell('A1', '1234')
        with self.assertRaises(AttributeError):
            cell.candidates = ''

        with self.assertRaises(Blanking_Cell_Exception):
            cell.set_candidates('')

        with self.assertRaises(Blanking_Cell_Exception):
            cell.remove_candidates('1234')

        cell = Cell('A1', '14')
        with self.assertRaises(Blanking_Cell_Exception):
            cell.remove_candidates('1234')

    def test_cell_distance(self):
        # The Cell candidates are irrelevant here, but something must be passed in
        cell = Cell('A1', '1')
        self.assertEqual(0, cell.distance_to_cell(cell))
        self.assertEqual(1, cell.distance_to_cell(Cell('A2', '1')))
        self.assertEqual(1, cell.distance_to_cell(Cell('B1', '1')))
        self.assertEqual(8, cell.distance_to_cell(Cell('A9', '1')))
        self.assertEqual(8, cell.distance_to_cell(Cell('I1', '1')))
        self.assertEqual(8, cell.distance_to_cell(Cell('E5', '1')))



if __name__ == '__main__':
    unittest.main()
