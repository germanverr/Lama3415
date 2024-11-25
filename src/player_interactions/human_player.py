# src/player_interactions/human_player.py

class Human:
    def __init__(self, name):
        self.name = name

    def make_move(self, game_state):
        move = input(f"{self.name}, введите ваш ход: ")
        return move

    def __str__(self):
        return self.name
