import pytest
from src.card import LlamaCard

def test_init():
    c = LlamaCard(3)
    assert c.value == 3

@pytest.mark.parametrize("value, expected_repr", [
    (3, '3'),
    (6, '6'),
    (1, '1'),
    (0, 'Лама'),
])
def test_save(value, expected_repr):
    c = LlamaCard(value)
    assert repr(c) == expected_repr
    assert c.save() == expected_repr

def test_eq():
    c1 = LlamaCard(3)
    c2 = LlamaCard(3)
    c3 = LlamaCard(1)
    c4 = LlamaCard(2)
    c5 = LlamaCard(6)
    c_lama = LlamaCard(0)  # Карта Лама

    assert c1 == c2
    assert c1 != c3
    assert c1 != c4
    assert c1 != c5
    assert c_lama == LlamaCard(0)  # Проверка на равенство карты Лама

def test_load():
    s = '3'
    c = LlamaCard.load(s)
    assert c == LlamaCard(3)

    s = '0'  # Проверка загрузки карты Лама
    c = LlamaCard.load(s)
    assert c == LlamaCard(0)

def test_validation():
    with pytest.raises(ValueError):
        LlamaCard('3')  # Проверка на невалидный ввод

def test_play_on():
    c1 = LlamaCard.load('1')
    c2 = LlamaCard.load('2')
    c3 = LlamaCard.load('3')
    c4 = LlamaCard.load('4')
    c_lama = LlamaCard.load('0')  # Карта Лама

    assert c1.can_play_on(c1)
    assert c2.can_play_on(c1)
    assert c2.can_play_on(c2)
    assert not c3.can_play_on(c1)
    assert not c4.can_play_on(c1)
    assert c_lama.can_play_on(c1)  # Проверка, что Лама может играть на 1
    assert c_lama.can_play_on(c_lama)  # Проверка, что Лама может играть на Ламу

def test_all_cards():
    cards = LlamaCard.all_cards(value=[5, 2, 6, 0])
    expected_cards = [
        LlamaCard.load('5'),
        LlamaCard.load('2'),
        LlamaCard.load('6'),
        LlamaCard.load('0'),  # Проверка карты Лама
    ]
    assert cards == expected_cards

def test_score():
    c = LlamaCard(6)
    assert c.score() == 6

    c = LlamaCard(5)
    assert c.score() == 5

    c_lama = LlamaCard(0)  # Проверка карты Лама
    assert c_lama.score() == 10  # Теперь карта Лама имеет 10 очков
