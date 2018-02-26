"""Pathfinder's modul."""

import pygame

import f_roboc.constants as cst


class PathfindingGroup(pygame.sprite.Group):
    """Main class."""

    def __init__(self, image, hero, the_others):
        """Init."""
        pygame.sprite.Group.__init__(self)

        self._hero = hero
        self._others = the_others
        self._abs_coords = cst.ABSOLUTES_COORDS

        self.path = []

        self._mouse = (0, 0)
        self._image = image

    @property
    def case_hero(self):
        """Case hero."""
        return PathCase(
            self._image, self._hero.abstract_coords, 0, is_hero=True)

    def draw(self, active_turn, surface):
        """Redefinit vite fait la méthode draw."""
        if active_turn:
            pygame.sprite.Group.draw(self, surface=surface)

    def active_the_pathfinding(self, mouse, case_group):
        """Activate."""
        if not mouse:
            return

        m = cst.get_abstract_coords(mouse)
        if m == cst.get_abstract_coords(self._mouse):
            return

        self._mouse = mouse
        self._calcul_a_new_path(case_group)

    def _calcul_a_new_path(self, case_group):
        """Calculate un nouveau chemin."""
        print("on calcul un nouveau chemin.")
        good_coords_lists = self._abs_coords[:self._hero.actual_moove]
        possibles_cases = [[self.case_hero]]
        self.empty()
        self.path = []

        for i, list_coords in enumerate(good_coords_lists):
            possibles_cases.append([])

            for coords in list_coords:

                x, y = cst.get_abstract_coords(self._hero.coords)
                r_coords = (coords[0] + x, coords[1] + y)

                if r_coords not in case_group.keys():
                    continue
                elif case_group[r_coords].solid:
                    continue
                elif r_coords in [y.abstract_coords for y in self._others]:
                    continue

                possibles_cases[-1].append(
                    PathCase(self._image, r_coords, i + 1,
                             cases=possibles_cases[-2]))

                if not possibles_cases[-1][-1].path:
                    del possibles_cases[-1][-1]

                if possibles_cases[-1] is []:
                    break

        mouse_coords = cst.get_abstract_coords(self._mouse)
        for cases_list in possibles_cases:
            for case in cases_list:

                if mouse_coords == case.coords:
                    print("chemin possible !!!")
                    print("chemin:", case.path)
                    self.path = case.path

                    for case in self.path:
                        self.add(case)
                    return


class PathCase(pygame.sprite.Sprite):
    """Class."""

    def __init__(self, image, coords, distance, cases=None, is_hero=False):
        """Init."""
        pygame.sprite.Sprite.__init__(self)

        self.coords = coords
        self.distance = distance
        self.is_hero = is_hero

        self.path = []
        self.neighbour_coords = []

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
        if self.is_hero:
            self.path.append(self)
            return

        left = (self.x - 1, self.y)
        right = (self.x + 1, self.y)
        top = (self.x, self.y - 1)
        down = (self.x, self.y + 1)

        self.neighbour_coords = [left, right, top, down]

        for case in cases:
            for coords in self.neighbour_coords:
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
        return cst.get_true_coords(self.coords)
