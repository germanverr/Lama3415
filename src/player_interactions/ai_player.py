import random
from src.player_interaction import PlayerInteraction
from src.card import LlamaCard
from src.hand import Hand
from src.player import Player

class Bot(PlayerInteraction):
    def __init__(self, name: str):
        self.name = name

    def choose_card(self, hand: Hand, top_card: LlamaCard) -> LlamaCard | None:
        print(f"Player {self.name} with hand {hand} can play {hand.playable_cards(top_card)} on top of {top_card}")
        playable_cards = hand.playable_cards(top_card)
        if not playable_cards:
            print(f"Player {self.name} could not play any card")
            return None
        return playable_cards[0]  # Бот всегда играет первую доступную карту

    def choose_to_play(self, top_card: LlamaCard, drawn_card: LlamaCard) -> bool:
        return drawn_card.can_play_on(top_card)

    def inform_card_drawn(self, player: Player, card: LlamaCard):
        pass  # Бот не выводит информацию о вытянутой карте

    def inform_card_played(self, player: Player, card: LlamaCard):
        pass  # Бот не выводит информацию о сыгранной карте

    def __str__(self):
        return "Bot"
