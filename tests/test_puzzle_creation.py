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
        self.assertEqual('ABCD', column_names)

        row_names = sudoku_puzzle_solver.row_names(puzzle_string)
        self.assertEqual('1234', row_names)

        addresses = sudoku_puzzle_solver.ordered_cell_addresses(puzzle_string)
        self.assertEqual(len(addresses), len(puzzle_string))
        expected_addresses = ['A1', 'B1', 'C1', 'D1', 'A2', 'B2', 'C2', 'D2', 'A3', 'B3', 'C3', 'D3', 'A4', 'B4', 'C4', 'D4']
        self.assertEqual(expected_addresses, addresses)
        print(addresses)
        print()

    def test_creation_cell_addresses_for_9x9(self):
        puzzle_string = self.sudoku_9x9_string
        column_names = sudoku_puzzle_solver.column_names(puzzle_string)
        self.assertEqual('ABCDEFGHI', column_names)

        row_names = sudoku_puzzle_solver.row_names(puzzle_string)
        self.assertEqual('123456789', row_names)

        addresses = sudoku_puzzle_solver.ordered_cell_addresses(puzzle_string)
        self.assertEqual(len(addresses), len(puzzle_string))
        print(addresses)
        print()

    def test_creation_of_values(self):
        values = sudoku_puzzle_solver.create_ordered_values_from_puzzle_string(self.sudoku_4x4_string)
        self.assertEqual(16, len(values))

        values = sudoku_puzzle_solver.create_ordered_values_from_puzzle_string(self.sudoku_9x9_string)
        self.assertEqual(81, len(values))

    def test_initializing_of_4x4_puzzle(self):
        puzzle_string = self.sudoku_4x4_string

        sudoku_puzzle = sudoku_puzzle_solver.create_puzzle(puzzle_string)
        self.assertEqual(16, len(sudoku_puzzle))

        sudoku_puzzle_solver.display_puzzle_simple(
            sudoku_puzzle,
            sudoku_puzzle_solver.row_names(puzzle_string),
            sudoku_puzzle_solver.column_names(puzzle_string))

        self.assertEqual('1', sudoku_puzzle['A1'])
        self.assertEqual('3', sudoku_puzzle['B4'])
        self.assertEqual('1234', sudoku_puzzle['D3'])

        print()

    def test_initializing_of_9x9_puzzle(self):
        puzzle_string = self.sudoku_9x9_string

        sudoku_puzzle = sudoku_puzzle_solver.create_puzzle(puzzle_string)
        self.assertEqual(len(sudoku_puzzle), 81)

        sudoku_puzzle_solver.display_puzzle_simple(
            sudoku_puzzle,
            sudoku_puzzle_solver.row_names(puzzle_string),
            sudoku_puzzle_solver.column_names(puzzle_string))

        self.assertEqual('5', sudoku_puzzle['C2'])
        self.assertEqual('8', sudoku_puzzle['I9'])
        self.assertEqual('123456789', sudoku_puzzle['B1'])

        print()

    def test_box_groupings(self):
        puzzle_string = self.sudoku_4x4_string

        column_names = sudoku_puzzle_solver.column_names(puzzle_string)
        row_names = sudoku_puzzle_solver.row_names(puzzle_string)

        box_groupings = sudoku_puzzle_solver.box_groupings(column_names, row_names)
        expected_box_groupings = [ ['A1', 'B1', 'A2', 'B2'], ['A3', 'B3', 'A4', 'B4'], ['C1', 'D1', 'C2', 'D2'], ['C3', 'D3', 'C4', 'D4']]
        self.assertEqual(expected_box_groupings, box_groupings)

    def test_column_groupings(self):
        puzzle_string = self.sudoku_4x4_string
        column_names = sudoku_puzzle_solver.column_names(puzzle_string)
        row_names = sudoku_puzzle_solver.row_names(puzzle_string)

        column_groupings = sudoku_puzzle_solver.column_groupings(column_names, row_names)
        expected_column_groupings = [['A1', 'A2', 'A3', 'A4'], ['B1', 'B2', 'B3', 'B4'], ['C1', 'C2', 'C3', 'C4'], ['D1', 'D2', 'D3', 'D4']]
        self.assertEqual(expected_column_groupings, column_groupings)

    def test_row_groupings(self):
        puzzle_string = self.sudoku_4x4_string
        column_names = sudoku_puzzle_solver.column_names(puzzle_string)
        row_names = sudoku_puzzle_solver.row_names(puzzle_string)

        row_groupings = sudoku_puzzle_solver.row_groupings(column_names, row_names)
        expected_row_groupings = [['A1', 'B1', 'C1', 'D1'], ['A2', 'B2', 'C2', 'D2'], ['A3', 'B3', 'C3', 'D3'],['A4', 'B4', 'C4', 'D4']]
        self.assertEqual(expected_row_groupings, row_groupings)

