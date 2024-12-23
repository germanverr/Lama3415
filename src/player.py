import hashlib
import json
import typing
from src.hand import Hand

class Player:
    def __init__(self, name: str, hand: Hand, score: int = 0):
        self.name = name
        self.hand = hand
        self.score = score
        self.__quit: bool = False   # игрок перестал ходить в этом раунде

    @property
    def quit(self):
        return self.__quit
    @quit.setter
    def quit(self, value):
        self.__quit = value

    def __str__(self):
        return f"{self.name}({self.score}): {self.hand}"

    def __eq__(self, other: typing.Self | str | dict):
        if isinstance(other, str):
            other = self.load(json.loads(other))
        if isinstance(other, dict):
            other = self.load(other)
        return (
            self.name == other.name
            and self.score == other.score
            and self.hand == other.hand
        )

    def __hash__(self) -> int:
        return int(hashlib.sha1(self.name.encode("utf-8")).hexdigest(), 16) % (10**8)

    def save(self) -> dict:
        return {
            "name": self.name,
            "hand": self.hand.save(),  # Сохраняем руку как строку
            "score": self.score
        }

    @classmethod
    def load(cls, data: dict):
        return cls(
            name=data["name"],
            hand=Hand.load(data["hand"]),  # Загружаем руку из строки
            score=int(data["score"])
        )
    def add_score(self, points: int):
        # Метод для добавления очков игроку
        self.score += points

    def remove_score(self, points: int):
        # Метод для удаления очков у игрока
        self.score = max(0, self.score - points)
