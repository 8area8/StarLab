"""This module contains the main_menu's sprites classes."""

from f_roboc.sprites_classes.main_sprite import MainSprite


class MainMenuLoop(MainSprite):
    """This class rules the main loop of main menu."""

    def __init__(self, images):
        """Initialize the class."""
        super().__init__()

        self.name = "background"

        self.images = images
        self.image = self.images[self._index]

        self._init_rect_position()

    def update(self):
        """Update the animation."""
        self._call_method_after_timer(self._set_ascending_index_loop)

        self._update_image_from_images()


class MainMenuButtons(MainSprite):
    """Rule the main menu's buttons."""

    def __init__(self, active_image, passive_image, coords, name):
        """Initialize the class."""
        super().__init__()

        self.name = name

        self.image = active_image
        self._active_image = active_image
        self._passive_image = passive_image

        self.coords = coords
        self._init_rect_position()

    def update(self, *arg):
        """Update the sprite."""
        self._change_image_if_overflew()


class joinButton(MainMenuButtons):
    """Special class for join's button."""

    def __init__(self, broken_image, active_image,
                 passive_image, coords, name):
        """Init the class."""
        super().__init__(active_image, passive_image, coords, name)

        self._broken_image = broken_image
        self.image = self._broken_image

    def update(self, game_init):
        """Update the sprite."""
        if not game_init:
            self.image = self._broken_image
            return

        self._change_image_if_overflew()


class LostConnexion(MainSprite):
    """This class show an error message."""

    def __init__(self, images, button_coords, name):
        """Initialize the class."""
        super().__init__()

        self.name = name

        self.image = images[0]

        self.coords = (0, 0)
        self._init_rect_position()

        self.button = MainMenuButtons(
            images[2],
            images[1],
            button_coords,
            'ok...')

    def update(self):
        """Update the sprite."""
        if not self.activated:
            return

        self.button.update()

        self.image.blit(self.button.image, self.button.coords)
