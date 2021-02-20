import unittest
from TicTacToe import TicTacToe


class TestTicTacToe(unittest.TestCase):

    def test_display_board(self):
        tictactoe = TicTacToe(3)
        tictactoe.display()

        tictactoe.get_user_name()
        self.assertIsNotNone(tictactoe.user_name)

    def test_making_moves(self):
        tictactoe = TicTacToe(3)
        tictactoe.display()

        tictactoe.current_player = 'X'
        tictactoe.make_move('A1')
        tictactoe.make_move('C1')
        tictactoe.current_player = 'O'
        tictactoe.make_move('B2')
        tictactoe.make_move('C3')
        tictactoe.display()

    def test_diagonal_group_creation(self):
        tictactoe = TicTacToe(3)
        diagonal_groups = tictactoe.create_diagonal_groups()

        print(diagonal_groups)
        self.assertEqual(2, len(diagonal_groups))

    def test_play_game(self):
        TicTacToe.start(3)


if __name__ == '__main__':
    unittest.main()
