import os
import enum
import json
import pygame
from typing import Dict
from pathlib import Path
from src.deck import Deck
from src.hand import Hand
from src.player import Player
from src.game_state import GameState
from src.ui.event import post_event, CustomEvent
from src.player_interaction import PlayerInteraction
from src.player_interactions.init import all_player_types

# Инициализация Pygame
pygame.init()

# Перечисление для различных фаз игры
class GamePhase(enum.StrEnum):
    CHOOSE_CARD = "Choose card"  # Фаза выбора карты -> DRAW_EXTRA, NEXT_PLAYER
    DRAW_EXTRA = "Draw extra card"  # Фаза вытягивания дополнительной карты -> CHOOSE_CARD_AGAIN
    CHOOSE_CARD_AGAIN = "Choose card again"  # Фаза повторного выбора карты -> NEXT_PLAYER
    NEXT_PLAYER = "Switch current player"  # Фаза смены текущего игрока -> ROUND_END, CHOOSE_CARD (NEXT_PLAYER)
    DETERMINE_WINNER = "Determine the winner"  # Фаза определения победителя -> DECLARE_WINNER
    DECLARE_WINNER = "Declare a winner"  # Фаза объявления победителя -> GAME_END
    GAME_END = "Game ended"  # Фаза окончания игры
    BEGIN_ROUND = "Begin round" # начинаем раунд, раздаем карты -> CHOOSE_CARD
    END_ROUND = "End round"     # конец раунда, подсчет очков -> BEGIN_ROUND, DETERMINE_WINNER

# Класс для управления игровым процессом
class GameServer:
    INITIAL_HAND_SIZE = 6  # Начальный размер руки игроков

    def __init__(self, player_types: Dict[Player, PlayerInteraction], game_state: GameState):
        self.game_state = game_state  # Состояние игры
        self.player_types = player_types  # Типы игроков
        self.current_phase = GamePhase.CHOOSE_CARD  # Текущая фаза игры
        self.turn_count = 0  # Счетчик ходов

    @classmethod
    def load_game(cls, filename: str | Path):
        # Загрузка состояния игры из файла
        with open(filename, 'r', encoding='utf-8') as fin:
            data = json.load(fin)  # Чтение данных из JSON-файла
            game_state = GameState.load(data)  # Загрузка состояния игры
            player_types = {
                player: next(pt for pt in all_player_types if pt.__name__ == player_data['kind'])(player.name)
                for player, player_data in zip(game_state.players, data['players'])
            }
            return cls(player_types=player_types, game_state=game_state)

    def save(self, filename: str | Path):
        # Сохранение текущего состояния игры в файл
        with open(filename, 'w', encoding='utf-8') as fout:
            json.dump(self.save_to_dict(), fout, indent=4)

    def save_to_dict(self):
        # Преобразование состояния игры в словарь для сохранения
        data = self.game_state.save()
        for player_index, player in enumerate(self.player_types.keys()):
            data['players'][player_index]['kind'] = self.player_types[player].__class__.__name__
        return data

    @classmethod
    def new_game(cls, player_types: Dict[Player, PlayerInteraction]):
        # Создание новой игры с заданными типами игроков
        deck = Deck()  # Создание колоды

        game_state = GameState(list(player_types.keys()), deck, deck.draw_card())  # Инициализация состояния игры
        return cls(player_types, game_state)

    def run(self):
        # Основной цикл игры
        print("=== Игра началась! ===")
        while self.current_phase != GamePhase.GAME_END:
            self.run_one_step()

    def round_begin(self):
        # Начало раунда, раздача карт
        # Проверяем, загружена ли игра из JSON файла
        if self.game_state.is_loaded_from_json:
            return GamePhase.CHOOSE_CARD  # Если загружены из JSON, просто переходим к выбору карты
        # Если руки пустые у текущего игрока, то надо сделать колоду, перемешать и раздавать карты
        current_player = self.game_state.current_player()
        if current_player.hand.is_empty():
            deck = Deck()  # Создание колоды
            deck.shuffle()
            self.game_state.deck = deck
            self.game_state.deal_cards()  # Раздаем карты всем игрокам

        return GamePhase.CHOOSE_CARD  # Переход к фазе выбора карты

    def round_end(self):
        # Конец раунда
        for player in self.game_state.players:
            # Считаем очки игрока на основе его руки, учитывая только уникальные значения карт
            unique_values = set(card.value for card in player.hand.cards)  # Получаем уникальные значения
            player_score = sum(unique_values)  # Суммируем уникальные значения
            player.score += player_score  # Добавляем очки к общему счету игрока
            # Очищаем руку игрока
            player.hand.clear()
            # Проверяем, если у игрока 40 или больше очков
            if player.score >= 40:
                return GamePhase.DETERMINE_WINNER  # Конец игры, если у кого-то 40 или больше очков
        # Делаем новую колоду и перемешиваем ее
        self.game_state.deck = Deck()
        self.game_state.deck.shuffle()
        return GamePhase.BEGIN_ROUND  # Переход к началу нового раунда

    def run_one_step(self):
        # Выполнение одного шага в зависимости от текущей фазы игры
        phases = {
            GamePhase.BEGIN_ROUND: self.round_begin,        # CHOOSE_CARD
            GamePhase.CHOOSE_CARD: self.choose_card_phase,  # DRAW_EXTRA | NEXT_PLAYER
            GamePhase.CHOOSE_CARD_AGAIN: self.choose_card_again_phase,  # NEXT_PLAYER
            GamePhase.DRAW_EXTRA: self.draw_extra_phase,    # CHOOSE_CARD_AGAIN | NEXT_PLAYER
            GamePhase.NEXT_PLAYER: self.next_player_phase,
                # CHOOSE_CARD (следующий игрок пытается играть)
                # NEXT_PLAYER (этот игрок в состоянии quit и идем к следующему игроку)
                # END_ROUND (все игроки в состоянии quit)
            GamePhase.END_ROUND: self.round_end,            # BEGIN_ROUND, DETERMINE_WINNER
            GamePhase.DETERMINE_WINNER: self.determine_winner_phase,
            GamePhase.DECLARE_WINNER: self.declare_winner_phase
        }
        self.current_phase = phases[self.current_phase]()  # Переход к следующей фазе

    def determine_winner_phase(self) -> GamePhase:
        # Фаза определения победителя
        players = self.game_state.players
        print("\nТекущие очки игроков:")
        for player in players:
            print(f"{player.name}: {player.score}")  # Вывод очков каждого игрока

        # Проверка, если кто-то достиг 40 очков
        if any(player.score >= 40 for player in players):
            # Получаем игроков с очками менее 40
            players_below_40 = [player for player in players if player.score < 40]

            if players_below_40:  # Проверяем, есть ли такие игроки
                min_score = min(player.score for player in players_below_40)  # Минимальный счет среди игроков с < 40
                winners = [player for player in players_below_40 if
                           player.score == min_score]  # Игроки с минимальным счетом

                if winners:
                    return self.declare_winner_phase(winners[0])  # Объявление игрока с наименьшим счетом победителем

        # Если никто не достиг 40 очков, определяем победителя по обычным правилам
        min_score = min(player.score for player in players)  # Поиск минимального счета
        winners = [player for player in players if player.score == min_score]
        return self.declare_winner_phase(winners[0])  # Объявление победителя

    def declare_winner_phase(self, winner: Player) -> GamePhase:
        # Фаза объявления победителя
        print(f"\n🎉 {winner.name} выиграл с результатом {winner.score}! 🎉")
        post_event(CustomEvent.DECLARE_WINNER, player_index=self.game_state.current_player_index)
        return GamePhase.GAME_END

    def next_player_phase(self) -> GamePhase:
        # Фаза смены текущего игрока
        current_player = self.game_state.current_player()
        print(f'{current_player.name}: {current_player.hand}')

        # если у текущего игрока пустая рука, то завершаем раунд и он победитель
        if current_player.hand.is_empty():
            print(f'{current_player.name}: Сыграны все карты с руки')
            return GamePhase.END_ROUND  # Если у игрока нет карт, завершаем раунд
        # Проверяем, если все игроки в состоянии quit
        if all(player.quit for player in self.game_state.players):
            print(f'Все игроки QUIT')
            return GamePhase.END_ROUND  # Все игроки вышли, завершаем раунд

        self.game_state.next_player()  # Переход к следующему игроку
        print(f"\n=== Ход {self.game_state.current_player().name} ===")
        return GamePhase.CHOOSE_CARD  # Переход к фазе выбора карты

    def choose_card_again_phase(self) -> GamePhase:
        # Фаза повторного выбора карты
        current_player = self.game_state.current_player()
        playable_cards = current_player.hand.playable_cards(self.game_state.top)
        if playable_cards:
            card = playable_cards[0]
            if self.player_types[current_player].choose_to_play(self.game_state.top, card):
                current_player.hand.remove_card(card)  # Удаление карты из руки
                self.game_state.top = card  # Обновление верхней карты
                print(f'Игрок {current_player.name} сыграл {card}')
                print(f'Top: {self.game_state.top}')

                self.inform_all("inform_card_played", current_player, card)
                post_event(CustomEvent.PLAY_CARD, card=card, player_index=self.game_state.current_player_index)
        return GamePhase.NEXT_PLAYER

    def choose_card_phase(self) -> GamePhase:
        # Фаза выбора карты
        current_player = self.game_state.current_player()
        # если игрок РАНЬШЕ решил закончить ход, то вместо игры карт, передаем ход другому игроку
        if current_player.quit:
            print(f'Игрок {current_player.name} в состоянии QUIT, ход переходит следующему игроку.')
            return GamePhase.NEXT_PLAYER

        playable_cards = current_player.hand.playable_cards(self.game_state.top)
        print(f"\nИгрок {current_player.name} {current_player.hand} может сыграть: {playable_cards} на {self.game_state.top}")

        if not playable_cards:
            # выбрали не тянуть карту, а закончить играть в этом раунде
            if self.player_types[current_player].choose_quit(current_player.hand, self.game_state.top) : # Игрок выбирает карту:
                current_player.quit = True
                return GamePhase.NEXT_PLAYER
            print(f"Игрок {current_player.name} не может сыграть ни одной карты.")
            return GamePhase.DRAW_EXTRA  # Переход к фазе вытягивания дополнительной карты

        card = self.player_types[current_player].choose_card(current_player.hand,
                                                             self.game_state.top)  # Игрок выбирает карту
        if card and card in playable_cards:
            current_player.hand.remove_card(card)  # Удаление карты из руки
            self.game_state.top = card  # Обновление верхней карты
            print(f'Игрок {current_player.name} сыграл {card}')
            print(f'Top: {self.game_state.top}')
            self.player_types[current_player].inform_card_played(current_player, card)
            post_event(CustomEvent.PLAY_CARD, card=card, player_index=self.game_state.current_player_index)
        return GamePhase.NEXT_PLAYER

    def draw_extra_phase(self) -> GamePhase:
        # Фаза вытягивания дополнительной карты
        current_player = self.game_state.current_player()
        drawn_card = self.game_state.draw_card()  # Вытягивание карты из колоды
        if drawn_card is None:
            print("Колода пуста, ход пропущен.")
            # костыль: если колода пустая, то переходим в quit
            current_player.quit = True
            return GamePhase.NEXT_PLAYER

        self.player_types[current_player].inform_card_drawn(current_player, drawn_card)
        print(f"Игрок {current_player.name} вытянул карту: {drawn_card}")
        return GamePhase.CHOOSE_CARD_AGAIN

    def inform_all(self, method: str, *args, **kwargs):
        # Информирование всех игроков о событии
        for player in self.player_types.values():
            getattr(player, method)(*args, **kwargs)  # Вызов метода для каждого игрока

    def calculate_points(self, card):
        # Пример логики для начисления очков
        return card.value  # Предполагается, что у карты есть атрибут value

    @classmethod
    def request_player_count(cls) -> int:
        # Запрос количества игроков
        while True:
            try:
                count = int(input("Сколько игроков? "))
                if count > 0:
                    return count
            except ValueError:
                pass
            print("Пожалуйста, введите корректное число.")

    @classmethod
    def request_player_names(cls, count: int) -> list:
        # Запрос имен игроков
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
        # Запрос типа игрока
        player_types_list = [cls.__name__ for cls in all_player_types]
        print(f"Доступные типы игроков: {', '.join(player_types_list)}")
        while True:
            kind = input("Выберите тип игрока: ")
            if kind in player_types_list:
                return next(cls for cls in all_player_types if cls.__name__ == kind)

    @classmethod
    def get_players(cls):
        # Получение информации о игроках
        player_count = cls.request_player_count()
        names = cls.request_player_names(player_count)
        return {Player(name, Hand()): cls.request_player_type() for name in names}


def __main__():
    # Основная функция для запуска игры
    save_file = 'lama.json'
    server = GameServer.load_game(save_file) if os.path.exists(save_file) else GameServer.new_game(
        GameServer.get_players())
    server.save(save_file)
    server.run()


if __name__ == "__main__":
    from random import seed
    seed(7)
    __main__()