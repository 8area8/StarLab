"""Module HUB of the game part."""

import pygame

import constants.coordinates as csc
import constants.find as csfind

from f_roboc.game.time import TimeController as TimeController
from f_roboc.game.event import EventsController


class Game:
    """The game client class.

    Manages the game part.
    """

    def __init__(self, imgs, connection, players, _map):
        """Initialization of the class."""

        # GAME'S MAP
        self._map = _map

        # CONNECTION INFORMATIONS
        self.connection = connection
        self.msg = ""

        # GAME INFORMATIONS
        self.player_turn = None
        self.in_action = False

        # SPRITES INITIALIZATION.
        self.sprt = None
        self.sprt.create_map(self._map)
        self.sprt.init_heroes(players)
        self.sprt.init_pathfinder()
        self.sprt.init_transform_paths()

        # EVENT OBJECTS
        self.time = TimeController()
        self.evt = EventsController(self)

    @property
    def active_player(self):
        """Return the active player."""
        for hero in self.sprt.heroes_grp:
            if hero.number == self.player_turn:
                return hero
        raise ValueError("The turn's number doesn't correspond to any hero!")

    @property
    def active_turn(self):
        """Return the active turn."""
        if self.player_number == self.player_turn:
            return True
        else:
            return False

    def events(self, event, mouse):
        """Events call."""
        actions = self.evt.start(event, mouse)

        # We now send the actions.
        self._clt.send(actions)

    def update(self):
        """Recept and process the datas."""
        msg = self._clt.receive()

        self.show_possibles_cases()

        if self.active_turn:
            self.sprt.menu = self.sprt.menu_blue
        else:
            self.sprt.menu = self.sprt.menu_grey

        if "time:" in msg:
            i = self._server_msg.find("time:") + 5
            self.sprt.time.choose_index(
                int(self._server_msg[i]), self.active_turn)

        if "next_turn" in msg:
            i = self._server_msg.find("next_turn:")
            i += 10
            self.player_turn = int(self._server_msg[i])
            self.sprt.next_turn.start_anim()
            self.active_player.activate_skills()

        # TRANSFORM
        if "transform:" in msg:
            if "transform: activated" in msg:
                self.in_action = True
                self.active_player.define_key_imgs("transform")
                coords = csfind.find_and_get_coords_after("coords:", msg)
                self.sprt.transform_anim.define_coords(coords)

            elif "index:" in msg:
                index = csfind.find_number_after("index:", msg)
                self.sprt.transform_anim.play_animation(index=index)

            if "transfNow:" in self._server_msg:
                coords = csfind.find_and_get_coords_after('transfNow:', msg)
                self.sprt.cases_group[coords].transform()

            if "end" in self._server_msg:
                self.in_action = False
                self.sprt.transform_anim.play_animation(end=True)
                self.active_player.define_key_imgs("breath")

        # MOOVE
        if "moove" in msg:
            if "end" in msg:
                self.in_action = False
                self.active_player.define_key_imgs("breath")
            else:
                self.in_action = True
                coords = csfind.find_and_get_coords_after("moove:", msg)
                self.active_player.moove(coords)

        self.sprt.cases_group.update()
        self.sprt.menu_layer_2.update(self.active_turn)
        self.sprt.heroes_grp.update()

    def show_moove_or_transform(self):
        """Show the moove cases or transform cases."""
        if self.active_turn and not self.in_action:
            if self.evt.transform_vision:
                self.sprt.transform_paths.show_possibles_cases(
                    self.sprt.cases_group)
            else:
                self.sprt.transform_paths.empty()
                self.sprt.pathfinder.active_the_pathfinding(
                    pygame.mouse.get_pos(), self.sprt.cases_group)
        else:
            self.sprt.pathfinder.empty()
            self.sprt.transform_paths.empty()

    def draw(self):
        """Sprites drawing."""
        self.sprt.cases_group.draw(self.sprt.map_surface)
        self.sprt.heroes_grp.draw(self.sprt.map_surface)
        self.sprt.pathfinder.draw(self.active_turn, self.sprt.map_surface)
        self.sprt.transform_paths.draw(self.active_turn, self.sprt.map_surface)
        self.sprt.main_surface.blit(self.sprt.map_surface, (0, 0))

        self.sprt.main_surface.blit(self.sprt.menu, (0, 0))
        self.sprt.menu_layer_1.draw(self.sprt.main_surface)
        self.sprt.menu_layer_2.draw(self.sprt.main_surface)
