import unittest
from Sudoku_Puzzle import Sudoku_Puzzle


class TestSudoku(unittest.TestCase):
    sudoku_incorrect_string = '1...4...321...'

    sudoku_4x4_string = '1...' + \
                        '...4' + \
                        '..2.' + \
                        '.3..'

    sudoku_not_solved_4x4_string = '1234' + \
                                   '1234' + \
                                   '1234' + \
                                   '1234'

    sudoku_solved_4x4_string = '1234' + \
                               '3412' + \
                               '2143' + \
                               '4321'

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

    def test_box_groups(self):
        puzzle = Sudoku_Puzzle(self.sudoku_4x4_string)
        box_groupings = puzzle.box_groupings()
        print('Box groupings are:', box_groupings)
        self.assertEqual(4, len(box_groupings))

    def test_row_groups(self):
        puzzle = Sudoku_Puzzle(self.sudoku_4x4_string)
        row_groupings = puzzle.row_groupings()
        print('Row groupings are:', row_groupings)
        for group in row_groupings:
            self.assertEqual(4, len(group))
        self.assertEqual(4, len(row_groupings))

    def test_all_groups(self):
        puzzle = Sudoku_Puzzle(self.sudoku_4x4_string)
        all_groups = puzzle.get_all_groups()
        print('All groups are:', all_groups)
        self.assertEqual(12, len(all_groups))

    def test_incorrect_sudoku_string(self):
        with self.assertRaises(Exception):
            puzzle = Sudoku_Puzzle(self.sudoku_incorrect_string)

    def test_puzzle_not_solved(self):
        puzzle = Sudoku_Puzzle(self.sudoku_4x4_string)
        self.assertFalse(puzzle.is_solved(), 'Puzzle is wrongly assumed to be solved.')

    def test_puzzle_seemingly_solved(self):
        puzzle = Sudoku_Puzzle(self.sudoku_not_solved_4x4_string)
        self.assertFalse(puzzle.is_solved(), 'Puzzle is wrongly assumed to NOT be solved.')

    def test_puzzle_really_solved(self):
        puzzle = Sudoku_Puzzle(self.sudoku_solved_4x4_string)
        self.assertTrue(puzzle.is_solved(), 'Puzzle is wrongly assumed to NOT be solved.')


if __name__ == '__main__':
    unittest.main()
