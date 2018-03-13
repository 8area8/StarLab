"""Class who rules the button menu of game interface."""

from f_roboc.sprites_classes.main_sprite import MainSprite, ButtonGame


class TimeSprite(MainSprite):
    """Small class who return an image that represent the timer.

    To use it:
        - use 'choose_index' function to set a new index,
          and change the actual image.
        - don't forget to give the 'active_turn' parameter to the function.
    """

    def __init__(self, images, coords, name):
        """Initialization."""
        super().__init__()

        # IMAGES
        self.images = images[10:]
        self.passive_images = images[:10]
        self.image = self.images[self.index]

        # POSITION
        self.coords = coords
        self._init_rect_position()

        # NAME
        self.name = name

    def choose_index(self, index, active_turn):
        """Update the sprite image."""
        self._index = index

        if active_turn:
            self.image = self.images[self._index]
        else:
            self.image = self.passive_images[self._index]


class BullSprite(ButtonGame):
    """Class for the bull object."""
    __doc__ += ButtonGame.__doc__

    def __init__(self, images, coords):
        """Initialization."""
        super().__init__(images[14], images[13], images[:11],
                         images[15], coords, 'bull')
