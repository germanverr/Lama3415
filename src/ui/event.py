from enum import IntEnum, auto
import pygame

class CustomEvent(IntEnum):
    PLAY_CARD = pygame.USEREVENT + 1   # Событие для игры карты
    DRAW_CARD = auto()                  # Событие для вытягивания карты
    DECLARE_WINNER = auto()             # Событие для объявления победителя
    SELECT_INTERACTIVE_CARDS = auto()   # Событие для выделения играбельных карт игрока

def post_event(event_type: int, **kwargs):
    """ Посылаем пользовательский event, данные передаем в kwargs. """
    event = pygame.event.Event(event_type)  # Создаем новое событие
    event.user_data = kwargs                  # Сохраняем дополнительные данные в user_data
    pygame.event.post(event)                  # Публикуем событие в очередь событий Pygame
