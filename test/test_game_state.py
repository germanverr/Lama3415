import pytest
from src.player import Player
from src.deck import Deck
from src.card import LlamaCard
from src.game_state import GameState

data = {
    "top": "7",
    "current_player_index": 1,
    "deck": "2 6 0",
    "players": [
        {"name": "Alex", "hand": "3 6", "score": 9},
        {"name": "Bob", "hand": "5", "score": 5},
        {"name": "Charley", "hand": "7 1 2", "score": 10},
    ],
}

# Загрузка игроков и колоды для тестов
alex = Player.load(data["players"][0])
bob = Player.load(data["players"][1])
charley = Player.load(data["players"][2])
full_deck = Deck.load(data["deck"])


def test_init(): #Проверяет инициализацию состояния игры
    players = [alex, bob, charley]
    game = GameState(players=players, deck=full_deck, current_player=1, top=LlamaCard.load("7"))

    assert game.players == players
    assert game.deck == full_deck
    assert game.current_player() == bob
    assert str(game.top) == "7"


def test_current_player(): #Проверяет, что текущий игрок корректно определяется на основе индекса. Тестирует несколько сценариев с разными индексами
    players = [alex, bob, charley]
    game = GameState(players=players, deck=full_deck, top=LlamaCard.load("7"))

    assert game.current_player() == alex

    game = GameState(players=players, deck=full_deck, top=LlamaCard.load("7"), current_player=1)
    assert game.current_player() == bob

    game = GameState(players=players, deck=full_deck, top=LlamaCard.load("7"), current_player=2)
    assert game.current_player() == charley


def test_eq(): #Проверяет, что два состояния игры могут быть равны, если у них одинаковые игроки, колода и верхняя карта. Также проверяет, что разные состояния игры не равны

    players = [alex, bob, charley]
    game1 = GameState(players=players, deck=full_deck, top=LlamaCard.load("7"))
    game1_copy = GameState(players=players.copy(), deck=Deck(game1.deck.cards.copy()), top=LlamaCard.load("7"))
    game2 = GameState(players=players.copy(), deck=Deck.load("2 6 0"), top=LlamaCard.load("7"))

    assert game1 == game1_copy
    assert game1 != game2


def test_save(): #Проверяет, что метод сохранения состояния игры (save) возвращает ожидаемый словарь с данными
    players = [alex, bob, charley]
    game = GameState(players=players, deck=full_deck, top=LlamaCard.load("7"), current_player=1)

    expected_save = {
        "top": str(LlamaCard.load("7")),
        "deck": str(full_deck),
        "current_player_index": 1,
        "players": [p.save() for p in players],
    }

    assert game.save() == expected_save


def test_load(): #Проверяет, что метод загрузки состояния игры (load) создает объект, который соответствует исходным данным
    game = GameState.load(data)
    assert game.save() == data


def test_next_player(): #Проверяет, что метод next_player корректно переключает текущего игрока
    game = GameState.load(data)
    assert game.current_player() == bob

    game.next_player()
    assert game.current_player() == charley

    game.next_player()
    assert game.current_player() == alex

    game.next_player()
    assert game.current_player() == bob


def test_draw_card(): #Проверяет, что метод draw_card корректно тянет карту из колоды и добавляет ее в руку текущего игрока
    game = GameState.load(data)
    assert str(game.deck) == "2 6 0"
    assert str(game.current_player().hand) == "5"

    game.draw_card()
    assert str(game.deck) == "2 6"
    assert str(game.current_player().hand) == "5 0"  # Предполагается, что карта 0 была добавлена


def test_play_card(): #Проверяет, что игрок может сыграть карту, и что карта удаляется из его руки, а верхняя карта обновляется
    players = [alex, bob, charley]
    game = GameState(players=players, deck=full_deck, top=LlamaCard.load("7"), current_player=2)

    assert str(game.current_player().hand) == "7 1 2"
    assert str(game.top) == "7"

    game.play_card(LlamaCard.load("1"))
    assert str(game.current_player().hand) == "7 2"
    assert str(game.top) == "1"


def test_is_round_over(): #Проверяет, что раунд не заканчивается, пока у игроков есть карты, и что он заканчивается, когда у одного из игроков больше нет карт
    players = [alex, bob, charley]
    game = GameState(players=players, deck=full_deck, top=LlamaCard.load("7"), current_player=0)

    assert not game.is_round_over()  # Игра не закончена

    # Удалим карты у одного игрока
    alex.hand.clear()
    assert game.is_round_over()  # Игра закончена


def test_end_round(): #Проверяет, что метод end_round очищает руки всех игроков в конце раунда
    players = [alex, bob, charley]
    game = GameState(players=players, deck=full_deck, top=LlamaCard.load("7"), current_player=0)

    # Предполагаем, что у игроков есть карты, и раунд не закончился
    assert not game.is_round_over()

    game.end_round()

    # Проверяем, что руки игроков очищены
    assert len(alex.hand.cards) == 0
    assert len(bob.hand.cards) == 0
    assert len(charley.hand.cards) == 0


# Тесты с картой "Лама"
def test_play_lama_card(): #Проверяет, что игрок может сыграть карту "Лама" (0), и верхняя карта становится "Ламой". У игрока при этом не должно изменяться количество карт
    players = [alex, bob, charley]
    game = GameState(players=players, deck=full_deck, top=LlamaCard.load("7"), current_player=2)

    assert str(game.current_player().hand) == "7 1 2"
    assert str(game.top) == "7"

    # Игрок Charley играет карту "Лама" (0)
    game.play_card(LlamaCard.load("0"))
    assert str(game.current_player().hand) == "7 1 2"  # У Charley все еще карты
    assert str(game.top) == "0"  # Теперь верхняя карта - Лама


def test_play_card_on_lama(): #Проверяет, что игрок может сыграть другую карту (например, "1") на верхнюю карту "Лама"
    players = [alex, bob, charley]
    game = GameState(players=players, deck=full_deck, top=LlamaCard.load("0"), current_player=1)  # Верхняя карта - Лама

    assert str(game.current_player().hand) == "5"  # У Bob только одна карта

    # Bob играет карту "1"
    game.play_card(LlamaCard.load("1"))
    assert str(game.current_player().hand) == "5"  # У Bob все еще одна карта
    assert str(game.top) == "1"  # Теперь верхняя карта - 1


def test_lama_can_play_on_lama(): #Проверяет, что игрок может сыграть карту "Лама" на другую карту "Лама"
    players = [alex, bob, charley]
    game = GameState(players=players, deck=full_deck, top=LlamaCard.load("0"), current_player=2)  # Верхняя карта - Лама

    assert str(game.current_player().hand) == "7 1 2"

    # Charley играет карту "Лама" (0)
    game.play_card(LlamaCard.load("0"))
    assert str(game.current_player().hand) == "7 1 2"  # У Charley все еще карты
    assert str(game.top) == "0"  # Верхняя карта остается Ламой


def test_score_lama(): #Проверяет, что карта "Лама" дает определенное количество очков (10), но если у игрока есть несколько "Лам", они не дают дополнительных очков
    players = [alex, bob, charley]
    game = GameState(players=players, deck=full_deck, top=LlamaCard.load("7"), current_player=2)

    # Проверка очков для карты "Лама"
    lama_card = LlamaCard.load("0")
    assert lama_card.score([lama_card]) == 10  # Лама дает 10 очков
    assert lama_card.score([lama_card, lama_card]) == 0  # Дубликат Ламы дает 0 очков

