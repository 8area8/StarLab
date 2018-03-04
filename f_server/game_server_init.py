"""Game init."""

import random

from f_server.connection import Connection


class GameServerInit:
    """Class who initialize the game."""

    def __init__(self, nb_players, _map, client_sockets, socket):
        """Initialize the class."""
        self.go_to = ''

        self.nb_players = nb_players
        self._map = _map

        self.connection = Connection(nb_players, client_sockets, socket)
        self.players = self.connection.players

        self._step = 1
        self.synchronisation = [False for x in range(len(nb_players))]

    def run_a_turn(self):
        """Run a turn in the main loop."""
        self.connection.re_initialize_server_messages()
        self.connection.receive()

        if self._step == 1:
            self._return_the_initialization_status()
            self._wait_for_players()

        elif self._step == 2:
            self._wait_for_synchronisation()

        elif self._step == 3:
            self._init_hereos_places()

        elif self._step == 4:
            self.go_to = 'game_server'

        self.connection.send()

    def _wait_for_players(self):
        """Wait and add new players."""
        if len(self.client_sockets) < self.nb_players:
            pass

    def _return_the_initialization_status(self):
        """Confirm the game initialization."""
        for player in self.players:
            if "is_game_init" not in player['msg']:
                continue

            player['to_send'] = ("game_init_yes "
                                 f"connected_clients:{len(self.players)} ")

    def _send_map_and_nb_players(self):
        """Return the map and the number of players."""
        for player in self.players:
            if "need_map" not in player['msg']:
                continue

            player["to_send"] = (f"map:{self._map} "
                                 f"nb_players:{len(self.players)}")

    def _send_players_informations(self):
        """Send players informations.

        Send:
            - the first active turn
            - the player's digital
            - the number of players
        """
        for player in self.players:
            if "players?" not in player["msg"]:
                continue

            turn = random.randint(1, len(self.players))
            player['to_send'] = ("players_ok "
                                 f"active_turn:{turn} "
                                 f"player_digit:{player['digit']} "
                                 f"nb_players:{self.nb_players}")

    def _wait_for_synchronisation(self):
        """Wait for all the players to continue."""
        for i, player in enumerate(self.players):
            if "synchro_ok" not in player["msg"]:
                continue

            self.synchronisation[i] = True

        if all(self.synchronisation):
            self._step = 3

    def _init_hereos_places(self):
        """Create a random spawn position for each hero.

        Add the result in global_message.
        """
        max_spawns = self._map.count(".")
        print(f"There are {max_spawns} spawners.")

        number_list = list(range(1, max_spawns))

        for player in self.players:

            number = self._get_unique_number(number_list)
            index = self._get_the_spawn_position(number)

            # Create a string treatable version
            str_spawn = ('0' for x in range(3) if index < 10**x) + str(index)

            self.connection.global_message += (f"player{player['digit']}"
                                               f"_place:{str_spawn} ")

    def _get_unique_number(self, number_list):
        """Get a number in number_list and remove it from the list."""
        n = random.choice(number_list)
        number_list.remove(n)
        print("n is equal to ", n)

        return n

    def _get_the_spawn_position(self, number):
        """Return the spawn position from its number."""
        index = 0
        index = (index + 1 for x in self._map.find('.', index) if x <= number)