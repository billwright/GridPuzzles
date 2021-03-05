from Grid_Puzzle import Grid_Puzzle
from Group import Group
from TicTacToe_Cell import TicTacToe_Cell

from termcolor import colored
from random import random
from random import randrange


class TicTacToe(Grid_Puzzle):

    user_name = None

    def __init__(self, board_size):
        self.current_player = None
        self.winner = None
        super().__init__(board_size)
        self.diagonal_groups = self.create_diagonal_groups()

    def validate(self):
        pass    # Required by superclass

    def create_puzzle(self):
        cell_dictionary = {}
        for row in self.row_names:
            for column in self.column_names:
                cell_dictionary[column+row] = TicTacToe_Cell(column+row, '')
        return cell_dictionary

    def get_display_cell_width(self):
        return 3

    def get_display_cell(self, cell):
        attributes = []
        if cell.value == 'X':
            cell_color = 'blue'
        elif cell.value == 'O':
            cell_color = 'green'
        else:
            cell_color = 'magenta'
        return colored(cell.value.center(self.get_display_cell_width()), cell_color, attrs=attributes)

    def get_display_row(self, row_name):
        """"Return a string representation of the specified row"""
        row_string = ''
        for col_name in self.column_names:
            cell_address = col_name + row_name
            cell = self.get_cell(cell_address)
            row_string += self.get_display_cell(cell)
            row_string += '|'
        return row_name.rjust(3) + ' |' + row_string

    def display(self):
        print()
        print(self.get_display_header())
        print(self.get_horizontal_puzzle_boundary())

        for row_name in self.row_names:
            print(self.get_display_row(row_name))
        print(self.get_horizontal_puzzle_boundary())

    def calculate_size(self):
        return self.definition

    @staticmethod
    def get_user_name():
        TicTacToe.user_name = input('Please enter your name: ')

    def determine_starting_player(self):
        print(f"Hi, {self.user_name}. Let's flip a coin to see who goes first.")
        heads_or_tails = input("Type 'h' for Heads and 't' for Tails: ")
        coin_flip = random()
        if coin_flip >= 0.5:
            print("\nt was heads.")
            if heads_or_tails.capitalize() == 'H':
                print('You chose heads, so you go first')
                self.current_player = 'X'
            else:
                print('You chose tails, so I will go first')
                self.current_player = 'O'
        else:
            print("\nIt was tails.")
            if heads_or_tails.capitalize() == 'H':
                print('You chose heads, so I will go first')
                self.current_player = 'O'
            else:
                print('You chose tails, so you go first')
                self.current_player = 'X'

    def get_valid_move(self):
        while True:
            move_address = input("\nEnter your move (column first, e.g. A1 or C3): ").capitalize()
            if len(move_address) != 2:
                print("Invalid move. Your move should be just two characters long.")
                continue
            if move_address[0] not in self.column_names:
                print("Invalid move. The first character needs to be one of: ", self.column_names)
                continue
            if move_address[1] not in self.row_names:
                print("Invalid move. The second character needs to be one of: ", self.row_names)
                continue
            if not self.puzzle_dict[move_address].is_open():
                print("Invalid move. That location is already taken.")
                continue
            return move_address

    def create_diagonal_groups(self):
        down_and_right_group = []
        for row_number, column_name in enumerate(self.column_names, 1):
            down_and_right_group.append(self.get_cell(column_name + str(row_number)))

        up_and_right_group = []
        for row_number, column_name in enumerate(self.column_names, 0):
            up_and_right_group.append(self.get_cell(column_name + str(self.size - row_number)))

        return [Group('Down and Right Diagonal', down_and_right_group), Group('Up and Right Diagonal', up_and_right_group)]

    def get_all_groups(self):
        return self.row_groups + self.column_groups + self.diagonal_groups

    def game_is_over(self):
        # Check for horizontal winner
        for group in self.get_all_groups():
            if group.cells[0].is_open():
                continue
            group_values = [cell.value for cell in group.cells]
            # If all the values are the same and they are not open, then this player has won
            if len(set(group_values)) == 1:
                self.winner = group.cells[0].value
                return True

        return len(self.get_open_locations()) == 0

    def make_move(self, address):
        self.puzzle_dict[address].value = self.current_player

    def make_computer_move(self):
        # return self.make_random_move()
        return self.make_evaluated_move()

    def get_open_locations(self):
        return [cell for cell in self.get_all_cells() if cell.is_open()]

    def make_evaluated_move(self):
        open_locations = self.get_open_locations()
        best_move = open_locations[0]
        best_score = self.calculate_location_score(best_move)
        for location in open_locations:
            location_score = self.calculate_location_score(location)
            if location_score > best_score:
                best_score = location_score
                best_move = location
        best_move.value = 'O'

    def calculate_location_score(self, location):
        groups = self.get_groups_for_cell(location)
        total_score = 0
        for group in groups:
            total_score += self.calculate_group_score(group)
        if self.is_corner_or_middle(location):
            total_score += 75
        print('score for location', location, 'is', total_score)
        return total_score

    def is_corner_or_middle(self, location):
        col_number = location.get_column_number()
        if location.get_row_number() == location.get_column_number():
            return True
        if location.get_column_number() == 1 and location.get_row_number() == self.size:
            return True
        if location.get_row_number() == 1 and location.get_column_number() == self.size:
            return True
        return False

    @staticmethod
    def calculate_group_score(group):
        group_score = 0
        number_of_ohs = len([cell for cell in group.cells if cell.value == 'O'])
        if number_of_ohs == 2:
            group_score = 10000
        elif number_of_ohs == 1:
            group_score = 50
        number_of_exs = len([cell for cell in group.cells if cell.value == 'X'])
        if number_of_exs == 2:
            group_score += 10000
        if number_of_exs == 1:
            group_score -= 50
        return group_score

    def make_random_move(self):
        open_locations = self.get_open_locations()
        if len(open_locations) == 1:
            open_locations[0].value = 'O'
        else:
            selection = randrange(1, len(open_locations))
            open_locations[selection].value = 'O'

    def switch_player(self):
        if self.current_player == 'X':
            self.current_player = 'O'
        else:
            self.current_player = 'X'

    @staticmethod
    def start(size=3):
        TicTacToe.get_user_name()
        play_again = True
        while play_again:
            tictactoe = TicTacToe(size)
            tictactoe.play_game()
            play_again = TicTacToe.ask_to_play_again()
        print(f"\nThanks for playing, {TicTacToe.user_name}. Bye.")

    @staticmethod
    def ask_to_play_again():
        answer = input("\nWould you like to play again? (y or n): ")
        return answer.capitalize() == 'Y'

    def display_results(self):
        self.display()
        if self.winner == 'X':
            print("\nYou won! Great job. I'll get you next time.")
        elif self.winner == 'O':
            print("\nI won, but you'll get me next time. I've got confidence in you.")
        else:
            print("Cat game! No one won. We are both too good to make a mistake.")

    def play_game(self):
        self.determine_starting_player()
        while not self.game_is_over():
            if self.current_player == 'X':
                self.display()
                move = self.get_valid_move()
                self.make_move(move)
            else:
                self.make_computer_move()
            self.switch_player()
        self.display_results()
