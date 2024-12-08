import json
import os
from pathlib import Path
from typing import Dict
import enum
import pygame
from src.deck import Deck
from src.game_state import GameState
from src.hand import Hand
from src.player import Player
from src.player_interaction import PlayerInteraction
from src.player_interactions.init import all_player_types
from src.ui.event import post_event, CustomEvent

# Инициализация Pygame
pygame.init()

class GamePhase(enum.StrEnum):
    CHOOSE_CARD = "Choose card"
    DRAW_EXTRA = "Draw extra card"
    CHOOSE_CARD_AGAIN = "Choose card again"
    NEXT_PLAYER = "Switch current player"
    DETERMINE_WINNER = "Determine the winner"
    DECLARE_WINNER = "Declare a winner"
    GAME_END = "Game ended"

class GameServer:
    INITIAL_HAND_SIZE = 6
    MAX_TURNS = 100

    def __init__(self, player_types: Dict[Player, PlayerInteraction], game_state: GameState):
        self.game_state = game_state
        self.player_types = player_types
        self.current_phase = GamePhase.CHOOSE_CARD
        self.turn_count = 0

    @classmethod
    def load_game(cls, filename: str | Path):
        with open(filename, 'r', encoding='utf-8') as fin:
            data = json.load(fin)
            game_state = GameState.load(data)
            player_types = {
                player: next(pt for pt in all_player_types if pt.__name__ == player_data['kind'])(player.name)
                for player, player_data in zip(game_state.players, data['players'])
            }
            return cls(player_types=player_types, game_state=game_state)

    def save(self, filename: str | Path):
        with open(filename, 'w') as fout:
            json.dump(self.save_to_dict(), fout, indent=4)

    def save_to_dict(self):
        data = self.game_state.save()
        for player_index, player in enumerate(self.player_types.keys()):
            data['players'][player_index]['kind'] = self.player_types[player].__class__.__name__
        return data

    @classmethod
    def new_game(cls, player_types: Dict[Player, PlayerInteraction]):
        deck = Deck()
        game_state = GameState(list(player_types.keys()), deck, deck.draw_card())
        for _ in range(cls.INITIAL_HAND_SIZE):
            for player in player_types.keys():
                player.hand.add_card(deck.draw_card())
        return cls(player_types, game_state)

    def run(self):
        print("=== Игра началась! ===")
        while self.current_phase != GamePhase.GAME_END and self.turn_count < self.MAX_TURNS:
            self.run_one_step()
            self.turn_count += 1
        if self.turn_count >= self.MAX_TURNS:
            print("Достигнуто максимальное количество ходов. Определяем победителя.")
            self.determine_winner_phase()

    def run_one_step(self):
        phases = {
            GamePhase.CHOOSE_CARD: self.choose_card_phase,
            GamePhase.CHOOSE_CARD_AGAIN: self.choose_card_again_phase,
            GamePhase.DRAW_EXTRA: self.draw_extra_phase,
            GamePhase.NEXT_PLAYER: self.next_player_phase,
            GamePhase.DETERMINE_WINNER: self.determine_winner_phase,
            GamePhase.DECLARE_WINNER: self.declare_winner_phase
        }
        self.current_phase = phases[self.current_phase]()

    def determine_winner_phase(self) -> GamePhase:
        players = self.game_state.players
        print("\nТекущие очки игроков:")
        for player in players:
            print(f"{player.name}: {player.score}")

        winners = [player for player in players if not player.hand.cards or player.score >= 40]
        if winners:
            return self.declare_winner_phase(winners[0])

        max_score = max(player.score for player in players)
        winners = [player for player in players if player.score == max_score]
        return self.declare_winner_phase(winners[0])

    def declare_winner_phase(self, winner: Player) -> GamePhase:
        print(f"\n🎉 {winner.name} выиграл с результатом {winner.score}! 🎉")
        post_event(CustomEvent.DECLARE_WINNER, player_index=self.game_state.current_player_index)
        return GamePhase.GAME_END

    def next_player_phase(self) -> GamePhase:
        current_player = self.game_state.current_player()
        if not current_player.hand.cards:
            return GamePhase.DETERMINE_WINNER
        self.game_state.next_player()
        print(f"\n=== Ход {self.game_state.current_player().name} ===")
        return GamePhase.CHOOSE_CARD

    def choose_card_again_phase(self) -> GamePhase:
        current_player = self.game_state.current_player()
        playable_cards = current_player.hand.playable_cards(self.game_state.top)
        if playable_cards:
            card = playable_cards[0]
            if self.player_types[current_player].choose_to_play(self.game_state.top, card):
                current_player.hand.remove_card(card)
                self.game_state.top = card
                self.inform_all("inform_card_played", current_player, card)
                post_event(CustomEvent.PLAY_CARD, card=card, player_index=self.game_state.current_player_index)
        return GamePhase.NEXT_PLAYER

    def choose_card_phase(self) -> GamePhase:
        current_player = self.game_state.current_player()
        playable_cards = current_player.hand.playable_cards(self.game_state.top)
        print(f"\nИгрок {current_player.name} может сыграть: {playable_cards} на {self.game_state.top}")

        if not playable_cards:
            print(f"Игрок {current_player.name} не может сыграть ни одной карты.")
            return GamePhase.DRAW_EXTRA

        card = self.player_types[current_player].choose_card(current_player.hand, self.game_state.top)
        if card and card in playable_cards:
            current_player.hand.remove_card(card)
            self.game_state.top = card
            self.player_types[current_player].inform_card_played(current_player, card)
            post_event(CustomEvent.PLAY_CARD, card=card, player_index=self.game_state.current_player_index)
        return GamePhase.NEXT_PLAYER

    def draw_extra_phase(self) -> GamePhase:
        current_player = self.game_state.current_player()
        drawn_card = self.game_state.draw_card()
        if drawn_card is None:
            print("Колода пуста, ход пропущен.")
            return GamePhase.NEXT_PLAYER

        self.player_types[current_player].inform_card_drawn(current_player, drawn_card)
        current_player.hand.add_card(drawn_card)
        print(f"Игрок {current_player.name} вытянул карту: {drawn_card}")
        if drawn_card.can_play_on(self.game_state.top) and self.player_types[current_player].choose_to_play(self.game_state.top, drawn_card):
            current_player.hand.remove_card(drawn_card)
            self.game_state.top = drawn_card
            self.player_types[current_player].inform_card_played(current_player, drawn_card)
            post_event(CustomEvent.PLAY_CARD, card=drawn_card, player_index=self.game_state.current_player_index)
        return GamePhase.NEXT_PLAYER

    def inform_all(self, method: str, *args, **kwargs):
        for player in self.player_types.values():
            getattr(player, method)(*args, **kwargs)

    @classmethod
    def request_player_count(cls) -> int:
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
        print(f"Доступные типы игроков: {', '.join(player_types_list)}")
        while True:
            kind = input("Выберите тип игрока: ")
            if kind in player_types_list:
                return next(cls for cls in all_player_types if cls.__name__ == kind)

    @classmethod
    def get_players(cls):
        player_count = cls.request_player_count()
        names = cls.request_player_names(player_count)
        return {Player(name, Hand()): cls.request_player_type() for name in names}

def __main__():
    save_file = 'lama.json'
    server = GameServer.load_game(save_file) if os.path.exists(save_file) else GameServer.new_game(GameServer.get_players())
    server.save(save_file)
    server.run()

if __name__ == "__main__":
    __main__()
