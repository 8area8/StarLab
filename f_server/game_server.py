"""Game server module."""

from f_server.time import TimeController
from f_server.heroes_actions import Transform, Moove, Teleportation

import constants.find as csfind
import constants.coordinates as csc


class GameServer:
    """This classe manages the server in game."""

    def __init__(self, connection, _map, turn):
        """Initialization of the class."""
        self.go_to = ''

        # CONNECTIONS
        self.connection = connection
        self.players = self.connection.players

        # EVENTS
        self._timer = TimeController()
        self.transform = Transform()
        self.moove = Moove()
        self.teleport = Teleportation()

        # GAME INFORMATIONS
        self._map = _map
        self.index_turns = turn - 1
        self.in_event = False
        self.victory = False

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
            msg = f"next_turn:{self.active_player['digit']} time:0 "

        if not msg:
            return

        self.connection.global_message += msg

    def run_a_turn(self):
        """Run a turn in the server's loop."""
        self.connection.re_initialize_server_messages()
        self.connection.receive()

        self._events()
        self._update()

        self.connection.send()
        self.connection.re_initialize_players_messages()

        if self.victory:
            self.go_to = 'default'

    def _events(self):
        """Get the active player's message and call the desired event.

        Call event only if there is no current events.
        """
        if self.in_event:
            return

        msg = self.active_player["msg"]

        if "transform:" in msg:

            self.in_event = True
            coords = csfind.find_and_get_coords_after('transform:', msg)

            self.connection.global_message = self.transform.activate(coords)

        if "moove" in msg:

            self.in_event = True
            directions = csfind.find_text_after('directions:', msg)
            hero_coords = csfind.find_and_get_coords_after('hero_coords:', msg)

            tp = None
            if 'teleporter:' in msg:
                tp = csfind.find_and_get_coords_after('teleporter:', msg)
            victory = True if "victory" in msg else False

            print(hero_coords)
            self.moove.init_moove(hero_coords, directions, tp, victory)

    def _update(self):
        """The event updates."""
        co = self.connection

        if self.in_event:
            self.connection.global_message += self.transform.update()
            self.connection.global_message += self.moove.update()
            self.connection.global_message += self.teleport.update()

        self._active_teleportation(co.global_message)
        self.get_next_time()

        self.victory = True if 'victory!' in co.global_message else False

        if "end" in co.global_message:
            if 'teleportation' not in co.global_message:
                self.in_event = False

    def _active_teleportation(self, msg):
        """Activate the teleportation."""
        if 'teleportation' in msg:
            coords = csfind.find_and_get_coords_after('teleportation:', msg)

            if self.active_player['digit'] == 1:
                name = 'superstar'
            else:
                name = 'superalien'

            self.teleport.activate(coords, name)
