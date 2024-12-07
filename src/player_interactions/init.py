# src/player_interactions/__init__.py

from src.player_interactions.ai_player import Bot
from src.player_interactions.human_player import Human

# Определяем список всех классов игроков
all_player_types = [Bot, Human]

__all__ = ['Bot', 'Human', 'all_player_types']


