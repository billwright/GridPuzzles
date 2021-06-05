from Player import Player


class Position_Evaluator_Player(Player):

    def get_move(self, game_state):
        open_locations = game_state.get_open_locations()
        best_move = open_locations[0]
        best_score = self.calculate_location_score(best_move, game_state)
        for location in open_locations:
            location_score = self.calculate_location_score(location, game_state)
            if location_score > best_score:
                best_score = location_score
                best_move = location
        return best_move

    def calculate_location_score(self, location, game_state):
        groups = game_state.get_groups_for_cell(location)
        total_score = 0
        for group in groups:
            total_score += self.calculate_group_score(group)
        if game_state.is_corner_or_middle(location):
            total_score += 75
        print('score for location', location, 'is', total_score)
        return total_score

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
