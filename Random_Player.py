from Player import Player
from random import randrange


class Random_Player(Player):

    def get_move(self, game_state):
        open_locations = game_state.get_open_locations()
        selection = randrange(1, len(open_locations) + 1)
        open_locations[selection]

