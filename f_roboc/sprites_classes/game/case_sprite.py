"""Module contenant la classe de sprite des éléments du jeu.

La classe contient déjà toutes les images de chaque case du jeu.
C'est en modifiant sa nature que l'objet changera d'image et d'attribus.
"""

import pygame
import random


class CaseSprite(pygame.sprite.Sprite):
    """La classe du module."""

    def __init__(self, cases, nature, coords, number):
        """Initalisation."""
        pygame.sprite.Sprite.__init__(self)

        self.cases = cases

        # Cette partie comprend les attributs propres au jeu.
        self.nature = nature
        self.name = 'undefined'
        self.coords = coords
        self.number = number
        self.solid = False

        # partie propre à la définition du sprite.
        self.image = None
        self.define_nature(nature)  # Définit les caracs de l'objet.

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.coords

        # Cette partie ne concerne que l'animation du teleporter.
        self.imgs_tp = cases['tp']
        self.imgs_wall_rare = self.cases["wall_rare"]
        self.index = 0
        self.current_time = 0.0

    def define_nature(self, nature):
        """On définit la nature du sprite."""
        if nature == 'path':
            self.nature = nature
            rand = random.randint(1, 12)
            if rand > 1:
                self.image = self.cases['path']
                self.name = 'path'
            else:
                self.image = self.cases["path_rare"]
                self.name = 'path_rare'
            self.solid = False

        elif nature == 'wall':
            self.nature = nature
            self.solid = True
            rand = random.randint(1, 6)
            if rand > 1:
                self.image = self.cases['wall']
                self.name = 'wall'
            else:
                self.image = self.cases["wall_rare"]['image 1'][0]
                self.name = 'wall_rare'

        elif nature == 'teleporter':
            self.nature = nature
            self.name = 'teleporter'
            self.solid = False
            self.image = self.cases['tp']["image 1"][0]

        elif nature == 'victory':
            self.nature = nature
            self.name = 'victory'
            self.solid = False
            self.image = self.cases['path']

        else:
            raise ValueError("nature incorrecte!\n\
                'path', 'wall', 'spawner', 'victory' et \
                'teleporter' sont les 5 types possibles.\n\
                type actuel définit: {0}".format(nature))

    def transform(self):
        """Transform."""
        if self.nature == 'wall':
            self.define_nature("path")
        elif self.nature == "path":
            self.define_nature("wall")
        else:
            raise ValueError("On ne peut transformer cette case.")

    def update(self):
        """Mise à jour."""
        if self.name == 'teleporter':
            self.current_time += 33.4
            if self.current_time >= 100:
                self.current_time = 0
                self.index = (self.index + 1) % len(self.imgs_tp)
                self.image = self.imgs_tp["image {}".format(self.index + 1)][0]
        elif self.name == 'wall_rare':
            self.current_time += 33.4
            if self.current_time >= 300:
                self.current_time = 0
                self.index = (self.index + 1) % len(self.imgs_wall_rare)
                self.image =\
                    self.imgs_wall_rare["image {}".format(self.index + 1)][0]
