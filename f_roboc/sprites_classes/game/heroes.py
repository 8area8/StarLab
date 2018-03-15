"""This module contains the hero's sprite."""

import constants.coordinates as csc
from f_roboc.sprites_classes.main_sprite import MainSprite


class Hero(MainSprite):
    """Base hero's class."""

    def __init__(self, images_group, coords, name, digit, is_yours):
        """Initialization."""
        super().__init__(no_images=True)

        # NAME
        self.name = name

        # IMAGES
        self.images_group = images_group
        self._key_image = "breath"
        self.image = self.images[self._index]

        # POSITION
        self.coords = coords
        self._init_rect_position()

        # TIME PER IMAGE
        self.get_times_per_images()

        # SKILLS
        self.activate_skills()

        # PLAYER'S INFORMATIONS
        self.is_yours = is_yours
        self.digit = digit

    @property
    def images(self):
        """Return the actual images."""
        return self.images_group[self._key_image]

    @property
    def abstract_coords(self):
        """Get abstract coords."""
        return csc.transform_coords_to('abstract', self.coords)

    @property
    def x(self):
        """Return x coordinates."""
        return self.coords[0]

    @property
    def y(self):
        """Return y coordinates."""
        return self.coords[1]

    @property
    def has_moove(self):
        """Test if the hero has moove."""
        if self.actual_moove > 0:
            return True
        else:
            return False

    def activate_skills(self):
        """Initialize the skills."""
        self.moove_points = 3
        self.actual_moove = self.moove_points
        self.transform_spell = True

    def get_times_per_images(self):
        """Create a dict who contains max timer lists."""
        self._time_images = {}

        if self.name == "superstar":
            self._time_images["breath"] = [120 for x in range(5)]
            self._time_images["transform"] = [150 for x in range(4)]
        else:
            self._time_images["breath"] = [150, 120, 120, 180, 250]
            self._time_images["transform"] = [130 for x in range(5)]

        moove = [100 for x in range(4)]
        self._time_images["moove_r"] = moove[:]
        self._time_images["moove_l"] = moove[:]
        self._time_images["moove_d"] = moove[:]
        self._time_images["moove_t"] = moove[:]

    def activate_hero(self, key, index_image, coords):
        """Activate the hero's moove."""
        self._index = index_image
        self.coords = coords
        self.define_key_images(key)

    def define_key_images(self, key):
        """Define the hero's status."""
        if key == self._key_image:
            return

        if key in self.images_group.keys():
            self._key_image = key
            self._index = 0
        else:
            raise KeyError()

    def moove(self, coords):
        """Moove the hero."""
        x, y = self.coords
        a, b = coords
        if x < a:
            self.define_key_images("moove_r")
        elif x > a:
            self.define_key_images("moove_l")
        elif y < b:
            self.define_key_images("moove_d")
        elif y > b:
            self.define_key_images("moove_t")
        else:
            print("In hero. Position is the same!")
        self.coords = coords

    def teleport(self, key=None, index=None, coords=None):
        """Teleport the hero."""
        if coords:
            self.coords = coords
            return

        self.define_key_images(key)
        self._index = index

    def update(self):
        """Update the hero."""
        self.rect.x, self.rect.y = self.coords
        self.image = self.images[self._index]

        key = self._key_image
        if key is "breath":
            self._refresh_timer()
            if self._current_time >= self._time_images[key][self._index]:
                self._refresh_timer(set_zero=True)
                self._set_ping_pong_index(len_img=self._return_len_images())

        if key is "transform" or "moove" in key:
            self._refresh_timer()
            if self._current_time >= self._time_images[key][self._index]:
                self._refresh_timer(set_zero=True)
                self._index = (self._index + 1) % len(self.images)

    def _return_len_images(self):
        """Simply return the len of current images key."""
        return len(self.images) - 1
