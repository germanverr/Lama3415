# src/player_interactions/__init__.py

from src.player_interactions.ai_player import Bot
from src.player_interactions.human_player import Human
from src.player_interactions.humanGUI_player import HumanGUI

# Определяем список всех классов игроков
all_player_types = [Bot, Human, HumanGUI]

__all__ = ['Bot', 'Human', 'HumanGUI', 'all_player_types']


