"""The transform module."""

import pygame

import constants.coordinates as csc


class SearchTransformPaths(pygame.sprite.Group):
    """This class find and show the possibles transform paths."""

    def __init__(self, image, hero, others):
        """Initialization."""
        pygame.sprite.Group.__init__(self, )

        self.image = image
        self.hero = hero
        self.others = others

    def draw(self, active_turn, surface):
        """Redefine the draw method, that run if active_turn is True."""
        if active_turn:
            pygame.sprite.Group.draw(self, surface=surface)

    def show_possibles_cases(self, cases_list):
        """Show the possibles transform cases."""
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

            self.add(TransformCase(self.image, coords))


class TransformCase(pygame.sprite.Sprite):
    """Create a transform case sprite."""

    def __init__(self, image, coords):
        """Initialization."""
        super().__init__()

        self.image = image
        self.coords = coords

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = csc.transform_coords_to('real', self.coords)
