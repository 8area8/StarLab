"""module contenant les classes de héro."""

import pygame

import constants.game_sizes as cst


class Hero(pygame.sprite.Sprite):
    """Base heros class."""

    def __init__(self, imgs, coords, name, number, is_yours):
        """Init."""
        pygame.sprite.Sprite.__init__(self)

        self.imgs = imgs
        self.coords = coords
        self.name = name
        self.is_yours = is_yours
        self.number = number

        self.current_frame = 0
        self.index = 0
        self.ascend = True

        self.key_imgs = "breath"
        self.image = self.imgs[self.key_imgs][self.index]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.coords

        self.time_imgs = {"breath": [], "transform": []}
        self.get_times_per_imgs()
        self.activate_skills()

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
        """Tru story."""
        if self.name == "superstar":
            self.time_imgs["breath"] = [120 for x in range(5)]
            self.time_imgs["transform"] = [150 for x in range(4)]
        else:
            self.time_imgs["breath"] = [150, 120, 120, 180, 250]
            self.time_imgs["transform"] = [130 for x in range(5)]
        self.time_imgs["moove_r"] = [100 for x in range(4)]
        self.time_imgs["moove_l"] = [100 for x in range(4)]
        self.time_imgs["moove_d"] = [100 for x in range(4)]
        self.time_imgs["moove_t"] = [100 for x in range(4)]

    def activate_hero(self, key, index_img, coords):
        """Activate the hero."""
        self.index = index_img
        self.coords = coords
        self.define_key_imgs(key)

    def define_key_imgs(self, key):
        """BlabLa."""
        if key == self.key_imgs:
            return

        if key in self.imgs.keys():
            self.key_imgs = key
            self.current_time_imgs = self.time_imgs[key]
            self.index = 0
        else:
            raise KeyError()

    def moove(self, coords):
        """Moove."""
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
        """Update."""
        self.rect.x, self.rect.y = self.coords
        self.image = self.imgs[self.key_imgs][self.index]

        key = self.key_imgs
        if key is "breath":
            self.current_frame += 33.4
            if self.current_frame >= self.time_imgs[key][self.index]:
                self.current_frame = 0.0

                if self.ascend:
                    if self.index == len(self.time_imgs[key]) - 1:
                        self.ascend = False
                    else:
                        self.index += 1
                else:
                    if self.index == 0:
                        self.ascend = True
                    else:
                        self.index -= 1

        if key is "transform" or "moove" in key:
            self.current_frame += 33.4
            if self.current_frame >= self.time_imgs[key][self.index]:
                self.current_frame = 0.0
                self.index = (self.index + 1) % len(self.imgs[key])
