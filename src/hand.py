import typing
from src.card import LlamaCard

class Hand:
    def __init__(self, value: list[LlamaCard] = []):
        # Конструктор, принимающий список карт. По умолчанию - пустой список.
        if value is None:
            cards = []

    def __repr__(self):
        # Возвращаем строковое представление объекта, используя метод save
        return self.save()

    def save(self) -> str:
        # Преобразуем каждую карту в строку и объединяем их
        scards=[c.save() for c in self.value]
        s = ' '.join(scards)  # Объединяем список строк в одну строку return s  # Возвращаем строку формата '3 1 6'
        return s
    def __eq__(self, other):
        # Сравниваем текущий объект Hand с другим объектом
        if isinstance(other, str): #Если другой объект - строка, загружаем его как объект Hand other = Hand.load(other)
            return self.value == other.value  # Сравниваем списки карт def add_card(self, card: LlamaCard):
            # Добавляем карту в список карт
            self.value.append(card)

    @classmethod
    def load(cls, text: str) -> typing.Self:
        # Преобразуем строку в список карт и создаем объект Hand
        cards = [LlamaCard.load(s) for s in text.split()]  # Разбиваем строку и загружаем карты
        return cls(value=cards)  # Возвращаем новый объект Hand

    def remove_card(self, card: LlamaCard):
        # Удаляем карту из списка карт
        self.value.remove(card)

    def score(self):
        res = 0
        for c in self.cards:
            res += c.score()
        return res
