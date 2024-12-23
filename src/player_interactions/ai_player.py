# src/player_interactions/ai_player.py

import random
from typing import List

from src.player_interaction import PlayerInteraction
from src.card import LlamaCard
from src.hand import Hand
from src.player import Player

class Bot(PlayerInteraction):
    def __init__(self, name: str):
        self.name = name
    @classmethod
    def choose_card(self, hand: Hand, top_card: LlamaCard) -> LlamaCard:
        print(f"Player with hand {hand} can play {hand.playable_cards(top_card)} on top of {top_card}")
        playable_cards = hand.playable_cards(top_card)
        if not playable_cards:
            print(f"Player could not play any card")
            return None
        return playable_cards[0]  # Бот всегда играет первую доступную карту

    @classmethod
    def choose_to_play(cls, top: LlamaCard, drawn: LlamaCard) -> bool:
        return drawn.can_play_on(top)

    @classmethod
    def inform_card_drawn(cls, current_player: Player, card: LlamaCard):
        pass  # Бот не выводит информацию о вытянутой карте

    @classmethod
    def inform_card_played(cls, player: Player, card: LlamaCard):
        pass  # Бот не выводит информацию о сыгранной карте

    def __str__(self):
        return "Bot"

    @classmethod
    def choose_quit(cls, hand: Hand, top: LlamaCard, hand_counts: List[int] | None = None) -> bool:
        return False

