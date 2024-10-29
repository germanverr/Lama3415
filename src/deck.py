import random
import typing
from src.card import LlamaCard

class Deck:
    def __init__(self, cards: typing.Optional[list[LlamaCard]] = None):
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
        """Сохраняет колоду в строковом формате."""
        scards = [c.save() for c in self.cards]
        return " ".join(scards)

    @classmethod
    def load(cls, text: str) -> typing.Self:
        """Загружает колоду из строкового формата."""
        cards = [LlamaCard.load(s) for s in text.split()]
        return cls(cards=cards)

    def draw_card(self) -> LlamaCard:
        """Берет карту из колоды и возвращает её. Если колода пуста, выбрасывает исключение."""
        if not self.cards:
            raise ValueError("Cannot draw from an empty deck.")
        return self.cards.pop()

    def shuffle(self):
        """Перемешивает карты в колоде."""
        random.shuffle(self.cards)

    def is_empty(self) -> bool:
        """Проверяет, пуста ли колода."""
        return len(self.cards) == 0


