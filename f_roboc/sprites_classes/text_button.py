"""Définit les boutons de type texte."""

import pygame

import constants.colors as cons_colors


class TextButton(pygame.sprite.Sprite):
    """La classe des boutons textuels."""

    def __init__(self, text, size, color, active_color,
                 x, y, absolute_x=0, absolute_y=0, w_container=None):
        """Initialisation."""
        pygame.sprite.Sprite.__init__(self)

        self.activated = False

        self.color = cons_colors.find_color(color)
        self.active_color = cons_colors.find_color(active_color)
        self.size = size
        self.text = text
        self.absolute_x = absolute_x
        self.absolute_y = absolute_y

        self.font = pygame.font.Font("f_roboc/assets/"
                                     "police/pixeled.ttf", self.size)
        self.image = self.font.render(self.text, 0, self.color)

        if w_container:
            w, h = self.image.get_size()
            x = center_rect(w, w_container)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y * 2

        self.define_text()

    def define_text(self, activated=False, text=None):
        """Colle le texte sur une surface."""
        text = text if text else self.text
        color = self.active_color if activated else self.color

        self.image = self.font.render(text, 0, color)

    def update(self):
        """Mise à jour."""
        pos = pygame.mouse.get_pos()
        pos = pos[0] - 259 * 2, pos[1] - 160 * 2
        if self.rect.collidepoint(pos):
            if not self.activated:
                self.activated = True
                self.define_text(activated=True)
        else:
            if self.activated:
                self.activated = False
                self.define_text()


class TextMapButton(TextButton):
    """Rule the map buttons. Contains the map."""

    def __init__(self, text, size, color, active_color, x,
                 y, contents, absolute_x=0, absolute_y=0, w_container=None):
        """Initialization."""
        TextButton.__init__(self, text, size, color,
                            active_color, x, y, absolute_x,
                            absolute_y, w_container)

        self.contents = contents


class DynamicTextButton(TextButton):
    """Ultra basic.

    Just use the define_text method with text argument.
    """

    def __init__(self, text, size, x, y):
        """Initialization."""
        TextButton.__init__(self, text, size, "white", "blue", x, y)

    def update(self, *args):
        """Unused."""
        pass


def center_rect(w_rect_to_center, w_rect_container):
    """Prend la largeur des deux rectangles.

    Centre le premier sur le deuxième.
    """
    w_rect_to_center = w_rect_to_center / 2
    w_rect_container = w_rect_container / 2
    x_position = w_rect_container - w_rect_to_center

    return x_position if x_position >= 0 else 0
