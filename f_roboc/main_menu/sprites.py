"""This module rules the main menu's sprites."""

import pygame

import constants.game_sizes as csize

from f_roboc.sprites_classes.main_menu_sprites import MainMenuLoop
from f_roboc.sprites_classes.main_menu_sprites import MainMenuButtons
from f_roboc.sprites_classes.main_menu_sprites import LostConnexion
from f_roboc.sprites_classes.main_menu_sprites import joinButton


class SpritesController:
    """Main class."""

    def __init__(self, images):
        """Initialization."""
        self.images = images

        self.main_surface = pygame.Surface(csize.SCREEN_SIZE)

        self.background = MainMenuLoop(images["background"])

        self.commencer = MainMenuButtons(
            self.images['buttons'][0],
            self.images['buttons'][1],
            (266 * csize.UPSCALE, 250 * csize.UPSCALE),
            name='commencer')

        self.rejoindre = joinButton(
            self.images['buttons'][2],
            self.images['buttons'][3],
            self.images['buttons'][4],
            (266 * csize.UPSCALE, 286 * csize.UPSCALE),
            name='rejoindre')

        self.quitter = MainMenuButtons(
            self.images['buttons'][5],
            self.images['buttons'][6],
            (266 * csize.UPSCALE, 321 * csize.UPSCALE),
            name='quitter')

        self.button_list = pygame.sprite.Group()
        self.button_list.add(
            self.commencer,
            self.rejoindre,
            self.quitter)

        self.lost_connexion = LostConnexion(
            self.images['error'],
            (263 * csize.UPSCALE, 191 * csize.UPSCALE),
            name='lost_connexion')
