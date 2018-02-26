"""Module de gestion des sprites de la classe Introduction."""

import pygame

import constants.game_sizes as gsizes


class SpritesController:
    """Main class."""

    def __init__(self, images):
        """Init."""
        self.main_surface = pygame.Surface(
            gsizes.SCREEN_SIZE)

        self.presentation = images[0]
