"""This modul contain the parent's class of all unitest classes."""
import unittest
import pygame


class PygameTest(unittest.TestCase):
    """This class just has a setUp for the pygame's window implementation."""

    def setUp(self):
        """Implement the pygame's window."""
        self.main_screen = pygame.display.set_mode((1280, 720))
