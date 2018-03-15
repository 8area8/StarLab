"""Class who runs the presentation."""

from f_roboc.interface import Interface
from f_roboc.introduction.sprites import SpritesController
import f_roboc.introduction.movie as movie


class Introduction(Interface):
    """Introduct the game project with a presentation screen and a movie."""

    def __init__(self, images, connection):
        """Init."""
        super().__init__()

        self.name = 'introduction'

        self.connection = connection
        self.sprt = SpritesController(images)
        self.events = None

        self._play_movie = True

    def start_events(self, event, mouse):
        """Not used."""
        pass

    def transfer_datas(self):
        """Not used."""
        pass

    def update(self):
        """Update."""
        self._refresh_timer()
        if self._is_timer_over(700) and self._play_movie:
            self._play_movie = False
            movie.play_video()
            self.go_to = 'main_menu'

    def draw(self):
        """Draw."""
        self.sprt.main_surface.fill((0, 0, 0))

        if self._current_time < 700:
            self.sprt.main_surface.blit(self.sprt.presentation, (0, 0))
