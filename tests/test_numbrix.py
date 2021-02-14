import unittest
from Numbrix import Numbrix
from Numbrix_Cell import Numbrix_Cell
from Chain_Endpoint import Chain_Endpoint

beginner_puzzle = [5, 6, 7, 8, 9, 24, 25, 30, 31,
                   4, None, None, None, None, None, None, None, 32,
                   15, None, None, None, None, None, None, None, 33,
                   16, None, None, None, None, None, None, None, 34,
                   65, None, None, None, None, None, None, None, 39,
                   66, None, None, None, None, None, None, None, 40,
                   69, None, None, None, None, None, None, None, 45,
                   70, None, None, None, None, None, None, None, 46,
                   71, 72, 81, 80, 79, 52, 51, 48, 47]

dec_27_2020 = [3, None, 9, None, 17, None, 21, None, 23,
               None, None, None, None, None, None, None, None, None,
               1, None, None, None, None, None, None, None, 27,
               None, None, None, None, None, None, None, None, None,
               59, None, None, None, None, None, None, None, 43,
               None, None, None, None, None, None, None, None, None,
               63, None, None, None, None, None, None, None, 81,
               None, None, None, None, None, None, None, None, None,
               67, None, 69, None, 73, None, 77, None, 79]

very_hard_puzzle = [55, None, 61, None, 69, None, 79, None, 77,
                    None, None, None, None, None, None, None, None, None,
                    53, None, None, None, None, None, None, None, 75,
                    None, None, None, None, None, None, None, None, None,
                    47, None, None, None, None, None, None, None, 31,
                    None, None, None, None, None, None, None, None, None,
                    45, None, None, None, None, None, None, None, 17,
                    None, None, None, None, None, None, None, None, None,
                    5, None, 7, None, 9, None, 13, None, 15]


# noinspection PyPep8Naming
class TestNumbrix(unittest.TestCase):

    def test_creation(self):
        numbrix = Numbrix(beginner_puzzle)
        self.assertIsNotNone(numbrix)
        numbrix.display()

    def test_get_neighbors(self):
        numbrix = Numbrix(beginner_puzzle)
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
        numbrix = Numbrix(beginner_puzzle)
        cell_B1 = numbrix.get_cell('B1')
        neighbors_of_cell_B1 = numbrix.get_cell_neighbors(cell_B1)
        print('Neighbors of cell B1:', neighbors_of_cell_B1)

        cell_B1.reduce_neighbors(neighbors_of_cell_B1)
        print('Neighbors of cell B2:', neighbors_of_cell_B1)
        cell_B2 = numbrix.get_cell('B2')
        self.assertEqual(3, cell_B2.get_value())

    def test_beginner_puzzle_reduction(self):
        numbrix = Numbrix(beginner_puzzle)
        numbrix.display()

        numbrix.reduce()
        numbrix.display()

        cell_E7 = numbrix.get_cell('E7')
        neighbors_of_cell_E7 = numbrix.get_cell_neighbors(cell_E7)
        self.assertFalse(cell_E7.is_link_endpoint(neighbors_of_cell_E7))

        cell_G6 = numbrix.get_cell('G6')
        neighbors_of_cell_G6 = numbrix.get_cell_neighbors(cell_G6)
        self.assertTrue(cell_G6.is_link_endpoint(neighbors_of_cell_G6))

    def test_find_chain_endpoints(self):
        numbrix = Numbrix(beginner_puzzle)
        numbrix.reduce()
        numbrix.display()

        # By looking at the puzzle produced above, we know that
        # the chain endpoints are: D4, D6, E3, G6, H3, H5
        chain_endpoints = numbrix.get_chain_endpoints()
        print(chain_endpoints)
        chain_endpoint_addresses = [cell.address for cell in chain_endpoints]
        self.assertTrue('D4' in chain_endpoint_addresses)
        self.assertTrue('D6' in chain_endpoint_addresses)
        self.assertTrue('E3' in chain_endpoint_addresses)
        self.assertTrue('G6' in chain_endpoint_addresses)
        self.assertTrue('H3' in chain_endpoint_addresses)
        self.assertTrue('H5' in chain_endpoint_addresses)

    def test_get_cell_between(self):
        """Test getting the cell between two cells that are 2 cells apart"""
        numbrix = Numbrix(beginner_puzzle)
        cell_C1 = numbrix.get_cell('C1')
        cell_C2 = numbrix.get_cell('C2')
        cell_C3 = numbrix.get_cell('C3')
        cell_C4 = numbrix.get_cell('C4')
        cell_C5 = numbrix.get_cell('C5')
        cell_A3 = numbrix.get_cell('A3')
        cell_B3 = numbrix.get_cell('B3')
        cell_D3 = numbrix.get_cell('D3')
        cell_E3 = numbrix.get_cell('E3')

        self.assertEqual(cell_C2, numbrix.get_cell_between(cell_C3, cell_C1))
        self.assertEqual(cell_C4, numbrix.get_cell_between(cell_C3, cell_C5))
        self.assertEqual(cell_B3, numbrix.get_cell_between(cell_C3, cell_A3))
        self.assertEqual(cell_D3, numbrix.get_cell_between(cell_C3, cell_E3))

    def test_another_reduction(self):
        numbrix = Numbrix(dec_27_2020)
        numbrix.display()

        numbrix.reduce()
        numbrix.display()

    def test_hard_puzzle_reduction(self):
        numbrix = Numbrix(very_hard_puzzle)
        numbrix.display()

        numbrix.reduce()
        numbrix.display()

    def test_solve_one_cell_gaps(self):
        numbrix = Numbrix(beginner_puzzle)
        numbrix.reduce()
        numbrix.display()

        # By looking at the puzzle produced above, we know that
        # the chain endpoints are: D4, D6, E3, G6, H3, H5
        numbrix.fill_1_cell_gaps()
        numbrix.display()

        cell_D5 = numbrix.get_cell('D5')
        self.assertEqual(20, cell_D5.get_value())

    def test_create_endpoint_cell(self):
        numbrix = Numbrix(beginner_puzzle)
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

        endpoint_cell_D4 = Numbrix_Cell('D4', [19])
        endpoint_cell_D6 = Numbrix_Cell('D6', [21])
        endpoint_cell_G6 = Numbrix_Cell('G6', [54])
        endpoint_cell_H3 = Numbrix_Cell('H3', [74])
        endpoint_cell_H5 = Numbrix_Cell('H5', [78])

        all_endpoints = [endpoint_cell_H5, endpoint_cell_H3, endpoint_cell_G6, endpoint_cell_E3, endpoint_cell_D6, endpoint_cell_D4]
        chain_endpoints = numbrix.get_chain_endpoints()
        self.assertEqual(set(all_endpoints), set(chain_endpoints))

        numbrix.fill_1_cell_gaps()

        all_endpoints = [endpoint_cell_H5, endpoint_cell_H3, endpoint_cell_G6, endpoint_cell_E3]
        chain_endpoints = numbrix.get_chain_endpoints()
        self.assertEqual(set(all_endpoints), set(chain_endpoints))

        numbrix.display()

        cell_G3 = Numbrix_Cell('G3', [])
        cell_H4 = Numbrix_Cell('H4', [])
        expected_guessing_endpoint = Chain_Endpoint(endpoint_cell_H3, [cell_G3, cell_H4], 75, 4)
        actual_guessing_endpoint = numbrix.get_guessing_cell()
        self.assertEqual(expected_guessing_endpoint, actual_guessing_endpoint)

        print("Chain Endpoint Guess is:", actual_guessing_endpoint)

    def test_solving_beginner_puzzle(self):
        numbrix = Numbrix(beginner_puzzle)
        numbrix.display()

        solved_puzzle = numbrix.search()
        solved_puzzle.display()
        self.assertTrue(solved_puzzle.is_solved())

    def test_solving_intermediate_puzzle(self):
        numbrix = Numbrix(dec_27_2020)
        numbrix.display()

        solved_puzzle = numbrix.search()
        solved_puzzle.display()
        self.assertTrue(solved_puzzle.is_solved())

    def test_solving_very_hard_puzzle(self):
        numbrix = Numbrix(very_hard_puzzle)
        numbrix.display()

        solved_puzzle = numbrix.search()
        solved_puzzle.display()
        self.assertTrue(solved_puzzle.is_solved())

    @unittest.skip
    def test_solving_puzzles(self):
        puzzles = [beginner_puzzle, dec_27_2020, very_hard_puzzle]
        for puzzle in puzzles:
            numbrix = Numbrix(puzzle)
            numbrix.display()

            solved_puzzle = numbrix.search()
            solved_puzzle.display()
            self.assertTrue(solved_puzzle.is_solved())


if __name__ == '__main__':
    unittest.main()
