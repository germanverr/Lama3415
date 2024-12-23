from abc import ABC, abstractmethod
from typing import List, Optional
from src.card import LlamaCard
from src.hand import Hand
from src.player import Player

class PlayerInteraction(ABC):
    @classmethod
    @abstractmethod
    def choose_card(
            cls, hand: Hand, top: LlamaCard, hand_counts: List[int] | None = None
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
    def choose_quit(
            cls, hand: Hand, top: LlamaCard, hand_counts: List[int] | None = None
    ) -> bool:
        """
        Запрашивает у игрока продолжать играть или закончить игру в раунде.
        :param hand: Объект Hand, представляющий руки игрока.
        :param top: Карта, находящаяся на вершине стека.
        :param hand_counts: Список количества карт у других игроков (если нужно).
        :return: True если заканчиваем раунд.
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
    def inform_card_drawn(cls, current_player: Player, card: LlamaCard):
        # Логика уведомления о вытянутой карте
        print(f"Player {current_player.name} drew {card}")

    @classmethod
    def inform_card_played(cls, player: Player, card: LlamaCard):
        """
        Сообщает, что игрок сыграл карту.
        :param player: Игрок, который сыграл карту.
        :param card: Сыгранная карта.
        """
        print(f"{player.name} has played {card}.")

class ExamplePlayerInteraction(PlayerInteraction):
    @classmethod
    def choose_card(
            cls, hand: Hand, top: LlamaCard, hand_counts: List[int] | None = None
    ) -> LlamaCard:
        playable_cards = hand.playable_cards(top)
        if not playable_cards:
            print(f"No playable cards in hand: {hand}")
            return None

        # Пример: выбираем первую playable карту
        chosen_card = playable_cards[0]
        print(f"Chose card: {chosen_card} from playable cards: {playable_cards}")
        return chosen_card

    def choose_quit(
            cls, hand: Hand, top: LlamaCard, hand_counts: List[int] | None = None
    ) -> bool:
        """Никогда не сдаемся и играем раунд, пока есть физическая возможность."""
        return False

    @classmethod
    def choose_to_play(cls, top: LlamaCard, drawn: LlamaCard) -> bool:
        # Пример: играем карту, если она playable
        return drawn.is_playable(top)
