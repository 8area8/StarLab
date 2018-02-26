"""Classe HUB de la partie Select_level."""

import f_roboc.constants as cst

from f_roboc.select_level.sprites import SpritesController as SpritesController
from f_roboc.select_level.events import EventsController as EventsController


class SelectLevel:
    """Classe qui gère la selection de niveaux."""

    def __init__(self, imgs):
        """Initialisation."""
        self.to_select_level = False
        self.to_game = False
        self.to_main_menu = False

        self.sprt = SpritesController(imgs)
        self.evt = EventsController(
            self.sprt.button_list,
            self.sprt.not_implemented,
            self.sprt.text_button_list)

        self.nb_players = 2

    def events(self, event, mouse):
        """Appel les évènements propres à la classe."""
        if self.evt.back_to_main:
            self.to_main_menu = True
        elif self.evt.go_to_game:
            self.to_game = True
        self.evt.start(event, mouse)

    def update(self):
        """Mise à jour."""
        self.sprt.button_list.update()
        self.sprt.text_button_list.update()
        self.sprt.ponct_sprites.update()

    def draw(self):
        """Dessin des éléments de SelectLevel."""
        self.sprt.main_surface.blit(self.sprt.background["bg"], (0, 0))

        self.sprt.text_button_list.draw(self.sprt.text_list_surface)
        self.sprt.main_surface.blit(
            self.sprt.text_list_surface, (
                259 * cst.UPSCALE, 160 * cst.UPSCALE))

        self.sprt.button_list.draw(self.sprt.main_surface)
        self.sprt.ponct_sprites.draw(self.sprt.main_surface)
