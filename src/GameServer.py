import inspect
import json
import sys
from pathlib import Path
from typing import Dict

from src.deck import Deck
from src.game_state import GameState
from src.hand import Hand
from src.player import Player
from src.player_interaction import PlayerInteraction
from src.player_interactions.init import all_player_types
from src.ui.event import post_event, CustomEvent

import logging
import enum


class GamePhase(enum.StrEnum):
    # Перечисление для различных фаз игры
    CHOOSE_CARD = "Choose card"  # Фаза выбора карты
    DRAW_EXTRA = "Draw extra card"  # Фаза вытягивания дополнительной карты
    CHOOSE_CARD_AGAIN = "Choose card again"  # Фаза повторного выбора карты
    NEXT_PLAYER = "Switch current player"  # Фаза переключения на следующего игрока
    DECLARE_WINNER = "Declare a winner"  # Фаза объявления победителя
    GAME_END = "Game ended"  # Фаза окончания игры


class GameServer:
    INITIAL_HAND_SIZE = 6

    def __init__(self, player_types: Dict[Player, PlayerInteraction], game_state: GameState):
        self.game_state: GameState = game_state
        self.player_types: Dict[Player, PlayerInteraction] = player_types  # {player: PlayerInteractions}
        self.current_phase = GamePhase.CHOOSE_CARD  # Устанавливаем начальную фазу игры

    @classmethod
    def load_game(cls, filename: str | Path):
        # Метод для загрузки игры из файла
        with open(filename, 'r') as fin:
            data = json.load(fin)
            game_state = GameState.load(data)
            player_types = {}
            # Создаем словарь игроков и их типов
            for player, player_data in zip(game_state.players, data['players']):
                kind = player_data['kind']
                kind = getattr(all_player_types, kind)
                player_types[player] = kind
            return cls(player_types=player_types, game_state=game_state)

    def save(self, filename: str | Path):
        # Метод для сохранения состояния игры в файл
        data = self.save_to_dict()
        with open(filename, 'w') as fout:
            json.dump(data, fout, indent=4)

    def save_to_dict(self):
        # Метод для преобразования состояния игры в словарь
        data = self.game_state.save()
        for player_index, player in enumerate(self.player_types.keys()):
            player_interaction = self.player_types[player]
            data['players'][player_index]['kind'] = self.player_types[player].__name__
        return data


    @classmethod
    def new_game(cls, player_types: Dict[Player, PlayerInteraction]):
        # Метод для создания новой игры
        deck = Deck()
        game_state = GameState(list(player_types.keys()), deck, deck.draw_card())

        # Каждому игроку раздаем 6 карт
        for _ in range(cls.INITIAL_HAND_SIZE):
            for player in player_types.keys():
                player.hand.add_card(deck.draw_card())  # Добавляем карту в руку игрока

        return cls(player_types, game_state)

    def run(self):
        # Метод для запуска игры
        while self.current_phase != GamePhase.GAME_END:
            self.run_one_step()

    def run_one_step(self):
        # Метод для выполнения одного шага игры
        phases = {
            GamePhase.CHOOSE_CARD: self.choose_card_phase,
            GamePhase.CHOOSE_CARD_AGAIN: self.choose_card_again_phase,
            GamePhase.DRAW_EXTRA: self.draw_extra_phase,
            GamePhase.NEXT_PLAYER: self.next_player_phase,
            GamePhase.DECLARE_WINNER: self.declare_winner_phase,
        }
        self.current_phase = phases[self.current_phase]()

    def declare_winner_phase(self) -> GamePhase:
        # Фаза объявления победителя
        print(f"{self.game_state.current_player()} is the winner!")
        post_event(CustomEvent.DECLARE_WINNER, player_index=self.game_state.current_player_index)
        return GamePhase.GAME_END

    def next_player_phase(self) -> GamePhase:
        # Фаза переключения на следующего игрока
        if not self.game_state.current_player().hand.cards:
            return GamePhase.DECLARE_WINNER
        self.game_state.next_player()
        print(f"=== {self.game_state.current_player()}'s turn")
        return GamePhase.CHOOSE_CARD

    def draw_extra_phase(self) -> GamePhase:
        # Фаза вытягивания дополнительной карты
        current_player = self.game_state.current_player()
        card = self.game_state.draw_card()
        print(f"Player {current_player} draws {card}")

        # Передаем как текущего игрока, так и вытянутую карту
        self.inform_all("inform_card_drawn", current_player, card)

        post_event(CustomEvent.DRAW_CARD, card=card, player_index=self.game_state.current_player_index)
        return GamePhase.CHOOSE_CARD_AGAIN

    def choose_card_again_phase(self) -> GamePhase:
        # Фаза выбора карты снова
        current_player = self.game_state.current_player()
        playable_cards = current_player.hand.playable_cards(self.game_state.top)
        if playable_cards:
            card = playable_cards[0]  # Играть только вновь взятую карту
            print(f"Player {current_player} can play drawn card")
            if self.player_types[current_player].choose_to_play(self.game_state.top, card):
                print(f"Player {current_player.name} played {card}")
                current_player.hand.remove_card(card)
                self.game_state.top = card
                self.inform_all("inform_card_played", current_player, card)
                post_event(CustomEvent.PLAY_CARD, card=card, player_index=self.game_state.current_player_index)
            else:
                print(f"Player decides not to play {card}")
        return GamePhase.NEXT_PLAYER

    def choose_card_phase(self) -> GamePhase:
        current_player = self.game_state.current_player()
        playable_cards = current_player.hand.playable_cards(self.game_state.top)

        print(
            f"Player {current_player.name} with hand {current_player.hand} can play {playable_cards} on top of {self.game_state.top}"
        )

        if not playable_cards:
            print(f"Player {current_player.name} could not play any card")
            return GamePhase.DRAW_EXTRA

        card = self.player_types[current_player].choose_card(current_player.hand, self.game_state.top)

        if card is None:
            print(f"Player {current_player.name} skipped a turn")
            return GamePhase.DRAW_EXTRA

        assert card in playable_cards
        print(f"Player {current_player.name} played {card}")
        current_player.hand.remove_card(card)
        self.game_state.top = card
        self.inform_all("inform_card_played", current_player, card)
        post_event(CustomEvent.PLAY_CARD, card=card, player_index=self.game_state.current_player_index)
        return GamePhase.NEXT_PLAYER

    def inform_all(self, method: str, *args, **kwargs):
        # Метод для уведомления всех игроков
        for p in self.player_types.values():
            getattr(p, method)(*args, **kwargs)

    @classmethod
    def request_player_count(cls) -> int:
        while True:
            try:
                count = int(input("Сколько игроков? "))
                if count > 0:
                    return count
                else:
                    print("Пожалуйста, введите положительное число.")
            except ValueError:
                print("Пожалуйста, введите корректное число.")

    @classmethod
    def request_player_names(cls, count: int) -> list:
        names = []
        while len(names) < count:
            name = input(f"Введите имя игрока {len(names) + 1}: ")
            if name.isalpha():
                names.append(name)
            else:
                print("Имя должно состоять только из букв.")
        return names

    @classmethod
    def request_player_type(cls):
        player_types_list = [cls.__name__ for cls in all_player_types]
        player_types_as_str = ', '.join(player_types_list)

        print(f"Доступные типы игроков: {player_types_as_str}")
        while True:
            kind = input("Выберите тип игрока: ")
            if kind in player_types_list:
                return next(cls for cls in all_player_types if cls.__name__ == kind)
            else:
                print(f"Недопустимый тип игрока. Доступные типы: {player_types_as_str}")

    @classmethod
    def get_players(cls):
        player_count = cls.request_player_count()
        player_types = {}
        names = cls.request_player_names(player_count)  # Передаем количество игроков
        for name in names:
            player = Player(name, Hand())
            player_types[player] = cls.request_player_type()
        return player_types

def __main__():
    # Главная функция для запуска игры
    load_from_file = False
    if load_from_file:
        server = GameServer.load_game('lama.json')
    else:
        server = GameServer.new_game(GameServer.get_players())
    server.save('lama.json')
    server.run()

if __name__ == "__main__":
    __main__()

