import unittest
from Reducing_Group import Reducing_Group
from CandidatesCell import CandidatesCell


# noinspection PyPep8Naming
class TestGroup(unittest.TestCase):

    def test_creation(self):
        A1 = CandidatesCell('A1', '1234')
        B1 = CandidatesCell('B1', '1234')
        C1 = CandidatesCell('C1', '1234')
        D1 = CandidatesCell('D1', '1234')

        group = Reducing_Group('Row 1', [A1, B1, C1, D1])
        print(group)
        self.assertIsNotNone(group)
        self.assertEqual(4, len(group))

        self.assertTrue(A1 in group)

        for cell in group:
            print(cell)

        associated_cells = group.get_associated_cells(A1)
        self.assertEqual(3, len(associated_cells))
        self.assertTrue(B1 in associated_cells)
        self.assertTrue(C1 in associated_cells)
        self.assertTrue(D1 in associated_cells)

    def test_consistency(self):
        A1 = CandidatesCell('A1', '1')
        B1 = CandidatesCell('B1', '2')
        C1 = CandidatesCell('C1', '2')
        D1 = CandidatesCell('D1', '4')

        group = Reducing_Group('Row 1', [A1, B1, C1, D1])
        with self.assertRaises(Exception):
            group.check_consistency()


if __name__ == '__main__':
    unittest.main()
