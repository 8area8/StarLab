"""Module qui crée les boutons de jeu."""

import pygame


class SpriteButton(pygame.sprite.Sprite):
    """Cette classe crée un bouton qui change d'image si on pointe dessus."""

    def __init__(self, activated_img, neutral_img, coords,
                 name, anim_imgs=None, time_per_img=None):
        """Initialisation."""
        pygame.sprite.Sprite.__init__(self)

        self.name = name

        self.neutral = neutral_img
        self.activated = activated_img

        self.image = self.neutral
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords

        self.in_animation = False
        if anim_imgs:
            self.images = anim_imgs
            self.time_per_img = time_per_img
            self.current_time = 0
            self.index = 0

    def update(self):
        """Mise à jour."""
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if self.image is not self.activated:
                self.image = self.activated
        else:
            if self.image is not self.neutral:
                self.image = self.neutral

        if self.in_animation:
            if self.index + 1 > len(self.images):
                self.in_animation = False
                self.index = 0
                self.image = self.activated
            else:
                self.image = self.images[self.index]
                self.current_time += 33.4
                if self.current_time >= self.time_per_img[self.index]:
                    self.current_time = 0
                    self.index = self.index + 1
