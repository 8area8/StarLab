"""Game server module."""

import pygame

from f_server import time as time
from f_server.connection import Connection
from f_server.heroes_actions import Transform
from f_server.heroes_actions import Moove

import constants.find as csfind


class GameServer:
    """Main class."""

    def __init__(self, connection, map_content, client_sockets):
        """Init."""
        self.map_string = map_content.replace("Q", "")

        self._clock = pygame.time.Clock()
        self.connection = connection

        self.empty_orders = list("" * self.connection.nb_players)
        self.orders = self.empty_orders[:]

        self._wait_for_synchronisation()

        self._timer = time.TimeController()
        self.transform = Transform()
        self.moove = Moove()

        self.index_turns = 0
        self.in_action = False

        self.loop()

    @property
    def active_player(self):
        """Return current player turn."""
        return self.clt.players[self.index_turns]

    def _wait_for_synchronisation(self):
        """wait."""
        synchronised_players = [False for x in range(len(self.clt.players))]
        while True:
            self.orders = self.empty_orders[:]
            for player in self.clt.players:
                player["msg"] = ""

            self.clt.receive()
            g_i.test_server_status(self.clt.players, self.orders)
            g_i.test_game_info(self.clt.players, self.orders, self.map_content)
            g_i.test_start_game(self.clt.players, self.orders)
            g_i.test_synchro(synchronised_players, self.clt.players)
            self.clt.send(self.orders)

            if False in synchronised_players:
                continue
            break

        self.orders = self.empty_orders[:]
        g_i.init_heroes(self.clt.players, self.orders, self.map_string)
        self.clt.send(self.orders)

    def get_next_time(self):
        """Retourne nouveau temps."""
        msg = ""
        temp_time = self._timer.update(self.active_player["msg"],
                                       self.in_action)

        if "new_second" in temp_time:
            msg = "time:{} ".format(self._timer.current_seconds)

        if "next_turn" in temp_time:
            self.index_turns = (self.index_turns + 1) % len(self.clt.players)
            msg = "next_turn:{} time:0 ".format(self.active_player["number"])

        if not msg:
            return

        for i, message in enumerate(self.orders):
            self.orders[i] += msg

    def run_a_turn(self):
        """Loop principal."""
        self.orders = self.empty_orders[:]
        for player in self.clt.players:
            player["msg"] = ""

        self._events()

        self._update()
        self._clock.tick(30)

    def _events(self):
        """Events."""
        self.clt.receive()

        if self.in_action:
            return

        msg = self.active_player["msg"]

        if "transform:" in msg:

            self.in_action = True
            str_coords = csfind.find_str_coords_after('transform:', msg)

            self.transform.activation(str_coords, self.orders)

        if "moove" in msg:

            self.in_action = True
            directions = csfind.find_text_after('directions:', msg)
            hero_coords = csfind.find_and_get_coords_after('hero_coords:', msg)

            print(hero_coords)
            self.moove.init_moove(hero_coords, directions)

    def _update(self):
        """Updat."""
        if self.in_action:
            self.transform.update(self.orders)
            self.moove.update(self.orders)

        self.get_next_time()

        self.clt.send(self.orders)

        if "end" in self.orders[0]:
            self.in_action = False
