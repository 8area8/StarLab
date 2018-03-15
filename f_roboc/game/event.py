"""Event module."""

from pygame.locals import MOUSEBUTTONDOWN

from constants import coordinates as csc


class EventsController:
    """The game events class."""

    def __init__(self, game):
        """Initialization."""
        self.game = game
        self.mlr2 = self.game.sprt.menu_layer_2

        self.transform_vision = False

    def start(self, event, mouse):
        """Start the events."""
        hero = self.game.active_player
        pathfinder = self.game.sprt.pathfinder
        c_grp = self.game.sprt.cases_group

        if self.game.victory:
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                button = self.game.sprt.victory.button
                if button.rect.collidepoint(mouse):
                    self.game.go_to = 'main_menu'
            return

        if not self.game.active_turn or self.game.in_action:
            return

        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            self.transform_vision = False

            for button in self.mlr2:
                if button.rect.collidepoint(mouse):
                    if button.name == 'bull':
                        self.game.msg += "next_turn"
                        button.activated = True
                    if button.name == 'transform' and hero.transform_spell:
                        button.activated = True
                        if not self.transform_vision:
                            self.transform_vision = True

            if hero.transform_spell and self.game.sprt.transform_paths:

                for case in self.game.sprt.transform_paths:
                    if case.rect.collidepoint(mouse):
                        hero.transform_spell = False
                        self.game.sprt.transform.desactivated = True
                        coords = csc.transform_coords_to('string', case.coords)
                        self.game.msg += "transform:" + coords
                        self.game.in_action = True
                        return

            if hero.has_moove and pathfinder:

                for case in pathfinder:
                    if case.rect.collidepoint(mouse):
                        hero.actual_moove -= case.distance
                        coords_path = [case.coords for case in pathfinder]
                        str_moove = "moove:"
                        c = csc.transform_coords_to('string', hero.coords)
                        str_moove += "hero_coords:" + c
                        len_coords = len(coords_path) - 1
                        str_moove += f"len:{len_coords},directions:"

                        for i, coords in enumerate(coords_path):
                            if i == len(coords_path) - 1:
                                break

                            x = coords[0]
                            y = coords[1]
                            a = coords_path[i + 1][0]
                            b = coords_path[i + 1][1]
                            if x < a:
                                str_moove += "r"
                            elif x > a:
                                str_moove += "l"
                            elif y < b:
                                str_moove += "d"
                            elif y > b:
                                str_moove += "t"
                            else:
                                raise ValueError("Target case == current.")

                        last_c = coords_path[-1]
                        coords = csc.transform_coords_to('real', last_c)

                        if c_grp[last_c].nature == "teleporter":
                            coords = c_grp.find_another_teleporter(coords)
                            coords = csc.transform_coords_to('string', coords)
                            str_moove += f" teleporter:{coords} "

                        elif c_grp[last_c].nature == "victory":
                            str_moove += " victory "

                        self.game.msg += str_moove
                        return

        else:
            pass
