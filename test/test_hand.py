import random
from src.card import LlamaCard
from src.hand import Hand

# Инициализация карт, включая карту Лама
cards = [LlamaCard(3), LlamaCard(1), LlamaCard(6), LlamaCard(0)]  # 0 - карта Лама

def test_init():
    d = Hand(cards=cards)
    assert d.cards == cards

def test_save():
    d = Hand(cards=cards)
    assert d.save() == '3 1 6 0'  # Предположим, что карта Лама представляется как '0'

    d = Hand(cards=[])
    assert d.save() == ''

def test_load():
    d = Hand.load('3 1 6 0')
    expected_deck = Hand(cards)
    assert d == expected_deck

def test_score():
    h = Hand.load('3 1 6 0')
    assert h.score() == 10 + 3 + 1 + 6  # 10 очков за Ламу, 10 в сумме

    h = Hand.load('5 4')
    assert h.score() == 9

    h = Hand.load('Лама')  # Проверка только карты Лама
    assert h.score() == 10  # Убедитесь, что Лама дает 10 очков

def test_add_card():
    h = Hand.load('3 1 6')
    h.add_card(LlamaCard.load('0'))  # Добавление карты Лама
    assert repr(h) == '3 1 6 0'  # Проверка, что Лама добавлена

    h.add_card(LlamaCard.load('4'))
    assert repr(h) == '3 1 6 0 4'

def test_remove_card():
    h = Hand.load('3 1 6 0 4')
    c = LlamaCard.load('0')  # Удаление карты Лама
    h.remove_card(c)
    assert repr(h) == '3 1 6 4'  # Проверка, что Лама была успешно удалена
