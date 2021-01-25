import unittest
from Sudoku_Puzzle import Sudoku_Puzzle


class TestSudoku(unittest.TestCase):
    sudoku_4x4_string = '1...' + \
                        '...4' + \
                        '..2.' + \
                        '.3..'

    sudoku_9x9_string = '4...6.8..' + \
                        '.754.8...' + \
                        '.8..92...' + \
                        '5.23..4..' + \
                        '..79452..' + \
                        '..4..75.3' + \
                        '...87..3.' + \
                        '...6.394.' + \
                        '..3.2...8'

    def test_4x4_grid_creation(self):
        puzzle = Sudoku_Puzzle(self.sudoku_4x4_string)
        puzzle.display()

        self.assertEqual('1', puzzle.get_cell_value('A1'), 'Cell value is incorrect')
        self.assertEqual('4', puzzle.get_cell_value('D2'), 'Cell value is incorrect')
        self.assertEqual('3', puzzle.get_cell_value('B4'), 'Cell value is incorrect')
        self.assertEqual('1234', puzzle.get_cell_value('D4'), 'Cell value is incorrect')

    def test_9x9_grid_creation(self):
        puzzle = Sudoku_Puzzle(self.sudoku_9x9_string)
        puzzle.display()

        self.assertEqual('4', puzzle.get_cell_value('A1'), 'Cell value is incorrect')
        self.assertEqual('4', puzzle.get_cell_value('D2'), 'Cell value is incorrect')
        self.assertEqual('123456789', puzzle.get_cell_value('B4'), 'Cell value is incorrect')
        self.assertEqual('3', puzzle.get_cell_value('D4'), 'Cell value is incorrect')
        self.assertEqual('8', puzzle.get_cell_value('I9'), 'Cell value is incorrect')

    def test_column_boundaries(self):
        puzzle = Sudoku_Puzzle(self.sudoku_4x4_string)
        self.assertEqual('BD', puzzle.column_boundaries)

    def test_row_boundaries(self):
        puzzle = Sudoku_Puzzle(self.sudoku_4x4_string)
        self.assertEqual('24', puzzle.row_boundaries)

if __name__ == '__main__':
    unittest.main()
