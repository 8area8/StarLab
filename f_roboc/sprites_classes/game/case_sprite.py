"""Module that contains the cases sprite of the game.

The class contains all case images of the game.
"""

import pygame
import random


class CaseSprite(pygame.sprite.Sprite):
    """The case sprites class."""

    def __init__(self, images, nature, coords, number):
        """Initalization."""
        super().__init__()

        self.images = images

        # ATTRIBUTS
        self.nature = nature
        self.name = 'undefined'
        self.coords = coords
        self.number = number
        self.solid = False

        # SPRITE DEFINITION
        self.image = None
        self._define_nature(nature)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.coords

        # ANIMATIONS.
        self.imgs_tp = images['teleporter']
        self.imgs_wall_rare = self.images["wall_rare"]
        self._index = 0
        self._current_time = 0.0

    def _define_nature(self, nature):
        """Define the sprite nature.

        This method define the 'solid' attribut,
        the name and the image of the sprite.
        """
        if nature == 'path':
            self.nature = nature
            rand = random.randint(1, 12)
            if rand > 1:
                self.image = self.images['simples'][0]
                self.name = 'path'
            else:
                self.image = self.images["simples"][1]
                self.name = 'path_rare'
            self.solid = False

        elif nature == 'wall':
            self.nature = nature
            self.solid = True
            rand = random.randint(1, 6)
            if rand > 1:
                self.image = self.images['simples'][2]
                self.name = 'wall'
            else:
                self.image = self.images["wall_rare"][0]
                self.name = 'wall_rare'

        elif nature == 'teleporter':
            self.nature = nature
            self.name = 'teleporter'
            self.solid = False
            self.image = self.images['teleporter'][0]

        elif nature == 'victory':
            self.nature = nature
            self.name = 'victory'
            self.solid = False
            self.image = self.images['simples'][0]

        else:
            raise ValueError("incorrect nature!\n"
                             "Only 'path', 'wall', 'spawner', 'victory' and "
                             "'teleporter' are correct natures.\n"
                             f"actual nature: {nature}.")

    def transform(self):
        """Transform the sprite nature."""
        if self.nature == 'wall':
            self._define_nature("path")
        elif self.nature == "path":
            self._define_nature("wall")
        else:
            raise ValueError("We can't transform this case.")

    def update(self):
        """Update the sprite.

        Only used for the animated sprites
        """
        if self.name not in ["teleporter", "wall_rare"]:
            return

        over = 100 if self.name == 'teleporter' else 120

        self._current_time += 33.4
        if self._current_time >= over:
            self._current_time = 0
            self._index = (self._index + 1) % len(self.images[self.name])
            self.image = self.images[self.name][self._index]
