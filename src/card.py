from typing import Self

class LlamaCard:
    VALUES = list(range(1, 7)) + [0]  # возможные значения карт (1-6 и 0 для "Ламы")
    LLAMA = 0  # значение для карты "Лама"
    def __init__(self, value: int):
        """value (int): Номинальное значение карты."""
        # инициализация карты с проверкой значения
        if value not in LlamaCard.VALUES:
            raise ValueError
        self.value = value

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        # сравнение карт
        if isinstance(other, int):
            other = LlamaCard(value=other)
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def save(self):
        return repr(self)

    @staticmethod
    def load(text: str):
        return LlamaCard(value=int(text))

    def can_play_on(self, other: Self) -> bool:
        #Метод возвращает логическое значение, указывающее, можно ли сыграть текущую карту (self) на другую карту (other).

        if self.value == other.value or self.value == other.value + 1:
            return True
        if self.value == LlamaCard.LLAMA:
            return other.value == 6 or other.value == LlamaCard.LLAMA
        if other.value == LlamaCard.LLAMA:
            return self.value == 1 or self.value == LlamaCard.LLAMA
        return False

    @staticmethod
    def all_cards():
        # создание всех возможных карт
        cards = []
        for val in LlamaCard.VALUES:
            cards.extend([LlamaCard(value=val) for _ in range(8)])  # Создаем 8 карт для каждого значения
        return cards

    def score(self, cards):
        """
        Возвращает очки карты на основе переданного списка карт.
        Если карта является дубликатом (т.е. она появляется более одного раза в списке карт),
        то очки равны 0. В противном случае очки равны номинальному значению карты.
        :param cards: cards (list[Card]): Список карт для проверки на дубликаты.
        :return: int: Очки карты.
        """

        # штрафные очки за карту
        if self.value == LlamaCard.LLAMA:
            return 10
        elif cards.count(self) > 1:  # Если карта является дубликатом, возвращаем 0
            return 0
        else:  # В противном случае возвращаем номинальное значение карты
            return self.value