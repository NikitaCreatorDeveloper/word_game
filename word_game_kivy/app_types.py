# word_game_kivy/app_types.py
from __future__ import annotations

from typing import Dict

from kivy.uix.screenmanager import ScreenManager

from word_game_kivy.game.player import Player
from word_game_kivy.sound_manager import SoundManager


class AppScreenManager(ScreenManager):
    """ScreenManager с известными для линтера атрибутами контекста приложения."""

    sound_manager: SoundManager
    players_data: Dict[str, Player]
