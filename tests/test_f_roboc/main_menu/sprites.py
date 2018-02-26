"""Module de gestion des sprites de la classe MainMenu."""

import pygame

import f_roboc.constants as cst

from f_roboc.sprites_classes.animated_sprites import SpriteLoop as SpriteLoop
from f_roboc.sprites_classes.sprites_buttons import SpriteButton


class SpritesController:
    """Main class."""

    def __init__(self, imgs):
        """Init."""
        self.imgs = imgs

        self.main_surface = pygame.Surface(
            cst.SCREEN_SIZE)

        self.background = SpriteLoop(imgs["bg"])

        self.commencer = SpriteButton(
            self.imgs['buttons']["commencer_act"],
            self.imgs['buttons']["commencer_neutr"],
            (266 * cst.UPSCALE, 250 * cst.UPSCALE),
            name='commencer')
        self.aide = SpriteButton(
            self.imgs['buttons']['aide_act'],
            self.imgs['buttons']['aide_neutr'],
            (266 * cst.UPSCALE, 286 * cst.UPSCALE),
            name='aide')
        self.quitter = SpriteButton(
            self.imgs['buttons']['quitter_act'],
            self.imgs['buttons']['quitter_neutr'],
            (266 * cst.UPSCALE, 321 * cst.UPSCALE),
            name='quitter')

        self.button_list = pygame.sprite.Group()
        self.button_list.add(
            self.commencer,
            self.aide,
            self.quitter)
