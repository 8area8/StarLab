"""Module HUB de la partie game."""

import pygame

from constants import game_sizes as cst

from f_roboc.game.time import TimeController as TimeController
from f_roboc.game.event import EventsController

import f_roboc.game.game_initiator as g_i


class Game:
    """La classe de jeu côté client."""

    def __init__(self, imgs, client, map_contents=None, map_name=None,
                 nb_players=None, hote=True):
        """Initialisation."""
        self.to_select_level = False
        self.to_game = False
        self.to_main_menu = False

        self._map_contents = map_contents
        self.nb_players = nb_players
        self.hote = hote

        self._clt = client

        self._orders = ""
        self._server_msg = ""
        # on envoit les coordonnées du jeu.
        if self.hote:
            self._orders = g_i.return_game_infos(nb_players, map_contents)
            self._clt.send(self._orders)
        else:
            self._map_contents = g_i.wait_game_infos(self._clt)

        self._have_players_infos = False
        self._start_game = False

        self.player_number = None
        self.players = []

        self.player_turn = None
        self.in_action = False

        self.sprt = None
        self.sprt.create_map(self._map_contents)
        self.time = TimeController()
        self.evt = EventsController(self)

    @property
    def active_player(self):
        """Active."""
        for hero in self.sprt.heroes_grp:
            if hero.number == self.player_turn:
                return hero
        raise ValueError("le tour ne correspond à aucun héros!")

    @property
    def active_turn(self):
        """Active."""
        if self.player_number == self.player_turn:
            return True
        else:
            return False

    def events(self, event, mouse):
        """On appel les évènements."""
        if not self._start_game:
            return

        self._orders = ""

        self.evt.start(event, mouse)

        """Envoit des ordres."""
        self._clt.send(self._orders)

    def init_update(self):
        """Update for the game initiation."""
        self._orders = ""

        if not self._have_players_infos:

            temp = self.time.update()
            if not temp:
                return

            msg = self._clt.receive()

            self._orders += "players?"
            self.player_turn, self.player_number, self.nb_players =\
                g_i.wait_new_players(msg)

            if "players_ok" in msg:
                self._orders = "synchro_ok"
                self._have_players_infos = True

            self._clt.send(self._orders)
            return

        msg = self._clt.receive()

        if "player's list" in msg:
            g_i.define_players(msg, self.player_number, self.players)
            self.sprt.init_heroes(self.players)
            self.sprt.init_pathfinder()
            self.sprt.init_transform_paths()

        if "start_game" in msg:
            self._start_game = True

    def update(self):
        """On receptionne les données du serveur.

        pour chaque surface, on attribut les données du serveur.
        """
        if not self._start_game:
            self.init_update()
            return

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

        self._server_msg = self._clt.receive()

        if self.active_turn:
            self.sprt.menu = self.sprt.menu_blue
        else:
            self.sprt.menu = self.sprt.menu_grey

        if "time:" in self._server_msg:
            i = self._server_msg.find("time:") + 5
            self.sprt.time.choose_index(
                int(self._server_msg[i]), self.active_turn)

        if "next_turn" in self._server_msg:
            i = self._server_msg.find("next_turn:")
            i += 10
            self.player_turn = int(self._server_msg[i])
            self.sprt.next_turn.start_anim()
            self.active_player.activate_skills()

        if "transform:" in self._server_msg:
            if "transform:activated" in self._server_msg:
                self.in_action = True
                self.active_player.define_key_imgs("transform")
                index = self._server_msg.find("coords:") + 7
                str_coords = self._server_msg[index:index + 7]
                coords = cst.get_tuple_coords(str_coords)
                coords = cst.get_true_coords(coords)
                self.sprt.transform_anim.define_coords(coords)
            elif "index" in self._server_msg:
                index = self._server_msg.find("index") + 5
                index = int(self._server_msg[index])
                self.sprt.transform_anim.play_animation(index=index)
            if "transfNow:" in self._server_msg:
                index = self._server_msg.find("transfNow:") + 10
                str_coords = self._server_msg[index:index + 7]
                coords = cst.get_tuple_coords(str_coords)
                self.sprt.cases_group[coords].transform()
            if "end" in self._server_msg:
                self.in_action = False
                self.sprt.transform_anim.play_animation(end=True)
                self.active_player.define_key_imgs("breath")

        if "moove" in self._server_msg:
            if "end" in self._server_msg:
                self.in_action = False
                self.active_player.define_key_imgs("breath")
            else:
                self.in_action = True
                index = self._server_msg.find("moove:") + 6
                str_coords = self._server_msg[index:index + 9]
                coords = cst.get_tuple_coords(str_coords, base=1000)
                self.active_player.moove(coords)

        self.sprt.cases_group.update()
        self.sprt.menu_layer_2.update(self.active_turn)
        self.sprt.heroes_grp.update()

    def draw(self):
        """On dessine tous les éléments."""
        if not self._start_game:
            self.sprt.main_surface.blit(self.sprt.wait_players, (0, 0))
            return

        self.sprt.cases_group.draw(self.sprt.map_surface)
        self.sprt.heroes_grp.draw(self.sprt.map_surface)
        self.sprt.pathfinder.draw(self.active_turn, self.sprt.map_surface)
        self.sprt.transform_paths.draw(self.active_turn, self.sprt.map_surface)
        self.sprt.main_surface.blit(self.sprt.map_surface, (0, 0))

        self.sprt.main_surface.blit(self.sprt.menu, (0, 0))
        self.sprt.menu_layer_1.draw(self.sprt.main_surface)
        self.sprt.menu_layer_2.draw(self.sprt.main_surface)
