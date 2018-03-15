"""This module regroup all animated info sprites."""

from constants import coordinates as csc
from constants import game_sizes as csizes
from f_roboc.sprites_classes.main_sprite import MainSprite, Button


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
            if self._current_time >= self.time_per_img[self._index]:
                self._refresh_timer(set_zero=True)
                self._index += 1

            if self._index == len(self.images):
                self._index = 0
                self.image = self._no_image
                self.activated = False
            else:
                self.image = self.images[self._index]


class TransformAnim(MainSprite):
    """Transform animation.

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
        self.rect.x, self.rect.y = csc.transform_coords_to('real', coords)

    def play_animation(self, index=None, end=False):
        """Update the animation."""
        if not end:
            self.image = self.images[index]
        else:
            self.image = self._no_image


class SpaceShip(MainSprite):
    """The spaceship item.

    To use it:
        - Just call it with the 'activate()' method, to drop it.
        - call the Victory when the 'end' attribute is True
    """

    def __init__(self, images, coords):
        """Initialization."""
        super().__init__(no_images=True)

        # IMAGES
        self.images_group = images
        self._key_image = "ship_highlight"
        self.image = self.images[self._index]

        # POSITION
        self.coords = coords
        self._init_rect_position()

        # TIME PER IMAGE
        self._time_images = {
            "ship_highlight": [500, 100, 100, 100, 100, 100],
            "ship_droped": [100 for x in range(5)]}

        # INFOS
        self.name = "ship"
        self.end = False

    @property
    def images(self):
        """Return the actual images."""
        return self.images_group[self._key_image]

    def update(self, *args):
        """Update the ship."""
        key = self._key_image
        i = self._index

        if self.activated:
            self._key_image = 'ship_droped'
            self._refresh_timer()
            self.rect.y -= 6
            if self._current_time >= self._time_images[key][i]:
                self._refresh_timer(set_zero=True)
                if self._index < len(self.images) - 1:
                    self._index += 1
                else:
                    self.end = True
            self.image = self.images[self._index]
            return

        self._refresh_timer()
        if self._current_time >= self._time_images[key][i]:
            self._refresh_timer(set_zero=True)
            self._set_ping_pong_index(len_img=self._return_len_images())
            self.image = self.images[self._index]

    def _return_len_images(self):
        """Simply return the len of current images key."""
        return len(self.images) - 1


class Victory(MainSprite):
    """The victory class.

    To use it:
        - Call the 'activate()' function to activate it,
          and don't forget the parameters.
        - self.button.rect to collidepoint the button.
    """

    def __init__(self, images, coords):
        """Initialization."""
        super().__init__()

        # INFORMATIONS
        self.name = 'victory'
        self.active_turn = None
        self.player = None

        # IMAGES
        self.images = images["animation"]
        self.image = self._no_image
        assets = images['assets']
        self.defeat = assets[0]
        self.victory = assets[1]
        main_menu_active = assets[2]
        main_menu = assets[5]
        self.superstar = assets[4]
        self.superalien = assets[3]

        self.coords = coords
        self._init_rect_position()

        # SUBSPRITE
        coords = self._get_sub_coords(251 * csizes.UPSCALE,
                                      219 * csizes.UPSCALE)
        self.button = Button(
            main_menu_active,
            main_menu,
            coords,
            "main_menu")
        self.button.adjust_rect_position(self.coords)

    def activate(self, active_turn, player):
        """Activate."""
        self.activated = True
        self.active_turn = active_turn
        self.player = player

    def update(self):
        """Update the sprite."""
        if not self.activated:
            return

        self.button.update()

        self._refresh_timer()
        if self._current_time >= 100:
            self._refresh_timer(set_zero=100)
            if self._index < len(self.images) - 1:
                self._index += 1
                self.image = self.images[self._index].copy()

        if self._index == 9:
            self._blit_the_player_status()
            self.image.blit(self.button.image, self.button.coords)

    def _blit_the_player_status(self):
        """Blit the player status."""
        victory = self.victory if self.active_turn else self.defeat
        coords = self._get_sub_coords(224 * csizes.UPSCALE,
                                      163 * csizes.UPSCALE)
        self.image.blit(victory, coords)

        if self.player == "superalien":
            coords = self._get_sub_coords(216 * csizes.UPSCALE,
                                          24 * csizes.UPSCALE)
            self.image.blit(self.superalien, coords)
        else:
            coords = self._get_sub_coords(240 * csizes.UPSCALE,
                                          39 * csizes.UPSCALE)
            self.image.blit(self.superstar, coords)

    def _get_sub_coords(self, x, y):
        """Get the good coords for subimages."""
        x = x - self.coords[0]
        y = y - self.coords[1]

        return x, y
