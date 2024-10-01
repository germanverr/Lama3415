from src.card import LlamaCard
import pytest
def test_init():
    # тест инициализации карты
    c = LlamaCard(3)
    assert c.value == 3

def test_save():
    # тест сохранения карты
    c = LlamaCard(3)
    assert repr(c) == '3'
    assert c.save() == '3'

    c = LlamaCard(6)
    assert repr(c) == '6'
    assert c.save() == '6'

def test_eq():
    # тест сравнения двух карт
    c1 = LlamaCard(3)
    c2 = LlamaCard(3)
    c3 = LlamaCard(1)
    c4 = LlamaCard(2)
    c5 = LlamaCard(6)

    assert c1 == c2
    assert c1 != c3
    assert c1 != c4
    assert c1 != c5

def test_load():
    # тест загрузки карты
    s = '3'
    c = LlamaCard.load(s)
    assert c == LlamaCard(3)

    s = '6'
    c = LlamaCard.load(s)
    assert c == LlamaCard(6)

def test_divzero():
    # пример теста с ловлей исключения
    with pytest.raises(ZeroDivisionError):
        x = 2 / 0

def test_validation():
    # тест валидации карты
    with pytest.raises(ValueError):
        LlamaCard('3')

def test_play_on():
    # тест метода can_play_on
    c1 = LlamaCard.load('1')
    c2 = LlamaCard.load('2')
    c3 = LlamaCard.load('3')
    c4 = LlamaCard.load('4')

    assert c1.can_play_on(c1)
    assert c2.can_play_on(c1)
    assert c2.can_play_on(c2)
    assert not c3.can_play_on(c1)
    assert not c4.can_play_on(c1)

def test_all_cards():
    # тест метода all_cards
    cards = LlamaCard.all_cards(value=[5, 2, 6])
    expected_cards = [
        LlamaCard.load('5'),
        LlamaCard.load('2'),
        LlamaCard.load('6'),
    ]
    assert cards == expected_cards

def test_score():
    # тест метода score
    c = LlamaCard(6)
    assert 6 == c.score()

    c = LlamaCard(5)
    assert 5 == c.score()
