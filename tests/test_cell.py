import unittest
from CandidatesCell import CandidatesCell
from Blanking_Cell_Exception import Blanking_Cell_Exception


class TestCell(unittest.TestCase):

    def test_cell_creation(self):
        cell = CandidatesCell('A1', '1234')
        self.assertIsNotNone(cell)

        self.assertEqual('A1', cell.address)
        self.assertEqual('1234', cell.candidates)

    def test_remove_candidates(self):
        cell = CandidatesCell('A1', '1234')
        cell.remove_candidates('4')
        self.assertEqual('123', cell.candidates)
        cell.remove_candidates('13')
        self.assertEqual('2', cell.candidates)
        
    def test_size(self):
        cell = CandidatesCell('A1', '1234')
        self.assertEqual(4, cell.get_size())
        cell = CandidatesCell('A1', '3')
        self.assertEqual(1, cell.get_size())

    def test_protection_against_no_candidates(self):
        with self.assertRaises(Blanking_Cell_Exception):
            CandidatesCell('A1', '')

        cell = CandidatesCell('A1', '1234')
        with self.assertRaises(AttributeError):
            cell.candidates = ''

        with self.assertRaises(Blanking_Cell_Exception):
            cell.set_candidates('')

        with self.assertRaises(Blanking_Cell_Exception):
            cell.remove_candidates('1234')

        cell = CandidatesCell('A1', '14')
        with self.assertRaises(Blanking_Cell_Exception):
            cell.remove_candidates('1234')

    def test_cell_distance(self):
        # The Cell candidates are irrelevant here, but something must be passed in
        cell = CandidatesCell('A1', '1')
        self.assertEqual(0, cell.min_address_distance_to_cell(cell))
        self.assertEqual(1, cell.min_address_distance_to_cell(CandidatesCell('A2', '1')))
        self.assertEqual(1, cell.min_address_distance_to_cell(CandidatesCell('B1', '1')))
        self.assertEqual(8, cell.min_address_distance_to_cell(CandidatesCell('A9', '1')))
        self.assertEqual(8, cell.min_address_distance_to_cell(CandidatesCell('I1', '1')))
        self.assertEqual(8, cell.min_address_distance_to_cell(CandidatesCell('E5', '1')))



if __name__ == '__main__':
    unittest.main()
