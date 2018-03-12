"""Game server module."""

import pygame

from f_server.time import TimeController
from f_server.heroes_actions import Transform, Moove

import constants.find as csfind


class GameServer:
    """This classe manages the server in game."""

    def __init__(self, connection, _map):
        """Initialization of the class."""
        self.go_to = ''

        # CONNECTIONS
        self.connection = connection
        self.players = self.connection.players

        # EVENTS
        self._timer = TimeController()
        self.transform = Transform()
        self.moove = Moove()

        # GAME INFORMATIONS
        self._map = _map
        self.index_turns = 0
        self.in_event = False

    @property
    def map_string(self):
        """Return a readable map string."""
        return self._map.replace('Q', '')

    @property
    def active_player(self):
        """Return the current player's turn."""
        return self.players[self.index_turns]

    def get_next_time(self):
        """Return the turn's time."""
        result = self._timer.update(self.active_player["msg"], self.in_event)
        msg = ""

        if "new_second" in result:
            msg = "time:{} ".format(self._timer.current_seconds)

        if "next_turn" in result:
            self.index_turns = (self.index_turns + 1) % len(self.players)
            msg = "next_turn:{} time:0 ".format(self.active_player["digit"])

        if not msg:
            return

        for player in self.players:
            player['to_send'] += msg

    def run_a_turn(self):
        """Run a turn in the server's loop."""
        self.connection.re_initialize_server_messages()
        self.connection.receive()

        self._events()
        self._update()

        self.connection.send()
        self.connection.re_initialize_players_messages()

    def _events(self):
        """Get the active player's message and call the desired event.

        Call event only if there is no current events.
        """
        if self.in_event:
            return

        msg = self.active_player["msg"]

        if "transform:" in msg:

            self.in_event = True
            s_coords = csfind.find_str_coords_after('transform:', msg)

            self.connection.global_message = self.transform.activate(s_coords)

        if "moove" in msg:

            self.in_event = True
            directions = csfind.find_text_after('directions:', msg)
            hero_coords = csfind.find_and_get_coords_after('hero_coords:', msg)

            print(hero_coords)
            self.moove.init_moove(hero_coords, directions)

    def _update(self):
        """The event updates."""
        if self.in_event:
            self.connection.global_message += self.transform.update()
            self.connection.global_message += self.moove.update()

        self.get_next_time()

        if "end" in self.connection.global_message:
            self.in_event = False
