from src.card import LlamaCard
from src.hand import Hand
from src.player import Player
from src.player_interaction import PlayerInteraction

class Human(PlayerInteraction):
    def __init__(self, name: str):
        self.name = name

    def choose_card(self, hand: Hand, top_card: LlamaCard) -> LlamaCard | None:
        playable_cards = hand.playable_cards(top_card)
        if not playable_cards:
            return None

        print(f"Вы можете сыграть: {playable_cards}")
        while True:
            try:
                choice = int(input("Введите номер карты, которую хотите выбрать: ")) - 1
                if 0 <= choice < len(playable_cards):
                    return playable_cards[choice]
                else:
                    print("Неверная карта. Попробуйте снова.")
            except ValueError:
                print("Пожалуйста, введите корректное число.")

    def choose_to_play(self, top_card: LlamaCard, card: LlamaCard) -> bool:
        while True:
            choice = input(f"Хотите ли вы сыграть карту {card}? (y/n): ").lower()
            if choice == 'y':
                return True
            elif choice == 'n':
                return False
            else:
                print("Пожалуйста, введите 'y' или 'n'.")

    def inform_card_played(self, player: Player, card: LlamaCard):
        print(f"{player.name} сыграл карту: {card}")

    def inform_card_drawn(self, player: Player, card: LlamaCard):
        print(f"{player.name} вытянул карту: {card}")
