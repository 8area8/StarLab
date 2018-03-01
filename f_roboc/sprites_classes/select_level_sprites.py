"""Sprites classes for SelectLevel interface."""

from f_roboc.sprites_classes.main_sprite import MainSprite


class NotImplementedSprite(MainSprite):
    """Appear for a limited time if activated."""

    def __init__(self, image, coords):
        """Initialize the class."""
        super().__init__()

        self.name = 'not_implemented'
        self._active_image = image
        self.image = image

        self.coords = coords
        self._init_rect_position()

        self._max_time = 600

    def update(self):
        """Update the sprite."""
        if self.activated:
            if self.image == self._no_image:
                self.image = self._active_image

            self._call_method_after_timer(self.desactivate, self._max_time)

        elif self.image == self._active_image:
            self.image = self._no_image


class UnactivatedSprite(MainSprite):
    """Sprite who's not activated in first."""

    def __init__(self, image, coords, name):
        """Initialize the sprite."""
        super().__init__()

        self._active_image = image
        self.image = image

        self.coords = coords
        self._init_rect_position()

        self.name = name

    def update(self):
        """Update the sprite."""
        if self.activated:
            self.image = self._active_image
        else:
            self.image = self._no_image
