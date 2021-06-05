from Player import Player
from random import randrange


class Random_Player(Player):

    def __repr__(self):
        return f'Random {self.name}'

    def get_move(self, game_state):
        open_locations = game_state.get_open_locations()
        selection = randrange(0, len(open_locations))
        return open_locations[selection]

