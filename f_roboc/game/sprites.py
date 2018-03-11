"""Game and Game_initiator sprite module."""

import pygame

import constants.game_sizes as csizes


class GameInitSprites:
    """The game initiator sprite class."""

    def __init__(self, imgs):
        """Initialisation."""

        self.main_surface = pygame.Surface(
            csizes.SCREEN_SIZE)

        self.background = imgs[0]
