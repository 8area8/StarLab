"""Test of the roboc modul."""

import unittest

from roboc import _change_interface

import f_roboc.images as f_images
from f_roboc.main_menu.main_menu import MainMenu
from f_roboc.select_level.select_level import SelectLevel
from f_roboc.game.game import Game
from f_roboc.connection import ServerConnection


class TestRoboc(unittest.TestCase):
    """This class test the roboc's functions."""

    def test_change_interface(self):
        """Test if the interface is changed."""
        pass
