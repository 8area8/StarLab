"""Big module that contains a sprite group.

Has keys to control each element,
in function of their coordinates.
"""

import pygame


class MapSprites(pygame.sprite.Group):
    """The module class.

    It is as 'Group' from pygame.sprite, to wich i implement
    a dictionnary to better control/browse.
    """

    def __init__(self):
        """Initialization."""
        pygame.sprite.Group.__init__(self)

        self._coords = {}

    def __getitem__(self, key):
        """Allows you to simply retrieve a value from the group.

        We will use "MapSprite[key]".
        """
        if key in self._coords:
            return self._coords[key]
        else:
            raise KeyError(f"The key '{key}' doesn't exist!")

    def __setitem__(self, key, value):
        """Allows you to add values ​​to the group.

        We'll use "MapSprite[key] = value"

        The key must be a tuple that's correspond to coordinates,
        and the value an instance of LabyrinthSprite.
        """
        if key in self._coords:
            self.remove(self.coords[key])

        self.add(value)
        self._coords[key] = value

    def keys(self):
        """Return the self._coord key."""
        return self._coords.keys()

    def find_another_teleporter(self, tp_coords):
        """Return another teleporter."""
        for case in self.sprites():
            if case.nature == "teleporter" and case.coords != tp_coords:
                return case.coords
