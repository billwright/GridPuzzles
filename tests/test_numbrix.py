import logging
import unittest

from Chain_Endpoint import Chain_Endpoint
from Numbrix import Numbrix
from Numbrix_Cell import Numbrix_Cell
from Path import Path

logging.basicConfig(format='%(message)s', level=logging.DEBUG)

# Example puzzles here: https://www.mathinenglish.com/puzzlesnumbrix.php
#
# All-moves-forced puzzle. Just calling reduce_neighbors() repeatedly solves this puzzle
all_moves_forced_6_by_6 = [None, 15, 10, 9, 8, None,
                           17, None, None, None, None, 6,
                           18, None, 12, 3, None, 1,
                           19, None, 25, 26, None, 30,
                           20, None, None, None, None, 31,
                           None, 22, 35, 34, 33, None]

easy_4_forced_moves_one_gap_move = [None, None, None, None, None, None,
                                    31, None, 25, 22, 19, None,
                                    None, 27, 26, 21, 20, None,
                                    None, 34, 35, 12, 13, None,
                                    None, 3, 36, 11, 10, None,
                                    None, None, None, None, None, None]

easy_4_forced_moves_6_by_6 = [None, None, None, None, None, None,
                              None, 28, 25, 22, 19, None,
                              None, 27, 26, 21, 20, None,
                              None, 34, 35, 12, 13, None,
                              None, 3, 36, 11, 10, None,
                              None, None, None, None, None, None]

medium_6_by_6 = [4, None, None, None, None, 29,
                 None, 2, 33, 26, 27, None,
                 None, None, None, None, 24, None,
                 None, 36, None, None, 21, None,
                 None, 11, 12, 19, 18, None,
                 9, None, None, None, None, 16]

hard_6_by_6 = [None, None, None, None, None, None,
               None, 21, 24, 35, 36, None,
               None, 22, None, None, 33, None,
               None, 15, None, None, 32, None,
               None, 14, 9, 6, 5, None,
               None, None, None, None, None, None]

# Solution to the above puzzle is:
hard_6_by_6_solution = [19, 20, 25, 26, 27, 28,
                        18, 21, 24, 35, 36, 29,
                        17, 22, 23, 34, 33, 30,
                        16, 15, 8, 7, 32, 31,
                        13, 14, 9, 6, 5, 4,
                        12, 11, 10, 1, 2, 3]

very_hard_6_by_6 = [10, None, None, None, None, 1,
                    None, None, 5, 34, None, None,
                    None, 7, None, None, 36, None,
                    None, 14, None, None, 29, None,
                    None, None, 16, 27, None, None,
                    19, None, None, None, None, 24]

# Solution to the above puzzle is:
very_hard_6_by_6_solution = [10, 9, 4, 3, 2, 1,
                             11, 8, 5, 34, 33, 32,
                             12, 7, 6, 35, 36, 31,
                             13, 14, 15, 28, 29, 30,
                             18, 17, 16, 27, 26, 25,
                             19, 20, 21, 22, 23, 24]

blank_6_by_6 = [None, None, None, None, None, None,
                None, None, None, None, None, None,
                None, None, None, None, None, None,
                None, None, None, None, None, None,
                None, None, None, None, None, None,
                None, None, None, None, None, None]

beginner_puzzle_9_by_9 = [5, 6, 7, 8, 9, 24, 25, 30, 31,
                          4, None, None, None, None, None, None, None, 32,
                          15, None, None, None, None, None, None, None, 33,
                          16, None, None, None, None, None, None, None, 34,
                          65, None, None, None, None, None, None, None, 39,
                          66, None, None, None, None, None, None, None, 40,
                          69, None, None, None, None, None, None, None, 45,
                          70, None, None, None, None, None, None, None, 46,
                          71, 72, 81, 80, 79, 52, 51, 48, 47]

one_gaps = [3, None, 9, None, 17, None, 21, None, 23,
            None, None, None, None, None, None, None, None, None,
            1, None, None, None, None, None, None, None, 27,
            None, None, None, None, None, None, None, None, None,
            59, None, None, None, None, None, None, None, 43,
            None, None, None, None, None, None, None, None, None,
            63, None, None, None, None, None, None, None, 81,
            None, None, None, None, None, None, None, None, None,
            67, None, 69, None, 73, None, 77, None, 79]

# This puzzle, with the code as of this date (11/21/21), was solved
# in 5h23m! It took 5040 backtracks to solve it.
# TODO: Work on techniques to make this better and to analyze why it takes so long
nov_21_2021 = [1, None, 7, None, 75, None, 81, None, 61,
               None, None, None, None, None, None, None, None, None,
               3, None, None, None, None, None, None, None, 59,
               None, None, None, None, None, None, None, None, None,
               19, None, None, None, None, None, None, None, 57,
               None, None, None, None, None, None, None, None, None,
               23, None, None, None, None, None, None, None, 49,
               None, None, None, None, None, None, None, None, None,
               25, None, 27, None, 35, None, 45, None, 47]

# This puzzle, with the code as of this date (11/21/21), was solved
# in less than 2 seconds. It took 3 backtracks to solve it.
dec_5_2021 = [17, None, 11, None, 3, None, 1, None, 75,
              None, None, None, None, None, None, None, None, None,
              19, None, None, None, None, None, None, None, 73,
              None, None, None, None, None, None, None, None, None,
              21, None, None, None, None, None, None, None, 69,
              None, None, None, None, None, None, None, None, None,
              29, None, None, None, None, None, None, None, 65,
              None, None, None, None, None, None, None, None, None,
              35, None, 37, None, 51, None, 53, None, 55]

# This puzzle, with the code as of this date (11/21/21), was solved
# in 19 seconds. It took 228 backtracks to solve it.
jan_30_2022 = [25, None, 23, None, 19, None, 3, None, 7,
               None, None, None, None, None, None, None, None, None,
               29, None, None, None, None, None, None, None, 9,
               None, None, None, None, None, None, None, None, None,
               39, None, None, None, None, None, None, None, 11,
               None, None, None, None, None, None, None, None, None,
               41, None, None, None, None, None, None, None, 73,
               None, None, None, None, None, None, None, None, None,
               43, None, 51, None, 59, None, 81, None, 79]

# This puzzle causes the program to fail:
# Error
# Traceback (most recent call last):
# File "/Users/bwright/PycharmProjects/GridPuzzles/tests/test_numbrix.py", line 300, in test_solving_puzzles
# solved_puzzle.display()
# AttributeError: 'NoneType' object has no attribute 'display'

mar_20_2022 = [7, None, 5, None, 21, None, 31, None, 33,
               None, None, None, None, None, None, None, None, None,
               9, None, None, None, None, None, None, None, 37,
               None, None, None, None, None, None, None, None, None,
               13, None, None, None, None, None, None, None, 41,
               None, None, None, None, None, None, None, None, None,
               71, None, None, None, None, None, None, None, 43,
               None, None, None, None, None, None, None, None, None,
               75, None, 77, None, 55, None, 53, None, 45]

# The solver gets an error when trying to solve this puzzle:
# Error
# Traceback (most recent call last):
# File "/Users/bwright/PycharmProjects/GridPuzzles/tests/test_numbrix.py", line 316, in test_solving_puzzles
# solved_puzzle.display()
# AttributeError: 'NoneType' object has no attribute 'display'
#
apr_3_2022 = [None, None, None, None, 41, None, None, None, None,
              None, 51, 50, None, None, None, 34, 35, None,
              None, 56, None, None, None, None, None, 32, None,
              None, None, None, None, None, None, None, None, None,
              77, None, None, None, None, None, None, None, 21,
              None, None, None, None, None, None, None, None, None,
              None, 70, None, None, None, None, None, 2, None,
              None, 71, 68, None, None, None, 8, 1, None,
              None, None, None, None, 13, None, None, None, None]

apr_10_2022 = [77, None, None, None, 53, None, None, None, 41,
               None, 75, None, None, 50, None, None, 39, None,
               None, None, None, None, None, None, None, None, None,
               None, None, None, None, None, None, None, None, None,
               1, 2, None, None, None, None, None, 32, 31,
               None, None, None, None, None, None, None, None, None,
               None, None, None, None, None, None, None, None, None,
               None, 7, None, None, 14, None, None, 25, None,
               9, None, None, None, 13, None, None, None, 21]

apr_17_2022 = [33, None, 37, None, 41, None, 43, None, 45,
               None, None, None, None, None, None, None, None, None,
               31, None, None, None, None, None, None, None, 53,
               None, None, None, None, None, None, None, None, None,
               21, None, None, None, None, None, None, None, 55,
               None, None, None, None, None, None, None, None, None,
               5, None, None, None, None, None, None, None, 77,
               None, None, None, None, None, None, None, None, None,
               7, None, 9, None, 13, None, 71, None, 75]

# TODO: Handle this situation.
#  This is an invalid puzzle. The given value of 61 should be 81. Ideally,
#  the code should figure out the puzzles is unsolvable. Currently, it not
#  only fails to solve it (expected), but it crashes AND it somehow changes
#  some of the given values. That should be impossible. Fix this.
# in less than 2 seconds. It took 3 backtracks to solve it.
invalid_puzzle = [25, None, 23, None, 19, None, 3, None, 7,
                  None, None, None, None, None, None, None, None, None,
                  29, None, None, None, None, None, None, None, 9,
                  None, None, None, None, None, None, None, None, None,
                  39, None, None, None, None, None, None, None, 11,
                  None, None, None, None, None, None, None, None, None,
                  41, None, None, None, None, None, None, None, 73,
                  None, None, None, None, None, None, None, None, None,
                  43, None, 51, None, 59, None, 61, None, 79]

very_hard_puzzle = [55, None, 61, None, 69, None, 79, None, 77,
                    None, None, None, None, None, None, None, None, None,
                    53, None, None, None, None, None, None, None, 75,
                    None, None, None, None, None, None, None, None, None,
                    47, None, None, None, None, None, None, None, 31,
                    None, None, None, None, None, None, None, None, None,
                    45, None, None, None, None, None, None, None, 17,
                    None, None, None, None, None, None, None, None, None,
                    5, None, 7, None, 9, None, 13, None, 15]

may_1_puzzle = [73, None, None, None, 69, None, None, None, 57,
                None, 75, None, None, 68, None, None, 59, None,
                None, None, None, None, None, None, None, None, None,
                None, None, None, None, None, None, None, None, None,
                45, 44, None, None, None, None, None, 2, 3,
                None, None, None, None, None, None, None, None, None,
                None, None, None, None, None, None, None, None, None,
                None, 27, None, None, 36, None, None, 13, None,
                25, None, None, None, 17, None, None, None, 11]

may_23_puzzle = [23, None, None, None, 77, None, None, None, 71,
                 None, None, None, 29, None, 75, None, None, None,
                 None, None, None, None, None, None, None, None, None,
                 None, 19, None, None, None, None, None, 65, None,
                 17, None, None, None, None, None, None, None, 57,
                 None, 15, None, None, None, None, None, 59, None,
                 None, None, None, None, None, None, None, None, None,
                 None, None, None, 37, None, 41, None, None, None,
                 9, None, None, None, 39, None, None, None, 53]

# the solution to this puzzle is:
#         59 58 57 56 53 52 49 48 47
#         60 63 64 55 54 51 50 45 46
#         61 62 65 66 79 80 81 44 43
#         70 69 68 67 78 39 40 41 42
#         71 72 73 76 77 38 1 2 3
#         30 31 74 75 36 37 14 13 4
#         29 32 33 34 35 16 15 12 5
#         28 25 24 21 20 17 10 11 6
#         27 26 23 22 19 18 9 8 7
sept_18_puzzle = [59, None, None, None, 53, None, None, None, 47,
                  None, 63, None, None, 54, None, None, 45, None,
                  None, None, None, None, None, None, None, None, None,
                  None, None, None, None, None, None, None, None, None,
                  71, 72, None, None, None, None, None, 2, 3,
                  None, None, None, None, None, None, None, None, None,
                  None, None, None, None, None, None, None, None, None,
                  None, 25, None, None, 20, None, None, 11, None,
                  27, None, None, None, 19, None, None, None, 7]

# This next puzzle is hard. Here was the results of solving it:
#         |  A  |  B  |  C  |  D  |  E  |  F  |  G  |  H  |  I  |
#     ----‖=====‖=====‖=====‖=====‖=====‖=====‖=====‖=====‖=====‖
#       1 |  23 |  24 |  27 |  28 |  77 |  76 |  73 |  72 |  71 |
#       2 |  22 |  25 |  26 |  29 |  78 |  75 |  74 |  69 |  70 |
#       3 |  21 |  20 |  1  |  30 |  79 |  80 |  81 |  68 |  67 |
#       4 |  18 |  19 |  2  |  31 |  32 |  63 |  64 |  65 |  66 |
#       5 |  17 |  16 |  3  |  34 |  33 |  62 |  61 |  58 |  57 |
#       6 |  14 |  15 |  4  |  35 |  44 |  45 |  60 |  59 |  56 |
#       7 |  13 |  12 |  5  |  36 |  43 |  46 |  47 |  48 |  55 |
#       8 |  10 |  11 |  6  |  37 |  42 |  41 |  50 |  49 |  54 |
#       9 |  9  |  8  |  7  |  38 |  39 |  40 |  51 |  52 |  53 |
#     ----‖=====‖=====‖=====‖=====‖=====‖=====‖=====‖=====‖=====‖
#     The current puzzle count is 81
#     Guessed route are:
#          [Cell(B6) = [15], Cell(B5) = [16], Cell(A5) = [17]]
#          [Cell(D8) = [37], Cell(D9) = [38], Cell(E9) = [39]]
#          [Cell(E9) = [39], Cell(F9) = [40], Cell(F8) = [41]]
#          [Cell(F2) = [75], Cell(F1) = [76], Cell(E1) = [77]]
#          [Cell(B4) = [19], Cell(B3) = [20], Cell(A3) = [21], Cell(A2) = [22], Cell(A1) = [23]]
#          [Cell(B1) = [24], Cell(B2) = [25], Cell(C2) = [26], Cell(C1) = [27], Cell(D1) = [28], Cell(D2) = [29]]
#          [Cell(I1) = [71], Cell(H1) = [72], Cell(G1) = [73], Cell(G2) = [74], Cell(F2) = [75]]
#          [Cell(H4) = [65], Cell(I4) = [66], Cell(I3) = [67], Cell(H3) = [68], Cell(H2) = [69], Cell(I2) = [70]]
#          [Cell(H6) = [59], Cell(G6) = [60], Cell(G5) = [61], Cell(F5) = [62], Cell(F4) = [63], Cell(G4) = [64]]
#          [Cell(A9) = [9], Cell(A8) = [10], Cell(B8) = [11], Cell(B7) = [12], Cell(A7) = [13], Cell(A6) = [14], Cell(B6) = [15]]
#          [Cell(D3) = [30], Cell(D4) = [31], Cell(E4) = [32], Cell(E5) = [33], Cell(D5) = [34], Cell(D6) = [35], Cell(D7) = [36], Cell(D8) = [37]]
#     Guessed cells are:
#     Number of backtracks: 145
may_29_2022_puzzle = [23, None, None, None, 77, None, None, None, 71,
                      None, None, None, 29, None, 75, None, None, None,
                      None, None, None, None, None, None, None, None, None,
                      None, 19, None, None, None, None, None, 65, None,
                      17, None, None, None, None, None, None, None, 57,
                      None, 15, None, None, None, None, None, 59, None,
                      None, None, None, None, None, None, None, None, None,
                      None, None, None, 37, None, 41, None, None, None,
                      9, None, None, None, 39, None, None, None, 53]


# noinspection PyPep8Naming
class TestNumbrix(unittest.TestCase):

    def test_creation(self):
        numbrix = Numbrix(beginner_puzzle_9_by_9)
        self.assertIsNotNone(numbrix)
        numbrix.display()

    def test_get_neighbors(self):
        numbrix = Numbrix(beginner_puzzle_9_by_9)
        cell_A1 = numbrix.get_cell('A1')
        neighbors_of_cell_A1 = numbrix.get_cell_neighbors(cell_A1)
        print('Neighbors of cell A1:', neighbors_of_cell_A1)
        self.assertTrue(cell_A1 not in neighbors_of_cell_A1)
        self.assertEqual(2, len(neighbors_of_cell_A1))

        cell_I9 = numbrix.get_cell('I9')
        neighbors_of_cell_I9 = numbrix.get_cell_neighbors(cell_I9)
        print('Neighbors of cell I9:', neighbors_of_cell_I9)
        self.assertTrue(cell_I9 not in neighbors_of_cell_I9)
        self.assertEqual(2, len(neighbors_of_cell_I9))

        cell_A2 = numbrix.get_cell('A2')
        neighbors_of_cell_A2 = numbrix.get_cell_neighbors(cell_A2)
        print('Neighbors of cell A2:', neighbors_of_cell_A2)
        self.assertTrue(cell_A2 not in neighbors_of_cell_A2)
        self.assertEqual(3, len(neighbors_of_cell_A2))

        cell_B2 = numbrix.get_cell('B2')
        neighbors_of_cell_B2 = numbrix.get_cell_neighbors(cell_B2)
        print('Neighbors of cell B2:', neighbors_of_cell_B2)
        self.assertTrue(cell_B2 not in neighbors_of_cell_B2)
        self.assertEqual(4, len(neighbors_of_cell_B2))

    def test_cell_reduction(self):
        numbrix = Numbrix(beginner_puzzle_9_by_9)
        cell_B1 = numbrix.get_cell('B1')
        neighbors_of_cell_B1 = numbrix.get_cell_neighbors(cell_B1)
        print('Neighbors of cell B1:', neighbors_of_cell_B1)

        cell_B1.reduce_neighbors(neighbors_of_cell_B1, numbrix.get_all_values())
        print('Neighbors of cell B2:', neighbors_of_cell_B1)
        cell_B2 = numbrix.get_cell('B2')
        self.assertEqual(3, cell_B2.get_value())

    def test_beginner_puzzle_reduction(self):
        numbrix = Numbrix(beginner_puzzle_9_by_9)
        numbrix.display()

        numbrix.reduce()
        numbrix.display()

        cell_E7 = numbrix.get_cell('E7')
        self.assertFalse(self.is_link_endpoint(cell_E7))

        cell_G6 = numbrix.get_cell('G6')
        self.assertTrue(self.is_link_endpoint(cell_G6))

    def test_find_chain_endpoints(self):
        numbrix = Numbrix(beginner_puzzle_9_by_9)
        numbrix.reduce()
        numbrix.display()

        # By looking at the puzzle produced above, we know that
        # the chain endpoints are: C5, F7, C8, E8
        chain_endpoints = numbrix.get_chain_endpoints()
        print(chain_endpoints)
        chain_endpoint_addresses = [cell.address for cell in chain_endpoints]
        self.assertTrue('C5' in chain_endpoint_addresses)
        self.assertTrue('F7' in chain_endpoint_addresses)
        self.assertTrue('C8' in chain_endpoint_addresses)
        self.assertTrue('E8' in chain_endpoint_addresses)

    def test_get_cell_between(self):
        """Test getting the cell between two cells that are 2 cells apart"""
        numbrix = Numbrix(beginner_puzzle_9_by_9)
        cell_C1 = numbrix.get_cell('C1')
        cell_C2 = numbrix.get_cell('C2')
        cell_C3 = numbrix.get_cell('C3')
        cell_C4 = numbrix.get_cell('C4')
        cell_C5 = numbrix.get_cell('C5')
        cell_A3 = numbrix.get_cell('A3')
        cell_B3 = numbrix.get_cell('B3')
        cell_D3 = numbrix.get_cell('D3')
        cell_E3 = numbrix.get_cell('E3')

        self.assertEqual([cell_C2], numbrix.get_empty_cells_between(cell_C3, cell_C1))
        self.assertEqual([cell_C4], numbrix.get_empty_cells_between(cell_C3, cell_C5))
        self.assertEqual([cell_B3], numbrix.get_empty_cells_between(cell_C3, cell_A3))
        self.assertEqual([cell_D3], numbrix.get_empty_cells_between(cell_C3, cell_E3))

    def test_another_reduction(self):
        numbrix = Numbrix(one_gaps)
        numbrix.display()

        numbrix.reduce()
        numbrix.display()

    def test_hard_puzzle_reduction(self):
        numbrix = Numbrix(very_hard_puzzle)
        numbrix.display()

        numbrix.reduce()
        numbrix.display()

    def test_forced(self):
        Numbrix.interactive_mode = False
        numbrix = Numbrix(all_moves_forced_6_by_6)
        numbrix.display()
        numbrix.populate_all_forced_cells()
        numbrix.display()

        numbrix.is_solved()

    def test_solve_one_cell_gaps(self):
        Numbrix.interactive_mode = False
        numbrix = Numbrix(one_gaps)
        numbrix.display()
        numbrix.populate_all_1_gap_cells()
        numbrix.display()

        cell_H1 = numbrix.get_cell('H1')
        assert cell_H1.get_value() == 22
        cell_A2 = numbrix.get_cell('A2')
        assert cell_A2.get_value() == 2
        cell_I8 = numbrix.get_cell('I8')
        assert cell_I8.get_value() == 80
        cell_B9 = numbrix.get_cell('B9')
        assert cell_B9.get_value() == 68
        cell_H9 = numbrix.get_cell('H9')
        assert cell_H9.get_value() == 78

    def test_forced_and_one_cell_gaps(self):
        Numbrix.interactive_mode = False
        numbrix = Numbrix(one_gaps)
        numbrix.display()
        numbrix.reduce()
        numbrix.display()

    def test_finding_end_points(self):
        Numbrix.interactive_mode = False
        numbrix = Numbrix(one_gaps)
        numbrix.reduce()
        numbrix.display()

        # From the above, the puzzle will be in this state:
        #     |  A  |  B  |  C  |  D  |  E  |  F  |  G  |  H  |  I  |
        # ----‖=====‖=====‖=====‖=====‖=====‖=====‖=====‖=====‖=====‖
        #   1 |  3  |  4  |  9  |     |  17 |     |  21 |  22 |  23 |
        #   2 |  2  |  5  |     |     |     |     |     |  25 |  24 |
        #   3 |  1  |     |     |     |     |     |     |  26 |  27 |
        #   4 |  58 |  57 |     |     |     |     |     |  29 |  28 |
        #   5 |  59 |  60 |     |     |     |     |     |     |  43 |
        #   6 |  62 |  61 |     |     |     |     |     |     |     |
        #   7 |  63 |  64 |     |     |     |     |     |     |  81 |
        #   8 |  66 |  65 |     |     |     |     |     |     |  80 |
        #   9 |  67 |  68 |  69 |     |  73 |     |  77 |  78 |  79 |
        # ----‖=====‖=====‖=====‖=====‖=====‖=====‖=====‖=====‖=====‖
        #
        # and the endpoints should be: C1, G1, B2, B4, H4, I5, C9, G9 (not counting one-cell chains)

        endpoints = [cell.address for cell in numbrix.get_chain_endpoints()]
        print('Endpoints are: ', endpoints)
        assert 'C1' in endpoints

        cell_C1 = numbrix.get_cell('C1')
        smallest_value_distance = numbrix.calculate_smallest_value_difference_to_other_chains(cell_C1)
        assert smallest_value_distance == 4

        paths = numbrix.generate_required_paths()
        print(paths)

    def test_create_endpoint_cell(self):
        numbrix = Numbrix(beginner_puzzle_9_by_9)
        numbrix.reduce()
        numbrix.display()

        endpoint_cell_E3 = Numbrix_Cell('E3', [63])
        cell_F3 = Numbrix_Cell('F3', [])
        cell_E4 = Numbrix_Cell('E4', [])
        cell_D3 = Numbrix_Cell('D3', [18])
        cell_E2 = Numbrix_Cell('E2', [64])
        neighbors_of_E3 = [cell_E4, cell_F3, cell_E2, cell_D3]
        print("Neighbors of E3:", numbrix.get_cell_neighbors(endpoint_cell_E3))

        self.assertEqual(set(neighbors_of_E3), set(numbrix.get_cell_neighbors(endpoint_cell_E3)))

        endpoint_cell_G6 = Numbrix_Cell('G6', [54])
        endpoint_cell_H3 = Numbrix_Cell('H3', [74])
        endpoint_cell_H5 = Numbrix_Cell('H5', [78])

        all_endpoints = [endpoint_cell_H5, endpoint_cell_H3, endpoint_cell_G6, endpoint_cell_E3]
        chain_endpoints = numbrix.get_chain_endpoints()
        self.assertEqual(set(all_endpoints), set(chain_endpoints))

        numbrix.fill_1_cell_gaps()

        all_endpoints = [endpoint_cell_H5, endpoint_cell_H3, endpoint_cell_G6, endpoint_cell_E3]
        chain_endpoints = numbrix.get_chain_endpoints()
        self.assertEqual(set(all_endpoints), set(chain_endpoints))

        numbrix.display()

        cell_G3 = Numbrix_Cell('G3', [])
        cell_H4 = Numbrix_Cell('H4', [])
        expected_guessing_endpoint = Chain_Endpoint(endpoint_cell_H3, [cell_G3, cell_H4], [75], 4, 12)
        actual_guessing_endpoint = numbrix.get_guessing_cell()
        self.assertEqual(expected_guessing_endpoint, actual_guessing_endpoint)

        print("Chain.py Endpoint Guess is:", actual_guessing_endpoint)

    def test_solving_beginner_puzzle(self):
        numbrix = Numbrix(beginner_puzzle_9_by_9)
        numbrix.display()

        solved_puzzle = numbrix.search()
        solved_puzzle.display()
        self.assertTrue(solved_puzzle.is_solved())

    def test_finding_possible_paths(self):
        numbrix = Numbrix(medium_6_by_6)
        numbrix.reduce_forced_cell_only()
        numbrix.display()

        # At this point the state of the puzzle is:
        #     |  A  |  B  |  C  |  D  |  E  |  F  |
        # ----‖=====‖=====‖=====‖=====‖=====‖=====‖
        #   1 |  4  |     |     |     |     |  29 |
        #   2 |     |  2  |  33 |  26 |  27 |     |
        #   3 |     |     |     |     |  24 |     |
        #   4 |     |  36 |     |     |  21 |     |
        #   5 |     |  11 |  12 |  19 |  18 |     |
        #   6 |  9  |     |     |     |     |  16 |
        # ----‖=====‖=====‖=====‖=====‖=====‖=====‖

        paths = numbrix.generate_required_paths()
        for index, path in enumerate(paths):
            print(f'   {index}: {path}')
        # The expected paths are [Path:<length>(start->end)]:
        #    0: Path:2(B2->A1)
        #    1: Path:2(A6->B5)
        #    2: Path:2(F6->E5)
        #    3: Path:2(D5->E4)
        #    4: Path:2(E3->D2)
        #    5: Path:2(E2->F1)
        #    6: Path:3(E4->E3)
        #    7: Path:3(C2->B4)
        #    8: Path:4(C5->F6)
        #    9: Path:4(F1->C2)
        #    10: Path:5(A1->A6)
        assert len(paths) == 11
        # The first path is from B2(2) to A1(4)
        test_path = paths[0]

        # We expect just two routes: B2(2)->B1(3)->A1(4) or B2(2)->A2(3)->A1(4)
        routes = numbrix.generate_possible_routes_for_path(test_path)
        print(f'Routes for path {test_path} are', routes)
        assert len(routes) == 2

        # The ninth path is Path:4(C5->F6)
        test_path = paths[8]

        # We expect just one route: C5(12)->C6(13)->D6(14)->E6(15)->F6(16)
        routes = numbrix.generate_possible_routes_for_path(test_path)
        print(f'Routes for path {test_path} are', routes)
        assert len(routes) == 1

        # The eleventh path is Path:5(A1->A6)
        test_path = paths[10]

        # We expect just one route: A1(4)->A2(5)->A3(6)->A4(7)->A5(8)->A6(9)
        routes = numbrix.generate_possible_routes_for_path(test_path)
        print(f'Routes for path {test_path} are', routes)
        assert len(routes) == 1

        # Now get the route count for each path. There should be some, rough
        # correlation between the value distance of a path and the number of routes.
        print("Path          Value Distance         # of Routes")
        print("------------------------------------------------")
        for path in paths:
            routes = numbrix.generate_possible_routes_for_path(path)
            path.set_routes(routes)
            print(f'{path}    {path.value_distance}     {len(routes)}')

        # Now reduce all paths that have only one valid route:
        numbrix.reduce_paths_with_one_route_option()
        numbrix.display()

    def test_finding_routes_on_puzzle(self):
        # numbrix = Numbrix(very_hard_puzzle)
        numbrix = Numbrix(hard_6_by_6)
        paths = numbrix.generate_required_paths_with_routes()
        Path.print_path_info(paths)
        numbrix.display()

        paths = numbrix.generate_required_paths_with_routes()
        Path.print_path_info(paths)
        numbrix.display()

        forced_path_solved_puzzle = numbrix.solve_one_path_routes()
        forced_path_solved_puzzle.populate_all_forced_cells()
        forced_path_solved_puzzle.display()

        forced_path_solved_puzzle.get_well_bottoms()
        print(forced_path_solved_puzzle.get_remaining_well_bottoms_values())
        forced_path_solved_puzzle.display_as_code()

        if forced_path_solved_puzzle.fill_forced_well_bottom():
            paths = forced_path_solved_puzzle.generate_required_paths_with_routes()
            Path.print_path_info(paths)
            forced_path_solved_puzzle.display()
        forced_path_solved_puzzle.display()

        forced_path_solved_puzzle.populate_all_forced_cells()
        forced_path_solved_puzzle.display()

    # TODO: this is a problem. It finds one well bottom, but not
    # the other, so more work to be done here. No forced cells
    # and no paths here... But, the upper hole can be solved in
    # two different ways! So, it is unlikely to occur in a real
    # puzzle. Maybe the code is okay...
    def test_find_well_bottoms(self):
        puzzle_def = [19, 20, 25, 26, 27, 28,
                      18, 21, 24, None, None, 29,
                      17, 22, 23, None, 33, 30,
                      16, 15, 8, 7, 32, 31,
                      13, 14, 9, 6, 5, None,
                      12, 11, 10, None, None, None]
        numbrix = Numbrix(puzzle_def)
        numbrix.get_well_bottoms()
        print(numbrix.get_remaining_well_bottoms_values())
        numbrix.reduce()
        numbrix.display()

    def test_solving_intermediate_puzzle(self):
        interactive_mode = False

        numbrix = Numbrix(one_gaps, interactive_mode)
        numbrix.display()

        solved_puzzle = numbrix.search()
        if solved_puzzle:
            solved_puzzle.display()
            self.assertTrue(solved_puzzle.is_solved())
        else:
            print("Solver finished, but no solution was found!")
            self.assertTrue(False)

    def test_reducing_medium_6_x_6(self):
        numbrix = Numbrix(medium_6_by_6)
        numbrix.display()

        numbrix.reduce()
        numbrix.display()
        self.assertTrue(numbrix.is_solved())

    def test_reducing_very_hard(self):
        numbrix = Numbrix(very_hard_puzzle)
        numbrix.display()

        numbrix.reduce()
        numbrix.display()
        # self.assertTrue(numbrix.is_solved())

    def test_solving_very_hard_puzzle(self):
        numbrix = Numbrix(very_hard_puzzle)
        numbrix.display()

        solved_puzzle = numbrix.search()
        solved_puzzle.display()
        self.assertTrue(solved_puzzle.is_solved())

    # @unittest.skip
    def test_solving_puzzles(self):
        puzzles = [beginner_puzzle_9_by_9, very_hard_puzzle]
        puzzles = [all_moves_forced_6_by_6]
        puzzles = [easy_4_forced_moves_6_by_6]
        puzzles = [sept_18_puzzle]
        puzzles = [hard_6_by_6]
        puzzles = [medium_6_by_6]
        puzzles = [may_23_puzzle]
        puzzles = [very_hard_6_by_6]
        puzzles = [beginner_puzzle_9_by_9]
        puzzles = [apr_17_2022]
        puzzles = [mar_20_2022]
        puzzles = [very_hard_puzzle]
        puzzles = [may_29_2022_puzzle]

        for puzzle in puzzles:
            numbrix = Numbrix(puzzle, False)
            print('The initial puzzle is:')
            numbrix.display()

            solved_puzzle = numbrix.search()
            if solved_puzzle is None:
                logging.critical('Puzzle was not solved!')
                self.assertTrue(False)
            else:
                solved_puzzle.display()
                self.assertTrue(solved_puzzle.is_solved())
        print('Color key is:')

    def test_logging(self):
        logging.debug('Debug message')
        logging.warning('warning message')
        logging.info('info message')
        logging.error('error message')

    def test_finding_of_extended_holes(self):
        # This puzzle is invalid, but is created when searching for a solution
        puzzle_with_four_holes_and_no_paths = [59, 58, 57, 56, 53, 52, 49, 48, 47,
                                               60, 63, 64, 55, 54, 51, 50, 45, 46,
                                               61, 62, 65, 66, 41, 42, 43, 44, None,
                                               70, 69, 68, 67, 40, 39, None, None, None,
                                               71, 72, None, 34, 35, 38, None, 2, 3,
                                               None, None, 32, 33, 36, 37, 14, 13, 4,
                                               29, 30, 31, 22, 21, 16, 15, 12, 5,
                                               28, 25, 24, 23, 20, 17, 10, 11, 6,
                                               27, 26, None, None, 19, 18, 9, 8, 7]
        numbrix = Numbrix(puzzle_with_four_holes_and_no_paths)
        numbrix.display()

        well_bottom_values = numbrix.get_remaining_well_bottoms_values()
        assert 1 in well_bottom_values
        assert 81 in well_bottom_values

        numbrix.generate_required_paths()
        assert len(numbrix.paths) == 0

        starting_cell = numbrix.get_cell('I3')
        empty_cell_set = numbrix.get_all_connected_empty_cells(starting_cell)
        assert len(empty_cell_set) == 5

        holes = numbrix.get_extended_holes()
        print('puzzle holes are: ')
        for hole in holes:
            print('     ', hole)
        assert len(holes) == 4

    def test_finding_end_paths(self):
        near_complete_puzzle_def = [55, 56, 57, 58, 59, None, None, 76, 75,
                                    54, 53, 52, 61, 60, None, None, 73, 74,
                                    49, 50, 51, 62, 65, 66, None, 72, 71,
                                    48, 37, 36, 63, 64, 67, 68, 69, 70,
                                    47, 38, 35, 34, 33, 32, 31, 30, 29,
                                    46, 39, 6, 5, 4, None, None, None, 28,
                                    45, 40, 7, 16, 17, 18, 19, 26, 27,
                                    44, 41, 8, 15, 14, 13, 20, 25, 24,
                                    43, 42, 9, 10, 11, 12, 21, 22, 23]

        numbrix = Numbrix(near_complete_puzzle_def)
        numbrix.display()
        print('final cells', numbrix.get_final_cells())
        # numbrix.guess_final_cells()
        guesses = numbrix.generate_guesses_for_final_cells()
        print('guesses are', guesses)

        solved_puzzle = numbrix.search()
        if solved_puzzle is None:
            logging.critical('Puzzle was not solved!')
            self.assertTrue(False);
        else:
            solved_puzzle.display()
            self.assertTrue(solved_puzzle.is_solved())


if __name__ == '__main__':
    unittest.main()
