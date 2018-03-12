"""Game initiator."""

import pygame

import constants.find as fd
from f_roboc.interface import Interface
from f_roboc.game.sprites import GameInitSprites


class GameInitiator(Interface):
    """Initialize the game."""

    def __init__(self, imgs, connection, _map=None, nb_players=0, hote=False):
        """Initialize the class."""
        super().__init__()

        # CONNECTIONS VARIABLES
        self.connection = connection
        self.hote = hote
        self._orders = ""

        # PLAYERS INFORMATION
        self.active_turn = 0
        self.player_digit = 0
        self.nb_players = nb_players
        self.players = []

        # PROGRESS VARIABLE
        self.__step = 1

        # GAME'S MAP
        self._map = _map

        # SPRITES
        self.sprt = GameInitSprites(imgs)

        # FPS (USED TO SLOW THE SENDING)
        self.clock = pygame.time.Clock()

        self.name = 'game_init'

    @property
    def _step(self):
        """Unused 'get' property."""
        return self.__step

    @_step.setter
    def _step(self, value):
        """Just a print who advertise me when self.__step changes."""
        self.__step = value
        print("step is now ", self._step)

    def start_events(self, event, mouse):
        """Start the events."""
        pass

    @Interface._secured_connection
    def transfer_datas(self):
        """Data communication."""
        self.clock.tick(10)

        msg = self.connection.receive()

        if self._step == 1:
            self._get_or_send_map_and_nb_players(msg)

        elif self._step == 2:
            self._wait_for_all_players(msg)

        elif self._step == 3:
            self._define_players(msg)

        elif self._step == 4:
            self.go_to = 'game'

    def update(self):
        """Update the sprites."""
        self._refresh_timer()

    def draw(self):
        """Draw the sprites."""
        self.sprt.main_surface.blit(self.sprt.background, (0, 0))

    def _get_or_send_map_and_nb_players(self, msg):
        """Get or send the map and the number of players.

        if you are the hote, you will send these informations.
        Else, you will wait for these.
        """
        if self.hote:
            self._send_map_and_nb_players()
        else:
            self._wait_map_and_nb_players(msg)

    def _send_map_and_nb_players(self):
        """Send the map content and the number of players."""
        string_map = 'Q'.join("".join(line) for line in self._map)

        msg = f"create_game: nb_players:{self.nb_players} map:{string_map}"

        self.connection.send(msg)
        self._step = 2

    def _wait_map_and_nb_players(self, msg):
        """Wait for the map and the number of players."""
        if 'map:' not in msg:
            self.connection.send('need_map')

        else:
            # convert the map string into a valid map list.
            self._map = fd.find_text_after('map:', msg).split("Q")
            self._map = [list(line) for line in self._map]

            print('Game informations received.')
            print('map received:\n', self._map)
            self._step = 2

    def _wait_for_all_players(self, msg):
        """Wait for new game's connections.

        when the server has all its players, it send:
        - the player's number
        - the active turn
        - the number of players.
        """
        if "players_infos_ok:" in msg:
            self.player_digit = fd.find_number_after('player_digit:', msg)
            self.active_turn = fd.find_number_after("active_turn:", msg)
            self.nb_players = fd.find_number_after("nb_players:", msg)

            self.connection.send('synchro_ok')
            self._step = 3

        else:
            self.connection.send('players_informations?')

    def _define_players(self, msg):
        """Define the players lists if 'players_list in msg.

        We create one list per player, who contains his:
        - digit
        - name (and type)
        - membership
        - spawn
        """
        if 'players_list:' not in msg:
            return

        for i in range(self.nb_players):
            i += 1

            is_yours = True if self.player_digit == i else False
            name = 'superstar' if i == 1 else 'superalien'

            spawn = fd.find_and_get_coords_after(f"player{i}_place:", msg)
            print("dans g_i. spawn du joueur: ", spawn)

            self.players.append([i, name, is_yours, spawn])

        self._step = 4
