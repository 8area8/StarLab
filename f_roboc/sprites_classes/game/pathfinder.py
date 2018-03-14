"""Pathfinder's module."""

import pygame

import constants.coordinates as csc


class PathfindingGroup(pygame.sprite.Group):
    """This class find and show a possible path."""

    def __init__(self, image, hero, the_others):
        """Initialization."""
        pygame.sprite.Group.__init__(self)

        self._hero = hero
        self._others = the_others
        self._abs_coords = csc.RELATIVES_COORDS

        self.path = []

        self._mouse = (0, 0)
        self._image = image

    @property
    def case_hero(self):
        """Hero's case."""
        return PathCase(self._image, self._hero.abstract_coords,
                        0, is_hero=True)

    def draw(self, active_turn, surface):
        """Run only in active_turn is True."""
        if active_turn:
            pygame.sprite.Group.draw(self, surface=surface)

    def active_the_pathfinding(self, mouse, case_group):
        """Activate the pathfinding research."""
        if not mouse:  # If the mouse is over the map/game.
            return

        abstract_mouse = csc.transform_coords_to('abstract', mouse)
        if abstract_mouse == self.mouse:  # If the mouse is on the same case.
            return

        self._mouse = abstract_mouse
        self._calcul_a_new_path(case_group)

    def _calcul_a_new_path(self, case_group):
        """Calculate a new path."""
        print("We calculate a new path.")
        self.empty()
        self.path = []

        coords_lists = self._abs_coords[:self._hero.actual_moove]
        possibles_cases = [[self.case_hero]]

        for i, coords_list in enumerate(coords_lists):
            possibles_cases.append([])  # Add a new moove level

            for r_x, r_y in coords_list:

                x, y = self._hero.abstract_coords
                real_coords = (r_x + x, r_y + y)

                if real_coords not in case_group.keys():  # if doesn't exist.
                    continue
                elif case_group[real_coords].solid:  # if it's a wall
                    continue
                elif real_coords in [y.abstract_coords for y in self._others]:
                    continue  # if others heroes on this case

                # We passed all tests, lets add this case to our path! <3
                possibles_cases[-1].append(PathCase(self._image,
                                                    real_coords, i + 1,
                                                    cases=possibles_cases[-2]))

                if not possibles_cases[-1][-1].path:  # not linked, it's alone.
                    del possibles_cases[-1][-1]

                if possibles_cases[-1] is []:  # no more cases in our list.
                    break

        for cases_list in possibles_cases:
            for case in cases_list:

                if self._mouse == case.coords:
                    print("Path found!")
                    print("\nPath:", case.path)
                    self.path = case.path

                    for case in self.path:
                        self.add(case)
                    return


class PathCase(pygame.sprite.Sprite):
    """The sprite class for the path cases."""

    def __init__(self, image, coords, distance, cases=None, is_hero=False):
        """Initialization."""
        pygame.sprite.Sprite.__init__(self)

        self.coords = coords
        self._distance = distance
        self._is_hero = is_hero

        self.path = []
        self._neighbour_coords = []

        if cases:
            self.image = image
        else:
            self.image = pygame.Surface(
                [1, 1], pygame.SRCALPHA, 32).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.true_coords

        self.get_path(cases)

    def get_path(self, cases):
        """Get the best path to go to this case."""
        if self._is_hero:
            self.path.append(self)
            return

        left = (self.x - 1, self.y)
        right = (self.x + 1, self.y)
        top = (self.x, self.y - 1)
        down = (self.x, self.y + 1)

        self._neighbour_coords = [left, right, top, down]

        for case in cases:
            for coords in self._neighbour_coords:
                if coords == case.coords:
                    self.path = case.path[:]
                    self.path.append(self)
                    return

    @property
    def x(self):
        """Return x."""
        return self.coords[0]

    @property
    def y(self):
        """Return y."""
        return self.coords[1]

    @property
    def true_coords(self):
        """Return reals coords."""
        return csc.transform_coords_to('real', self.coords)
