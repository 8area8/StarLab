"""Module de gestion des sprites de la classe Game."""

import pygame

import f_roboc.constants as cst

from f_roboc.sprites_classes.case_sprite import CaseSprite as CaseSprite
from f_roboc.sprites_classes.map_sprite import MapSprites as MapSprites

from f_roboc.sprites_classes.animated_sprites import SpriteLoop as SpriteLoop
from f_roboc.sprites_classes.sprites_buttons import SpriteButton


class SpritesController:
    """Main class."""

    def __init__(self, imgs, map_name=None):
        """Init."""
        self.imgs = imgs

        self.main_surface = pygame.Surface(
            cst.SCREEN_SIZE)

        if map_name:
            if 'salt' in map_name:
                raise ValueError('Decors de type salt non implentes.')
                return

        self.map_surface = invi.InvisibleSurface(
            640, 288, 0, 0)
        self.map_group = pygame.sprite.Group()
        self.map_group.add(self.map_surface)

        self.cases_group = MapSprites()

    def create_map(self, map_contents):
        """Incorpore chaque case dans un groupe de sprite."""
        x = 0
        y = 0
        nature = ''
        true_coords = ()

        for line in map_contents:

            x = 0
            for word in line:
                true_coords = x * cst.CASE_SIZE, y * cst.CASE_SIZE

                if word == ".":
                    nature = 'spawner'
                elif word == ' ':
                    nature = 'path'
                elif word == 'O':
                    nature = 'wall'
                elif word == 'T':
                    nature = 'teleporter'
                elif word == 'V':
                    nature = 'victory'
                else:
                    nature = word

                self.cases_group[x, y] = CaseSprite(
                    self.cases, nature, true_coords)

                x += 1
            y += 1

        print('map cree.')
        print(self.cases_layer)
