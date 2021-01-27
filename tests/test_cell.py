import unittest
from Cell import Cell


class TestCell(unittest.TestCase):

    def test_cell_creation(self):
        cell = Cell('A1', '1234')
        self.assertIsNotNone(cell)

        self.assertEqual('A1', cell.address)
        self.assertEqual('1234', cell.values)

    def test_remove_values(self):
        cell = Cell('A1', '1234')
        cell.remove_values('4')
        self.assertEqual('123', cell.values)
        cell.remove_values('13')
        self.assertEqual('2', cell.values)
        
    def test_size(self):
        cell = Cell('A1', '1234')
        self.assertEqual(4, cell.get_size())
        cell = Cell('A1', '3')
        self.assertEqual(1, cell.get_size())




if __name__ == '__main__':
    unittest.main()
