"""Classe HUB de la partie main_menu."""

from f_roboc.main_menu.sprites import SpritesController as SpritesController
from f_roboc.main_menu.events import EventsController as EventsController


class MainMenu:
    """Classe principale."""

    def __init__(self, imgs):
        """Init."""
        self.to_select_level = False
        self.to_game = False
        self.to_main_menu = False

        self.sprt = SpritesController(imgs)
        self.evt = EventsController(self.sprt.button_list)

    def events(self, event, mouse):
        """Appel des évènements."""
        if self.evt.go_to_select:
            self.to_select_level = True
        self.evt.start(event, mouse)

    def update(self):
        """Mise à jour des éléments."""
        self.sprt.background.update()
        self.sprt.button_list.update()

    def draw(self):
        """Dessin des éléments."""
        self.sprt.main_surface.blit(self.sprt.background.image, (0, 0))
        self.sprt.button_list.draw(self.sprt.main_surface)
