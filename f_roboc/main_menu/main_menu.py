"""Interface of the main menu."""

from f_roboc.interface import Interface

from f_roboc.main_menu.sprites import SpritesController
from f_roboc.main_menu.events import EventsController


class MainMenu(Interface):
    """Main menu's main class."""

    def __init__(self, images, connection):
        """Init."""
        super().__init__()

        self.name = 'main_menu'

        self.connection = connection
        self.sprt = SpritesController(images)
        self.events = EventsController(self.sprt.button_list)

    def start_events(self, event, mouse):
        """Call of events."""
        self.events.start(event, mouse)

    @Interface._secured_connection
    def transfer_datas(self):
        """Connect to the server and try to know if a game is running."""
        if not self._is_timer_over(1000):
            return

        if not self.connection.connected:
            self.connection.connect()

    def update(self):
        """Sprite update."""
        self._refresh_timer()

        self.to_go = self.events.go_to

        self.sprt.background.update()
        self.sprt.button_list.update()

    def draw(self):
        """Sprite drawing."""
        self.sprt.main_surface.blit(self.sprt.background.image, (0, 0))
        self.sprt.button_list.draw(self.sprt.main_surface)
