"""module contenant les classes de héro."""

import pygame

import constants.game_sizes as cst
from f_roboc.sprites_classes.main_sprite import MainSprite


class Hero(MainSprite):
    """Base heros class."""

    def __init__(self, images, coords, name, digit, is_yours):
        """Init."""
        pygame.sprite.Sprite.__init__(self)

        # NAME
        self.name = name

        # IMAGES
        self.images = images
        self.key_imgs = "breath"
        self.image = self.images[self.key_imgs][self.index]

        # POSITION
        self.coords = coords
        self._init_rect_position()

        # TIME PER IMAGE
        self.get_times_per_imgs()

        # SKILLS
        self.activate_skills()

        # PLAYER'S INFORMATIONS
        self.is_yours = is_yours
        self.digit = digit

    @property
    def abstract_coords(self):
        """Get abstract coords."""
        return cst.get_abstract_coords(self.coords)

    @property
    def x(self):
        """Return x."""
        return self.coords[0]

    @property
    def y(self):
        """Return y."""
        return self.coords[1]

    @property
    def has_moove(self):
        """Has moove."""
        if self.actual_moove > 0:
            return True
        else:
            return False

    def activate_skills(self):
        """Init caract."""
        self.moove_points = 3
        self.actual_moove = self.moove_points
        self.transform_spell = True

    def get_times_per_imgs(self):
        """Create a dict who contains max timer lists."""
        if self.name == "superstar":
            self.time_imgs["breath"] = [120 for x in range(5)]
            self.time_imgs["transform"] = [150 for x in range(4)]
        else:
            self.time_imgs["breath"] = [150, 120, 120, 180, 250]
            self.time_imgs["transform"] = [130 for x in range(5)]

        moove = [100 for x in range(4)]
        self.time_imgs["moove_r"] = moove[:]
        self.time_imgs["moove_l"] = moove[:]
        self.time_imgs["moove_d"] = moove[:]
        self.time_imgs["moove_t"] = moove[:]

    def activate_hero(self, key, index_img, coords):
        """Activate the hero's moove."""
        self.index = index_img
        self.coords = coords
        self.define_key_imgs(key)

    def define_key_imgs(self, key):
        """Define the hero's status."""
        if key == self.key_imgs:
            return

        if key in self.imgs.keys():
            self.key_imgs = key
            self.current_time_imgs = self.time_imgs[key]
            self.index = 0
        else:
            raise KeyError()

    def moove(self, coords):
        """Moove the hero."""
        x, y = self.coords
        a, b = coords
        if x < a:
            self.define_key_imgs("moove_r")
        elif x > a:
            self.define_key_imgs("moove_l")
        elif y < b:
            self.define_key_imgs("moove_t")
        elif y > b:
            self.define_key_imgs("moove_d")
        else:
            print("IN HEROES. POSITION IS THE SAME!")
        self.coords = coords

    def update(self):
        """Update the hero."""
        self.rect.x, self.rect.y = self.coords
        self.image = self.imgs[self.key_imgs][self.index]

        key = self.key_imgs
        if key is "breath":
            self._call_method_after_timer(self._set_ping_pong_index, 33.4)

        if key is "transform" or "moove" in key:
            self.current_frame += 33.4
            if self.current_frame >= self.time_imgs[key][self.index]:
                self.current_frame = 0.0
                self.index = (self.index + 1) % len(self.imgs[key])
