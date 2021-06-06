from Player import Player


class Human_Player(Player):

    def __init__(self, name, marker):
        self.name = name
        self.marker = marker

    def get_move(self, game_state):
        while True:
            move_address = input("\nEnter your move (column first, e.g. A1 or C3): ").capitalize()
            if len(move_address) != 2:
                print("Invalid move. Your move should be just two characters long.")
                continue
            if move_address[0] not in game_state.column_names:
                print("Invalid move. The first character needs to be one of: ", game_state.column_names)
                continue
            if move_address[1] not in game_state.row_names:
                print("Invalid move. The second character needs to be one of: ", game_state.row_names)
                continue
            if not game_state.puzzle_dict[move_address].is_open():
                print("Invalid move. That location is already taken.")
                continue
            return game_state.puzzle_dict[move_address]

    @staticmethod
    def get_user_name():
        return input('Please enter your name: ')