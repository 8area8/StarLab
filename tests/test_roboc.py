"""Test of the roboc modul."""

import unittest
from collections import namedtuple

from roboc import _change_interface
import f_roboc.images as f_images
from f_roboc.main_menu.main_menu import MainMenu
from f_roboc.select_level.select_level import SelectLevel
from f_roboc.game.game import Game


class TestRoboc(unittest.TestCase):
    """This class test the roboc's functions."""

    def test_change_interface(self):
        """Test if the interface is changed.

        We make a fake interface, and fake connexion.
        """
        FakeInterface = namedtuple('Interface', 'go_to')
        images = f_images.get_content_of('f_roboc/assets/images/')

        connexion = 1

        possibles_values = ['main_menu', 'select_level', 'game', '']
        possibles_classes = [MainMenu, SelectLevel, Game]

        for value, class_type in zip(possibles_values, possibles_classes):
            interface = FakeInterface(value)

            interface = _change_interface(interface, images, connexion)

            self.assertIsInstance(interface, class_type)
