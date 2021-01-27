import unittest
from Cell import Cell


class TestCell(unittest.TestCase):

    address = 'A1'
    values = '1234'

    def test_cell_creation(self):
        cell = Cell(self.address, self.values)
        self.assertIsNotNone(cell)

        self.assertEqual(self.address, cell.get_address())
        self.assertEqual(self.values, cell.get_values())


if __name__ == '__main__':
    unittest.main()
