"""Module de transform."""

import pygame

import f_roboc.constants as cst


class TransformPaths(pygame.sprite.Group):
    """Clas."""

    def __init__(self, img, hero, others):
        """Init."""
        pygame.sprite.Group.__init__(self, )

        self.img = img
        self.hero = hero
        self.others = others

    def draw(self, active_turn, surface):
        """Redefinit vite fait la méthode draw."""
        if active_turn:
            pygame.sprite.Group.draw(self, surface=surface)

    def show_possibles_cases(self, cases_list):
        """show."""
        self.empty()

        x, y = self.hero.abstract_coords
        left = x - 1, y
        right = x + 1, y
        top = x, y - 1
        down = x, y + 1

        neighbour_coords = [left, right, top, down]
        for coords in neighbour_coords:
            if coords not in cases_list.keys():
                continue
            if cases_list[coords].nature == 'teleporter':
                continue
            if cases_list[coords].nature == 'victory':
                continue
            if coords in [y.abstract_coords for y in self.others]:
                continue

            self.add(TransformCase(self.img, coords))


class TransformCase(pygame.sprite.Sprite):
    """Ee<."""

    def __init__(self, image, coords):
        """init."""
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.coords = coords

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = cst.get_true_coords(self.coords)
