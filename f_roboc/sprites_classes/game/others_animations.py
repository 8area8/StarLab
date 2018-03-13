"""This module regroup all animated info sprites."""

from f_roboc.sprites_classes.main_sprite import MainSprite


class NextTurn(MainSprite):
    """Display the next_turn animation.

    To use it:
        - call the 'activate()' function to launch the sprite.
        - that's it.
    """

    def __init__(self, images, coords):
        """Initialization."""
        super().__init__()

        self.images = images
        self.image = self._no_image

        self.time_per_img = (100, 30, 30, 30, 180, 50, 900, 100, 100, 100, 100)

        self.name = "next_turn"

        self.coords = coords
        self.rect = self.images[4].get_rect()
        self.rect.x, self.rect.y = coords

    def update(self, *args):
        """Update the sprite."""
        if self.activated:
            self._refresh_timer()
            if self.current_time >= self.time_per_img[self._index]:
                self._refresh_timer(set_zero=True)
                self._index += 1

            if self._index == len(self.images):
                self._index = 0
                self.image = self._no_image
                self.activated = False
            else:
                self.image = self.images[self._index]


class TransformAnimSprite(MainSprite):
    """Transform sprite animation.

    To use it:
        - First define the (real) coordinates of the animation.
        - use 'play_animation() function to set an index and show an image.
        - set 'end' parameter to 'True' if you want to stop the animation.
    """

    def __init__(self, images, name):
        """Initialization."""
        super().__init__()

        self.images = images
        self.image = self._no_image

        self.name = name

        self.rect = self.images[0].get_rect()

    def define_coords(self, coords):
        """Define the coordinates."""
        self.rect.x, self.rect.y = coords

    def play_animation(self, index=None, end=False):
        """Update the animation."""
        if not end:
            self.image = self.images[index]
        else:
            self.image = self.no_image
