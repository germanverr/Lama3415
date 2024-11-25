from abc import ABC, abstractmethod
from src.card import LlamaCard
from src.hand import Hand
from src.player import Player

class PlayerInteraction(ABC):
    @classmethod
    @abstractmethod
    def choose_card(
            cls, hand: Hand, top: LlamaCard, hand_counts: list[int] | None = None
    ) -> LlamaCard:
        """
        Запрашивает у игрока выбор карты из руки.
        :param hand: Объект Hand, представляющий руки игрока.
        :param top: Карта, находящаяся на вершине стека.
        :param hand_counts: Список количества карт у других игроков (если нужно).
        :return: Выбранная карта.
        """
        pass

    @classmethod
    @abstractmethod
    def choose_to_play(cls, top: LlamaCard, drawn: LlamaCard) -> bool:
        """
        Принимает решение играть или не играть взятую из колоды карту.
        :param top: Карта на вершине стека.
        :param drawn: Карта, которую игрок только что взял.
        :return: True, если игрок хочет сыграть, иначе False.
        """
        pass

    @classmethod
    def inform_card_drawn(cls, player: Player):
        """
        Сообщает, что игрок взял карту.
        :param player: Игрок, который взял карту.
        """
        print(f"{player.name} has drawn a card.")

    @classmethod
    def inform_card_played(cls, player: Player, card: LlamaCard):
        """
        Сообщает, что игрок сыграл карту.
        :param player: Игрок, который сыграл карту.
        :param card: Сыгранная карта.
        """
        print(f"{player.name} has played {card}.")
