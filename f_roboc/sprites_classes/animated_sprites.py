"""."""

import pygame


class PonctualSprite(pygame.sprite.Sprite):
    """Crée des Sprites qui s'affichent un temps donné."""

    def __init__(self, img, coords, name, max_time=None, infinite=None):
        """Initialisation."""
        pygame.sprite.Sprite.__init__(self)

        if max_time and infinite:
            raise ValueError("max_time et infinite"
                             "ne peuvent être spécifiés en même temps.")

        self.image_activated = img
        self.no_image = pygame.Surface(
            [1, 1], pygame.SRCALPHA, 32).convert_alpha()
        self.image = self.no_image

        self.name = name
        self.rect = self.image.get_rect()
        self.coords = coords
        self.rect.x, self.rect.y = coords

        self.activated = False
        self.current_time = 0
        self.max_time = max_time

        self.infinite = infinite

    def update(self):
        """Mise à jour."""
        if self.activated:
            if self.max_time:
                if self.current_time >= self.max_time:
                    self.activated = False
                    self.image = self.no_image
                    self.current_time = 0
                    return

            if self.image == self.no_image:
                self.image = self.image_activated
                self.rect = self.image.get_rect()
                self.rect.x, self.rect.y = self.coords

            if self.max_time:
                self.current_time += 33.4

        elif self.image == self.image_activated:
            self.image = self.no_image


class TimeSprite(pygame.sprite.Sprite):
    """Cette classe possède une liste d'images."""

    def __init__(self, imgs, coords, name):
        """Init."""
        pygame.sprite.Sprite.__init__(self)

        self.imgs = imgs[10:]
        self.passive_imgs = imgs[:10]
        self.coords = coords
        self.name = name

        self.index = 0
        self.image = self.imgs[self.index]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.coords

    def choose_index(self, index, active_turn):
        """Update."""
        self.index = index

        if active_turn:
            self.image = self.imgs[self.index]
        else:
            self.image = self.passive_imgs[self.index]


class BullSprite(pygame.sprite.Sprite):
    """Class for the bull object."""

    def __init__(self, imgs, coords, name):
        """Initialisation."""
        pygame.sprite.Sprite.__init__(self)
        self.name = name

        self.images = imgs[:11]
        self.activated_img = imgs[12]
        self.clic_on_img = imgs[13]
        self.inactive_img = imgs[14]
        self.time_per_img = 100

        self.index = 0
        self.current_time = 0.0
        self.image = self.images[self.index]
        self.coords = coords
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.coords

        self.ascend = True
        self.activated = True
        self.on_clic = False
        self.current_on_clic_time = 0.0

    def update(self, active_turn):
        """Mise à jour de l'animation."""
        if self.on_clic:
            self.image = self.clic_on_img
            self.current_on_clic_time += 33.4

            if self.current_on_clic_time >= 100:
                self.current_on_clic_time = 0.0
                self.on_clic = False
            return

        if not active_turn:
            self.image = self.inactive_img
            return

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.activated:
                self.activated = True
        else:
            if self.activated:
                self.activated = False

        self.current_time += 33.4
        if self.current_time >= self.time_per_img:
            self.current_time = 0.0

            if self.ascend:
                if self.index == len(self.images) - 1:
                    self.ascend = False
                else:
                    self.index += 1
            else:
                if self.index == 0:
                    self.ascend = True
                else:
                    self.index -= 1

        if self.activated:
            self.image = self.activated_img
        else:
            self.image = self.images[self.index]


class AnimatedPonctualSprite(pygame.sprite.Sprite):
    """Class."""

    def __init__(self, imgs_dict, coords, name, endless=False):
        """Init."""
        pygame.sprite.Sprite.__init__(self)

        self.imgs = []
        self.time_per_img = []

        for value in imgs_dict.values():
            self.imgs.append(value[0])
            self.time_per_img.append(value[1])

        self.no_image = pygame.Surface(
            [1, 1], pygame.SRCALPHA, 32).convert_alpha()
        self.image = self.no_image

        self.name = name
        self.rect = self.imgs[4].get_rect()
        self.coords = coords
        self.rect.x, self.rect.y = coords

        self.index = 0
        self.current_time = 0.0

        self.activated = False

    def start_anim(self):
        """Initialise the animation."""
        self.index = 0
        self.current_time = 0.0
        self.activated = True

    def update(self, *args):
        """Maj."""
        if self.activated:
            self.current_time += 33.4
            if self.current_time >= self.time_per_img[self.index]:
                self.current_time = 0.0
                self.index += 1

            if self.index == len(self.imgs):
                self.index = 0
                self.image = self.no_image
                self.activated = False
            else:
                self.image = self.imgs[self.index]


class TransformSprite(pygame.sprite.Sprite):
    """Class."""

    def __init__(self, imgs, coords, name):
        """Initialisation."""
        pygame.sprite.Sprite.__init__(self)
        self.name = name

        self.imgs = imgs[:4]
        self.activated_img = imgs[4]
        self.clic_on_img = imgs[5]
        self.inactive_img = imgs[6]
        self.time_per_img = (3000, 100, 100, 1000)

        self.index = 0
        self.current_time = 0.0
        self.image = self.imgs[self.index]
        self.coords = coords
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.coords

        self.ascend = True
        self.activated = True
        self.on_clic = False
        self.current_on_clic_time = 0.0

        self.desactivated = False

    def update(self, active_turn):
        """Mise à jour de l'animation."""
        if not active_turn:
            self.desactivated = False
            self.image = self.inactive_img
            return
        elif self.desactivated:
            self.image = self.inactive_img
            return

        if self.on_clic:
            self.image = self.clic_on_img
            self.current_on_clic_time += 33.4

            if self.current_on_clic_time >= 150:
                self.current_on_clic_time = 0.0
                self.on_clic = False
            return

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.activated:
                self.activated = True
        else:
            if self.activated:
                self.activated = False

        self.current_time += 33.4
        if self.current_time >= self.time_per_img[self.index]:
            self.current_time = 0.0

            if self.ascend:
                if self.index == len(self.imgs) - 1:
                    self.ascend = False
                else:
                    self.index += 1
            else:
                if self.index == 0:
                    self.ascend = True
                else:
                    self.index -= 1

        if self.activated:
            self.image = self.activated_img
        else:
            self.image = self.imgs[self.index]


class TransformAnimSprite(pygame.sprite.Sprite):
    """Class de l'animation transform."""

    def __init__(self, imgs, name):
        """Init."""
        pygame.sprite.Sprite.__init__(self)

        self.imgs = imgs
        self.name = name

        self.case = None

        self.no_image = pygame.Surface(
            [1, 1], pygame.SRCALPHA, 32).convert_alpha()

        self.image = self.no_image
        self.rect = self.imgs[0].get_rect()

    def define_coords(self, coords):
        """Deinit les coordds."""
        self.rect.x, self.rect.y = coords
        print("in define coords:", coords)

    def play_animation(self, index=None, end=False):
        """Update."""
        if end:
            self.image = self.no_image
        else:
            self.image = self.imgs[index]
