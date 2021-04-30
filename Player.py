class Player:

    def __init__(self, name=None, marker=None):
        self.name = name
        self.marker = marker

    def get_name(self):
        return self.name

    def get_move(self, game_state):
        raise NotImplementedError('Subclass must implement this method!')


