import typing
from card import LlamaCard

class Hand:
    def __init__(self, cards: list[LlamaCard] = None):
        # Используем None вместо пустого списка по умолчанию, чтобы избежать проблем с изменяемыми объектами
        if cards is None:
            cards = []
        self.cards: list[LlamaCard] = cards

    def __repr__(self):
        return self.save()

    def save(self) -> str:
        """Преобразует руку в строку в формате '3 1 6'."""
        scards = [c.save() for c in self.cards]  # ['3', '1', '6']
        s = ' '.join(scards)
        return s

    def __eq__(self, other):
        if isinstance(other, str):
            other = Hand.load(other)
        return self.cards == other.cards

    def add_card(self, card: LlamaCard):
        """Добавляет карту в руку."""
        self.cards.append(card)

    @classmethod
    def load(cls, text: str) -> typing.Self:
        """Преобразует строку в формате '3 1 6' в объект Hand. Возвращает руку."""
        cards = [LlamaCard.load(s) for s in text.split()]
        return cls(cards=cards)

    def remove_card(self, card: LlamaCard):
        """Удаляет карту из руки."""
        self.cards.remove(card)

    def score(self) -> int:
        """Возвращает сумму очков карт в руке."""
        res = 0
        for c in self.cards:
            res += c.score(self.cards)  # Передаем текущую руку для проверки дубликатов
        return res

