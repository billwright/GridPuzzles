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

    def test_get_cell_groups(self):
        puzzle = Sudoku_Puzzle(self.sudoku_4x4_string)
        puzzle.display()

        # Confirm choices are there before elimination
        self.assertTrue('1' in puzzle.get_cell_value('B1'))
        self.assertTrue('1' in puzzle.get_cell_value('A2'))
        self.assertTrue('1' in puzzle.get_cell_value('B2'))

        cell_address = 'A1'
        cell_groups = puzzle.get_groups_for_cell(cell_address)
        print('All groups for cell', cell_address, ' are', cell_groups)
        self.assertEqual(3, len(cell_groups))

    def test_get_cell_associates(self):
        puzzle = Sudoku_Puzzle(self.sudoku_4x4_string)
        puzzle.display()

        cell_address = 'A1'
        associated_cells = puzzle.get_associated_cells(cell_address)
        print('Associated cells are:', associated_cells)

        # For a 4x4 puzzle there are 7 associated cells to each cell.
        # Three from the row, three from the column, and one extra one from the box group (two are already included)
        self.assertEqual(7, len(associated_cells))

    def test_remove_value_from_cell_associates(self):
        puzzle = Sudoku_Puzzle(self.sudoku_4x4_string)
        # Display initial state of the puzzle
        puzzle.display()

        cell_address = 'A1'
        puzzle.remove_value_from_cell_associates(cell_address, puzzle.get_cell_value(cell_address))
        # Now display simplified state of the puzzle
        puzzle.display()

        # Confirm the value has been removed from all other cells in the associated groups
        self.assertFalse('1' in puzzle.get_cell_value('B1'))
        self.assertFalse('1' in puzzle.get_cell_value('A2'))
        self.assertFalse('1' in puzzle.get_cell_value('B2'))

    def test_get_current_puzzle_size(self):
        puzzle = Sudoku_Puzzle(self.sudoku_solved_4x4_string)
        puzzle_count = puzzle.get_current_puzzle_count()
        print('The current puzzle count is', puzzle_count)
        self.assertEqual(16, puzzle_count)

        puzzle = Sudoku_Puzzle(self.sudoku_4x4_string)
        puzzle_count = puzzle.get_current_puzzle_count()
        print('The current puzzle count is', puzzle_count)
        self.assertEqual(52, puzzle_count)

    def test_solve_simple_puzzle(self):
        puzzle = Sudoku_Puzzle(self.sudoku_4x4_string)
        puzzle.display()
        self.assertEqual(52, puzzle.get_current_puzzle_count())

        puzzle.solve()
        puzzle.display()
        self.assertEqual(16, puzzle.get_current_puzzle_count())
        self.assertTrue(puzzle.is_solved())

    def test_solve_4x4_puzzle(self):
        puzzle = Sudoku_Puzzle(self.sudoku_4x4_string)
        puzzle.display()

        puzzle.solve()
        puzzle.display()
        self.assertTrue(puzzle.is_solved())

    def test_find_doubles(self):
        puzzle = Sudoku_Puzzle(self.sudoku_9x9_string)
        puzzle.search_and_reduce_singletons()
        puzzle.search_and_reduce_singletons()
        puzzle.search_and_reduce_singletons()
        puzzle.display()

        cells_with_values_of_size_two = puzzle.get_cells_with_value_size(2)
        print('cells with value of size 2:', cells_with_values_of_size_two)

        doubles = puzzle.find_doubles()
        print('doubles are:', doubles)
        self.assertEqual(7, len(doubles))

        self.assertIn(('E4', 'E6'), doubles)
        self.assertIn(('F7', 'F9'), doubles)
        self.assertIn(('E8', 'D9'), doubles)
        self.assertIn(('G2', 'G7'), doubles)

        puzzle.search_and_reduce_doubles()
        puzzle.display()

    def test_solve_9x9_puzzle(self):
        puzzle = Sudoku_Puzzle(self.sudoku_9x9_string)
        puzzle.display()

        puzzle.solve()
        puzzle.display()
        self.assertTrue(puzzle.is_solved())


if __name__ == '__main__':
    unittest.main()
