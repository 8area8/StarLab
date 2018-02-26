"""Module de gestion des sprites de la classe Introduction."""

import pygame

import f_roboc.constants as cst

from f_roboc.sprites_classes.animated_sprites import PonctualSprite


class SpritesController:
    """Main class."""

    def __init__(self, imgs):
        """Init."""
        self.imgs = imgs

        self.main_surface = pygame.Surface(
            cst.SCREEN_SIZE)

        self.presentation = PonctualSprite(
            self.imgs["presentation"],
            (0, 0),
            "presentation",
            infinite=True)

        self.hors_line = PonctualSprite(
            self.imgs["hors_line"],
            (0, 0),
            "hors_line",
            infinite=True)
