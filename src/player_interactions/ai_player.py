# src/player_interactions/ai_player.py

import random

class Bot:
    def __init__(self, name="AI Player"):
        self.name = name

    def make_move(self, game_state):
        # Простой алгоритм выбора хода
        possible_moves = game_state.get_possible_moves()
        return random.choice(possible_moves) if possible_moves else None

    def __str__(self):
        return self.name
