"""Module très important, il contient un groupe de sprite.

Possède des clés pour mieux controler les éléments,
en fonction de leur coordonnées.
"""

import pygame


class MapSprites(pygame.sprite.Group):
    """La classe du module.

    C'est une classe 'Group' de pygame.sprite, à laquelle j'implémente
    un dictionnaire pour mieux la controler/parcourir.
    """

    def __init__(self):
        """Initialisation."""
        pygame.sprite.Group.__init__(self)

        self._coords = {}

    def __getitem__(self, key):
        """Permet de récupérer simplement une valeur du groupe.

        On utilisera "MapSprite[key]".
        """
        if key in self._coords:
            return self._coords[key]
        else:
            raise KeyError("La clé '{0}' n'existe pas!".format(key))

    def __setitem__(self, key, value):
        """Permet d'ajouter simplement des valeurs au groupe.

        On utilisera "MapSprite[key] = value"

        la clé doit être un tuple correspondant à des coordonnées,
        et la valeur une instance de LabyrinthSprite.

        Le premier teste regarde si la clé existe déjà (donc
        si on a déjà définit cette coordonnée): si elle
        existe, on enlève la valeur correspondante (qui est un sprite)
        au groupe de sprites.
        """
        if key in self._coords:
            self.remove(self.coords[key])

        self.add(value)
        self._coords[key] = value

    def keys(self):
        """Retoune les clés de self._coord."""
        return self._coords.keys()
