"""This module contains the select level HUB interface."""

import constants.game_sizes as csizes

from f_roboc.interface import Interface
from f_roboc.select_level.sprites import SpritesController as SpritesController
from f_roboc.select_level.events import EventsController as EventsController


class SelectLevel(Interface):
    """This class rules the level selection."""

    def __init__(self, imgs, connection):
        """Initialize the class."""
        super().__init__()

        # MAIN MODULES
        self.connection = connection
        self.sprt = SpritesController(imgs)
        self.evt = EventsController(
            self.sprt.button_list,
            self.sprt.not_implemented,
            self.sprt.text_button_list)

        # BOOLEAN SERVER STATUS
        self._launched_game = False
        self._first_answer = False

        # MAP AND PLAYER NUMBERS
        self.nb_players = 2
        self._map = []

        # NAME
        self.name = 'select_level'

    def start_events(self, event, mouse):
        """Call events class."""
        self.evt.start(event, mouse, self.connection.connected,
                       self._launched_game, self._map)

    @Interface._secured_connection
    def transfer_datas(self):
        """Connect to the server and try to know if a game is running."""
        if not self._is_timer_over(100):
            return

        if not self.connection.connected:
            print('try to connect')
            self.connection.connect()
        else:
            self._ask_if_game_is_running()
            self._first_answer = True

    def _ask_if_game_is_running(self):
        """Ask to the server if a game is in initialization.

        If it is, _launched_game will be True.
        """
        msg = self.connection.receive()
        if 'game_init_yes' in msg or 'game_running_yes' in msg:
            self._launched_game = True
            return

        self.connection.send('is_game_init is_game_running')

    def update(self):
        """Sprites update."""
        self._refresh_timer()

        self.go_to = self.evt.go_to

        self.sprt.button_list.update()

        if self.connection.connected and not self._launched_game:
            self.sprt.text_button_list.update()

        self._update_interface_status()
        self.sprt.ponct_sprites.update()

    def _update_interface_status(self):
        """Update the actual status of SelectLevel."""
        launched_sprt = self.sprt.launched_game
        connect_sprt = self.sprt.no_connection

        connect_sprt.activated = False if self.connection.connected else True
        launched_sprt.activated = True if self._launched_game else False

    def draw(self):
        """Sprites drawing."""
        main_s = self.sprt.main_surface
        main_s.blit(self.sprt.background, (0, 0))

        self._draw_interface_status(main_s)
        self.sprt.button_list.draw(self.sprt.main_surface)
        self.sprt.ponct_sprites.draw(self.sprt.main_surface)

    def _draw_interface_status(self, main_s):
        """Draw map buttons or an error status."""
        launched_sprt = self.sprt.launched_game
        no_connect_sprt = self.sprt.no_connection

        if self.connection.connected and self._launched_game:
            main_s.blit(launched_sprt.image, launched_sprt.coords)

        elif self.connection.connected and self._first_answer:
            self._draw_map_buttons()

        else:
            main_s.blit(no_connect_sprt.image, no_connect_sprt.coords)

    def _draw_map_buttons(self):
        """Draw the map buttons."""
        self.sprt.text_button_list.draw(self.sprt.text_list_surface)
        self.sprt.main_surface.blit(
            self.sprt.text_list_surface, (
                259 * csizes.UPSCALE, 160 * csizes.UPSCALE))
