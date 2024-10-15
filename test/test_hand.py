import random
from src.card import LlamaCard
from src.hand import Hand

cards = [LlamaCard(3), LlamaCard(1), LlamaCard(6)]

def test_init():
    d = Hand(cards=cards)
    assert d.cards == cards

def test_save():
    d = Hand(cards=cards)
    assert d.save() == '3 1 6'

    d = Hand(cards=[])
    assert d.save() == ''

def test_load():
    d = Hand.load('3 1 6')
    expected_deck = Hand(cards)
    assert d == expected_deck

def test_score():
    h = Hand.load('3 0 6')
    assert h.score() == 19

    h = Hand.load('5 3')
    assert h.score() == 8

def test_add_card():
    h = Hand.load('3 1 6')
    h.add_card(LlamaCard.load('6'))
    assert repr(h) == '3 1 6 6'

    h.add_card(LlamaCard.load('4'))
    assert repr(h) == '3 1 6 6 4'

def test_remove_card():
    h = Hand.load('3 1 6 6 4')
    c = LlamaCard.load('6')
    h.remove_card(c)
    assert repr(h) == '3 1 6 4'
