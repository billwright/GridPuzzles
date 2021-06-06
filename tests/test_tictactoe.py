import unittest
from TicTacToe import TicTacToe
from Random_Player import Random_Player
from Position_Evaluator_Player import Position_Evaluator_Player
from Human_Player import Human_Player


class TestTicTacToe(unittest.TestCase):

    def test_display_board(self):
        tictactoe = TicTacToe(3)
        tictactoe.display()

        human_player = Human_Player(Human_Player.get_user_name(), 'X')
        self.assertIsNotNone(human_player.name)

    def test_making_moves(self):
        tictactoe = TicTacToe(3)
        tictactoe.display()

        player_x = Random_Player('robot', 'X')
        tictactoe.current_player = player_x
        tictactoe.make_move('A1')
        tictactoe.make_move('C1')

        player_o = Random_Player('robot', 'O')
        tictactoe.current_player = player_o
        tictactoe.make_move('B2')
        tictactoe.make_move('C3')
        tictactoe.display()

    def test_diagonal_group_creation(self):
        tictactoe = TicTacToe(3)
        diagonal_groups = tictactoe.create_diagonal_groups()

        print(diagonal_groups)
        self.assertEqual(2, len(diagonal_groups))

    def test_play_game(self):
        TicTacToe.start_human_vs_random(3)

    # This test should return a random collection of winners and cat games
    def test_random_vs_random(self):
        player1 = Random_Player('Alice Guess', 'X')
        player2 = Random_Player('Bob Random', 'O')
        game = TicTacToe(3)
        game.play_game(player1, player2)

    # In this test the evaluator (Smart Sally) should win nearly every game (maybe some cat games)
    def test_random_vs_evaluator(self):
        player1 = Position_Evaluator_Player('Smart Sally', 'X')
        player2 = Random_Player('Bob Random', 'O')
        game = TicTacToe(3)
        game.play_game(player1, player2)

    # This should always end in a cat game
    def test_evaluator_vs_evaluator(self):
        player1 = Position_Evaluator_Player('Smart Sally', 'X')
        player2 = Position_Evaluator_Player('Brilliant Bob', 'O')

        number_of_games = 10
        number_of_cat_games = 0
        for i in range(number_of_games):
            game = TicTacToe(3)
            game.play_game(player1, player2)
            if game.winner is None:
                number_of_cat_games += 1
        assert number_of_cat_games == number_of_games


if __name__ == '__main__':
    unittest.main()
