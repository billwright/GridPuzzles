import unittest
import sudoku_puzzle_solver


class MyTestCase(unittest.TestCase):
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

    def test_creation_cell_addresses_for_4x4(self):
        puzzle_string = self.sudoku_4x4_string
        column_names = sudoku_puzzle_solver.column_names(puzzle_string)
        self.assertEqual(column_names, 'ABCD')

        row_names = sudoku_puzzle_solver.row_names(puzzle_string)
        self.assertEqual(row_names, '1234')

        addresses = sudoku_puzzle_solver.ordered_cell_addresses(puzzle_string)
        self.assertEqual(len(addresses), len(puzzle_string))
        expected_addresses = ['A1', 'B1', 'C1', 'D1', 'A2', 'B2', 'C2', 'D2', 'A3', 'B3', 'C3', 'D3', 'A4', 'B4', 'C4', 'D4']
        self.assertEqual(expected_addresses, addresses)
        print(addresses)
        print()

    def test_creation_cell_addresses_for_9x9(self):
        puzzle_string = self.sudoku_9x9_string
        column_names = sudoku_puzzle_solver.column_names(puzzle_string)
        self.assertEqual(column_names, 'ABCDEFGHI')

        row_names = sudoku_puzzle_solver.row_names(puzzle_string)
        self.assertEqual(row_names, '123456789')

        addresses = sudoku_puzzle_solver.ordered_cell_addresses(puzzle_string)
        self.assertEqual(len(addresses), len(puzzle_string))
        print(addresses)
        print()

    def test_creation_of_values(self):
        values = sudoku_puzzle_solver.create_ordered_values_from_puzzle_string(self.sudoku_4x4_string)
        self.assertEqual(len(values), 16)

        values = sudoku_puzzle_solver.create_ordered_values_from_puzzle_string(self.sudoku_9x9_string)
        self.assertEqual(len(values), 81)

    def test_initializing_of_4x4_puzzle(self):
        puzzle_string = self.sudoku_4x4_string

        sudoku_puzzle = sudoku_puzzle_solver.create_puzzle(puzzle_string)
        self.assertEqual(len(sudoku_puzzle), 16)

        sudoku_puzzle_solver.display_puzzle_simple(
            sudoku_puzzle,
            sudoku_puzzle_solver.row_names(puzzle_string),
            sudoku_puzzle_solver.column_names(puzzle_string))

        self.assertEqual(sudoku_puzzle['A1'], '1')
        self.assertEqual('3', sudoku_puzzle['B4'])
        self.assertEqual(sudoku_puzzle['D3'], '1234')

        print()

    def test_initializing_of_9x9_puzzle(self):
        puzzle_string = self.sudoku_9x9_string

        sudoku_puzzle = sudoku_puzzle_solver.create_puzzle(puzzle_string)
        self.assertEqual(len(sudoku_puzzle), 81)

        sudoku_puzzle_solver.display_puzzle_simple(
            sudoku_puzzle,
            sudoku_puzzle_solver.row_names(puzzle_string),
            sudoku_puzzle_solver.column_names(puzzle_string))

        self.assertEqual(sudoku_puzzle['C2'], '5')
        self.assertEqual(sudoku_puzzle['I9'], '8')
        self.assertEqual(sudoku_puzzle['B1'], '123456789')

        print()
