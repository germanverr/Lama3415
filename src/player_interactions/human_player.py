# src/player_interactions/human_player.py

class Human:
    def __init__(self, name):
        self.name = name
    def make_move(self, game_state):
        move = input(f"{self.name}, введите ваш ход: ")
        return move

    def choose_card(self, hand, top_card):
        print(f"Ваша рука: {hand}")
        print(f"Верхняя карта: {top_card}")
        card_index = int(input("Введите номер карты, которую хотите выбрать: "))
        return hand.cards[card_index - 1]

    def inform_card_drawn(self, card):
        print(f"{self.name} вытянул карту: {card}")

    def __str__(self):
        return self.name

