import unittest
from Group import Group
from Cell import Cell


# noinspection PyPep8Naming
class TestGroup(unittest.TestCase):

    def test_creation(self):
        A1 = Cell('A1', '1234')
        B1 = Cell('B1', '1234')
        C1 = Cell('C1', '1234')
        D1 = Cell('D1', '1234')

        group = Group('Row 1', [A1, B1, C1, D1])
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
        A1 = Cell('A1', '1')
        B1 = Cell('B1', '2')
        C1 = Cell('C1', '2')
        D1 = Cell('D1', '4')

        group = Group('Row 1', [A1, B1, C1, D1])
        with self.assertRaises(Exception):
            group.check_consistency()


if __name__ == '__main__':
    unittest.main()
