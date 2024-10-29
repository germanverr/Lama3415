from src.hand import Hand
from src.player import Player
from src.card import LlamaCard

def test_init():
    """Тестирование инициализации игрока."""
    h = Hand.load("1 3 2")
    p = Player(name="Jordan", hand=h, score=10)
    assert p.name == "Jordan"
    assert p.hand == h
    assert p.score == 10

def test_str():
    """Тестирование строкового представления игрока."""
    h = Hand.load("1 3 2")
    p = Player(name="Jordan", hand=h, score=15)
    assert str(p) == "Jordan(15): 1 3 2"

def test_save():
    """Тестирование метода сохранения состояния игрока."""
    h = Hand.load("1 3 2")
    p = Player(name="Jordan", hand=h, score=15)
    assert p.save() == {"name": "Jordan", "score": 15, "hand": "1 3 2"}

def test_eq():
    """Тестирование сравнения двух игроков на равенство."""
    h1 = Hand.load("1 3 2")
    h2 = Hand.load("1 3 2")
    p1 = Player(name="Jordan", hand=h1, score=10)
    p2 = Player(name="Jordan", hand=h2, score=10)
    assert p1 == p2

def test_load():
    """Тестирование загрузки состояния игрока из словаря."""
    data = {"name": "Jordan", "score": 10, "hand": "1 3 2"}
    h = Hand.load("1 3 2")
    p_expected = Player(name="Jordan", hand=h, score=10)
    p = Player.load(data)
    assert p == p_expected

def test_hash():
    """Тестирование хеширования игрока."""
    h = Hand.load("1 3 2")
    p = Player(name="Jordan", hand=h, score=10)
    assert isinstance(hash(p), int)

def test_hand_modification():
    """Тестирование изменения руки игрока."""
    h = Hand.load("1 3 2")
    p = Player(name="Jordan", hand=h, score=10)
    p.hand.add_card(LlamaCard.load("4"))  # Добавляем карту Лама
    assert len(p.hand.cards) == 4  # Проверяем, что карта добавлена
    assert str(p) == "Jordan(10): 1 3 2 4"  # Проверяем строковое представление

def test_hand_score():
    """Тестирование подсчета очков в руке игрока."""
    h = Hand.load("1 3 2")  # Предположим, что каждая карта имеет значение 1
    p = Player(name="Jordan", hand=h, score=10)
    p.hand.add_card(LlamaCard.load("Lama"))  # Добавляем карту Лама
    assert p.hand.score() == 16  # Проверяем, что сумма очков в руке равна 16 (3*1 + 10)

def test_llama_card_score():
    """Тестирование подсчета очков карты Лама."""
    llama_card = LlamaCard.load("Lama")
    assert llama_card.score() == 10  # Проверяем, что карта Лама дает 10 очков

