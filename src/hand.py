import typing
from card import LlamaCard

class Hand:
    def __init__(self, cards: list[LlamaCard] = None):
        if cards is None:
            cards = []
        self.cards: list[LlamaCard] = cards

    def playable_cards(self, top_card: LlamaCard) -> list[LlamaCard]:
        """Возвращает список карт, которые можно сыграть на верхнюю карту."""
        return [card for card in self.cards if self.can_play(card, top_card)]

    def can_play(self, card: LlamaCard, top_card: LlamaCard) -> bool:
        """Определяет, может ли карта быть сыграна на верхнюю карту."""
        return card.value == top_card.value  # Убедитесь, что здесь логика соответствует правилам игры

    def __repr__(self):
        return self.save()

    def save(self) -> str:
        """Преобразует руку в строку в формате '3 1 6'."""
        scards = [c.save() for c in self.cards]
        return ' '.join(scards)

    def __eq__(self, other):
        if isinstance(other, Hand):
            return self.cards == other.cards
        elif isinstance(other, str):
            other = Hand.load(other)
            return self.cards == other.cards
        return False

    def add_card(self, card: LlamaCard):
        """Добавляет карту в руку."""
        self.cards.append(card)

    @classmethod
    def load(cls, text: str) -> typing.Self:
        """Преобразует строку в формате '3 1 6' в объект Hand. Возвращает руку."""
        cards = [LlamaCard.load(s) for s in text.split()]
        return cls(cards=cards)

    def remove_card(self, card: LlamaCard):
        """Удаляет карту из руки, если она там есть."""
        try:
            self.cards.remove(card)
        except ValueError:
            print(f"Card {card} not found in hand.")

    def score(self) -> int:
        """Возвращает сумму очков карт в руке."""
        return sum(c.score(self.cards) for c in self.cards)
