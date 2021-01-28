import unittest
from Sudoku_Puzzle import Sudoku_Puzzle
import random
from Blanking_Cell_Exception import Blanking_Cell_Exception


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

    sudoku_6_star_9x9_string = '15.2...67' + \
                               '8.7.5614.' + \
                               '4....3..2' + \
                               '....2..1.' + \
                               '.........' + \
                               '216....3.' + \
                               '.3.....2.' + \
                               '....4....' + \
                               '57...1..4'

    blank_puzzle_template = '.........' + \
                            '.........' + \
                            '.........' + \
                            '.........' + \
                            '.........' + \
                            '.........' + \
                            '.........' + \
                            '.........' + \
                            '.........'

    another_expert_puzzle = '....729.4' + \
                            '6..8.....' + \
                            '.2.5....3' + \
                            '..5......' + \
                            '....1....' + \
                            '.74.2...1' + \
                            '..3.84...' + \
                            '..83..7..' + \
                            '..6.....2'

    sudoku_16x16_string = '261.D9.A.....7..' + \
                          '5...F...0E......' + \
                          '.B.7C6...D...0.9' + \
                          'CDE.3..B5F......' + \
                          '6....D.4C3E.8..A' + \
                          '....B0...6...F23' + \
                          '.FD...A9..0....E' + \
                          '9..C...E4..B.1..' + \
                          '..4.1..6B...A..7' + \
                          '7....F..24...95.' + \
                          'BA2...9...1E....' + \
                          'E..9.C70A.3....4' + \
                          '......2D7..F.E8B' + \
                          'D.6...5...839.C.' + \
                          '......3C...0...2' + \
                          '..A.....6.C4.370'

    def test_4x4_grid_creation(self):
        puzzle = Sudoku_Puzzle(self.sudoku_4x4_string)
        puzzle.display()

        self.assertEqual('1', puzzle.get_cell('A1').values, 'Cell value is incorrect')
        self.assertEqual('4', puzzle.get_cell('D2').values, 'Cell value is incorrect')
        self.assertEqual('3', puzzle.get_cell('B4').values, 'Cell value is incorrect')
        self.assertEqual('1234', puzzle.get_cell('D4').values, 'Cell value is incorrect')

    def test_9x9_grid_creation(self):
        puzzle = Sudoku_Puzzle(self.sudoku_9x9_string)
        puzzle.display()

        self.assertEqual('4', puzzle.get_cell('A1').values, 'Cell value is incorrect')
        self.assertEqual('4', puzzle.get_cell('D2').values, 'Cell value is incorrect')
        self.assertEqual('123456789', puzzle.get_cell('B4').values, 'Cell value is incorrect')
        self.assertEqual('3', puzzle.get_cell('D4').values, 'Cell value is incorrect')
        self.assertEqual('8', puzzle.get_cell('I9').values, 'Cell value is incorrect')

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
            Sudoku_Puzzle(self.sudoku_incorrect_string)

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
        self.assertTrue('1' in puzzle.get_cell('A2').values)
        self.assertTrue('1' in puzzle.get_cell('B2').values)

        cell = puzzle.get_cell('A1')
        cell_groups = puzzle.get_groups_for_cell(cell)
        print('All groups for cell', cell, ' are', cell_groups)
        self.assertEqual(3, len(cell_groups))

    def test_get_cell_associates(self):
        puzzle = Sudoku_Puzzle(self.sudoku_4x4_string)
        puzzle.display()

        cell = puzzle.get_cell('A1')
        associated_cells = puzzle.get_associated_cells(cell)
        print('Associated cells are:', associated_cells)

        # For a 4x4 puzzle there are 7 associated cells to each cell.
        # Three from the row, three from the column, and one extra one from the box group (two are already included)
        self.assertEqual(7, len(associated_cells))

    def test_remove_value_from_cell_associates(self):
        puzzle = Sudoku_Puzzle(self.sudoku_4x4_string)
        # Display initial state of the puzzle
        puzzle.display()

        cell = puzzle.get_cell('A1')
        puzzle.remove_value_from_cell_associates(cell)
        # Now display simplified state of the puzzle
        puzzle.display()

        # Confirm the value has been removed from all other cells in the associated groups
        self.assertFalse('1' in puzzle.get_cell('B1').values)
        self.assertFalse('1' in puzzle.get_cell('A2').values)
        self.assertFalse('1' in puzzle.get_cell('B2').values)

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

        puzzle.reduce()
        puzzle.display()
        self.assertEqual(16, puzzle.get_current_puzzle_count())
        self.assertTrue(puzzle.is_solved())

    def test_solve_4x4_puzzle(self):
        puzzle = Sudoku_Puzzle(self.sudoku_4x4_string)
        puzzle.display()

        puzzle.reduce()
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

        E4 = puzzle.get_cell('E4')
        E6 = puzzle.get_cell('E6')
        F7 = puzzle.get_cell('F7')
        F9 = puzzle.get_cell('F9')
        E8 = puzzle.get_cell('E8')
        D9 = puzzle.get_cell('D9')
        G2 = puzzle.get_cell('G2')
        G7 = puzzle.get_cell('G7')
        self.assertIn((E4, E6), doubles)
        self.assertIn((F7, F9), doubles)
        self.assertIn((E8, D9), doubles)
        self.assertIn((G2, G7), doubles)

        puzzle.search_and_reduce_doubles()
        puzzle.display()

    def test_get_sorted_cells(self):
        puzzle = Sudoku_Puzzle(self.sudoku_4x4_string)
        puzzle.display()

        sorted_cells = puzzle.get_all_cells_sorted_by_size()
        print("Sorted cells (by size):", sorted_cells)

        # Test that the first cell is shorter than the last cell
        self.assertLess(sorted_cells[0].get_size(), sorted_cells[-1].get_size())

    def test_solve_9x9_puzzles(self):
        for puzzle_string in [self.sudoku_9x9_string, self.sudoku_6_star_9x9_string, self.another_expert_puzzle]:
            puzzle = Sudoku_Puzzle(puzzle_string)
            puzzle.display()

            solved_puzzle = puzzle.search()
            solved_puzzle.display()
            self.assertTrue(solved_puzzle.is_solved())

    @unittest.expectedFailure
    def test_solve_16x16_puzzle(self):
        puzzle = Sudoku_Puzzle(self.sudoku_16x16_string)
        puzzle.display()

        solved_puzzle = puzzle.search()
        solved_puzzle.display()
        self.assertTrue(solved_puzzle.is_solved())

    @unittest.skip
    def test_creating_puzzles_solving_them(self):

        number_of_puzzles_per_clue_number = 10  # Number of puzzles to make and solve of each size/clue_number tuple
        maximum_number_of_clues = 10            # The most clues to make is 10, but for 4x4 that is clipped below to be 3
        puzzle_sizes = [4, 9]                   # create puzzles of size 4x4 and 9x9

        total_number_of_puzzles_generated = 0
        total_number_of_puzzles_solved = 0

        for puzzle_size in puzzle_sizes:
            blank_puzzle = '.' * (puzzle_size**2)       # This creates a blank puzzle string of the correct size
            max_clues = min([int(puzzle_size ** 2/5), maximum_number_of_clues])
            print(f'Testing puzzles of size {puzzle_size}, with a maximum of {max_clues}')

            for clue_number in range(1, max_clues+1):
                for test_number in range(1, number_of_puzzles_per_clue_number):
                    puzzle = Sudoku_Puzzle(blank_puzzle)
                    total_number_of_puzzles_generated += 1

                    # Create n values randomly:
                    for i in range(1, clue_number+1):
                        row = str(random.randint(1, puzzle_size))
                        column = chr(ord('A') + random.randint(0, puzzle_size-1))
                        value = str(random.randint(1, puzzle_size))

                        seed_cell = puzzle.get_cell(column+row)
                        seed_cell.values = value

                    puzzle.display()
                    try:
                        solved_puzzle = puzzle.search()
                        self.assertTrue(solved_puzzle.is_solved())
                        total_number_of_puzzles_solved += 1
                    except Blanking_Cell_Exception as error:
                        print("Probably created an invalid puzzle. Moving on...")
                    solved_puzzle.display()

        print(f'Out of {total_number_of_puzzles_generated} puzzles generated, {total_number_of_puzzles_solved} were solved')


if __name__ == '__main__':
    unittest.main()
