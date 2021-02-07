import unittest
from Kenken import Kenken

kenken_size_3 = [
    ('/', 3, ['A1', 'A2']),
    ('-', 1, ['B1', 'C1']),
    ('/', 3, ['B2', 'B3']),
    ('/', 2, ['C2', 'C3']),
    ('', 2, ['A3'])
]

kenken_size_4 = [
    ('*', 24, ['A1', 'A2', 'B1']),
    ('', 3, ['A3']),
    ('-', 3, ['A4', 'B4']),
    ('/', 2, ['B2', 'B3']),
    ('+', 6, ['C1', 'C2', 'D1']),
    ('+', 11, ['C3', 'C4', 'D3', 'D4']),
    ('', 3, ['D2']),
]

kenken_size_6 = [
    ('-', 1, ['A1', 'A2']),
    ('', 2, ['A3']),
    ('+', 11, ['A4', 'A5']),
    ('+', 5, ['A6', 'B6']),
    ('*', 60, ['B1', 'C1', 'C2']),
    ('', 1, ['B2']),
    ('/', 2, ['B3', 'B4']),
    ('*', 24, ['B5', 'C5', 'C6']),
    ('-', 1, ['C3', 'D3']),
    ('+', 3, ['C4', 'D4']),
    ('+', 14, ['D1', 'D2', 'E2']),
    ('*', 10, ['D5', 'D6', 'E6']),
    ('-', 3, ['E1', 'F1']),
    ('+', 7, ['E3', 'E4']),
    ('', 6, ['E5']),
    ('/', 2, ['F2', 'F3']),
    ('', 5, ['F4']),
    ('/', 2, ['F5', 'F6']),
]

kenken_size_8 = [
    ('-', 2, ['A1', 'B1']),
    ('+', 17, ['A2', 'A3', 'B3']),
    ('-', 7, ['A4', 'A5']),
    ('*', 40, ['A6', 'A7', 'A8']),
    ('+', 16, ['B2', 'C2', 'C3']),
    ('', 6, ['B4']),
    ('*', 180, ['B5', 'C4', 'C5', 'C6']),
    ('+', 16, ['B6', 'B7', 'C7']),
    ('*', 10, ['B8', 'C8']),
    ('*', 24, ['C1', 'D1', 'D2']),
    ('+', 11, ['D3', 'D4', 'D5']),
    ('+', 13, ['D6', 'D7']),
    ('/', 3, ['D8', 'E8']),
    ('+', 14, ['E1', 'E2', 'F1']),
    ('+', 21, ['E3', 'E4', 'E5']),
    ('/', 4, ['E6', 'E7']),
    ('*', 40, ['F2', 'F3', 'G2']),
    ('+', 6, ['F4', 'F5', 'F6']),
    ('+', 13, ['F7', 'G6', 'G7']),
    ('-', 2, ['F8', 'G8']),
    ('-', 2, ['G1', 'H1']),
    ('+', 7, ['G3', 'H2', 'H3']),
    ('+', 11, ['G4', 'G5']),
    ('*', 30, ['H4', 'H5']),
    ('+', 17, ['H6', 'H7', 'H8'])
]


class Test_Kenken(unittest.TestCase):

    def test_creation(self):
        kenken = Kenken(kenken_size_3)
        self.assertIsNotNone(kenken)
        self.assertEqual(kenken.size, 3)
        kenken.display()

    def test_creation_and_display_of_all_sizes(self):
        for puzzle_definition in [
            kenken_size_3,
            kenken_size_4,
            kenken_size_6,
            kenken_size_8
        ]:
            kenken = Kenken(puzzle_definition)
            self.assertIsNotNone(kenken)
            kenken.display()
            print()

    def test_writing_puzzle_to_file(self):
        kenken = Kenken(kenken_size_3)
        kenken.write_puzzle_to_file('/tmp/kenken.puzzle')

    def test_solve_simple(self):
        kenken = Kenken(kenken_size_3)
        kenken.display()

        kenken.search()
        kenken.display()
        self.assertTrue(kenken.is_solved())


if __name__ == '__main__':
    unittest.main()
