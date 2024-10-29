import random
import typing

from src.card import LlamaCard


class Deck:
    def __init__(self, cards: None | list[LlamaCard]):
        if cards is None:
            # создание новой колоды
            cards = LlamaCard.all_cards()
            random.shuffle(cards)
        self.cards: list[LlamaCard] = cards

    def __repr__(self):
        return self.save()

    def __eq__(self, other):
        if isinstance(other, str):
            other = Deck.load(other)
        return self.cards == other.cards

    def save(self) -> str:
        scards = [c.save() for c in self.cards]
        s = " ".join(scards)
        return s

    @classmethod
    def load(cls, text: str) -> typing.Self:
        cards = [LlamaCard.load(s) for s in text.split()]
        return cls(cards=cards)

    def draw_card(self):
        """Берем карту из колоды и возвращаем ее."""
        return self.cards.pop()

    def shuffle(self):
        random.shuffle(self.cards)


