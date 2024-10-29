import pytest
from src.card import LlamaCard
from src.deck import Deck

def test_init_with_cards():
    cards = [LlamaCard(0), LlamaCard(1)]
    deck = Deck(cards)
    assert deck.cards == cards

def test_init_without_cards():
    deck = Deck()
    assert len(deck.cards) == len(LlamaCard.all_cards())  # Проверяем, что колода содержит все карты

def test_repr():
    cards = [LlamaCard(0), LlamaCard(1)]
    deck = Deck(cards)
    assert repr(deck) == "0 1"  # Проверяем строковое представление

def test_eq():
    deck1 = Deck([LlamaCard(0), LlamaCard(1)])
    deck2 = Deck([LlamaCard(1), LlamaCard(0)])
    assert deck1 == deck2  # Проверяем равенство колод

def test_save():
    deck = Deck([LlamaCard(0), LlamaCard(1)])
    assert deck.save() == "0 1"  # Проверяем сохранение

def test_load():
    deck = Deck.load("0 1")
    expected_deck = Deck([LlamaCard(0), LlamaCard(1)])
    assert deck == expected_deck  # Проверяем загрузку

def test_draw_card():
    deck = Deck([LlamaCard(0), LlamaCard(1)])
    card = deck.draw_card()
    assert card in [LlamaCard(0), LlamaCard(1)]  # Проверяем, что вытянутая карта из колоды
    assert len(deck.cards) == 1  # Проверяем, что одна карта была удалена

def test_draw_card_empty_deck():
    deck = Deck([])
    with pytest.raises(ValueError):
        deck.draw_card()  # Проверяем исключение при пустой колоде

def test_shuffle():
    deck = Deck([LlamaCard(0), LlamaCard(1)])
    original_order = deck.cards.copy()
    deck.shuffle()
    assert deck.cards != original_order  # Проверяем, что порядок изменился

def test_is_empty():
    deck = Deck([])
    assert deck.is_empty()  # Проверяем, что колода пуста
    deck = Deck([LlamaCard(0)])
    assert not deck.is_empty()  # Проверяем, что колода не пуста
