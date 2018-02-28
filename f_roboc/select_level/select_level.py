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

        self.connection = connection
        self.sprt = SpritesController(imgs)
        self.evt = EventsController(
            self.sprt.button_list,
            self.sprt.not_implemented,
            self.sprt.text_button_list)

        self.nb_players = 2

    def start_events(self, event, mouse):
        """Call events class."""
        self.evt.start(event, mouse)

    @Interface._secured_connection
    def transfer_datas(self):
        """Connect to the server and try to know if a game is running."""
        if not self._is_timer_over(1000):
            return

        if not self.connection.connected:
            self.connection.connect()

        elif not self._game_init:
            self._ask_if_game_init_is_running()

    def update(self):
        """Sprites update."""
        self.go_to = self.evt.go_to

        self.sprt.button_list.update()
        self.sprt.text_button_list.update()
        self.sprt.ponct_sprites.update()

    def draw(self):
        """Sprites drawing."""
        self.sprt.main_surface.blit(self.sprt.background["bg"], (0, 0))

        self.sprt.text_button_list.draw(self.sprt.text_list_surface)
        self.sprt.main_surface.blit(
            self.sprt.text_list_surface, (
                259 * csizes.UPSCALE, 160 * csizes.UPSCALE))

        self.sprt.button_list.draw(self.sprt.main_surface)
        self.sprt.ponct_sprites.draw(self.sprt.main_surface)
