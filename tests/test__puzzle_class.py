import unittest
import Sudoku_Puzzle


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

    def test_something(self):
        puzzle = Sudoku_Puzzle.Sudoku_Puzzle(self.sudoku_4x4_string)
        puzzle.display()
        print('Puzzle created')


if __name__ == '__main__':
    unittest.main()
