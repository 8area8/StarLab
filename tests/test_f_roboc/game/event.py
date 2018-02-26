"""Class event."""

from f_roboc import constants as cst

from pygame.locals import MOUSEBUTTONDOWN


class EventsController:
    """Main class."""

    def __init__(self, game):
        """Init."""
        self.game = game
        self.mlr2 = self.game.sprt.menu_layer_2

        self.transform_vision = False

    def start(self, event, mouse):
        """Event."""
        hero = self.game.active_player
        pathfinder = self.game.sprt.pathfinder
        c_grp = self.game.sprt.cases_group

        if self.game.active_turn and not self.game.in_action:

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                self.transform_vision = False

                for button in self.mlr2:
                    if button.rect.collidepoint(mouse):
                        if button.name == 'bull':
                            self.game._orders += "next_turn"
                            button.on_clic = True
                        if button.name == 'transform' and hero.transform_spell:
                            button.on_clic = True
                            if not self.transform_vision:
                                self.transform_vision = True

                if hero.transform_spell and self.game.sprt.transform_paths:
                    for case in self.game.sprt.transform_paths:
                        if case.rect.collidepoint(mouse):
                            hero.transform_spell = False
                            self.game.sprt.transform.desactivated = True
                            str_coords = cst.get_string_coords(case.coords)
                            len_imgs = len(hero.time_imgs["transform"])
                            len_imgs = str(len_imgs)
                            self.game._orders += "transform:" + str_coords
                            self.game.in_action = True
                            return

                if hero.has_moove and self.game.sprt.pathfinder:
                    for case in self.game.sprt.pathfinder:
                        if case.rect.collidepoint(mouse):
                            hero.actual_moove -= case.distance
                            coords_path = [case.coords for case in pathfinder]
                            str_moove = "moove:"
                            c = cst.get_string_coords(hero.coords, base=1000)
                            str_moove += "hero_coords:" + c
                            temp = len(coords_path) - 1
                            str_moove += "len:{},directions:".format(temp)

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
                                    raise ValueError(
                                        "la case cible est la même que la"
                                        "case base.")

                            last_c = coords_path[-1]
                            if c_grp[last_c].nature == "teleporter":
                                c_grp.find_another_teleporter(last_c)
                                str_moove += " teleporter "

                            self.game._orders += str_moove
                            # self.game.in_action = True
                            return

        else:
            pass
