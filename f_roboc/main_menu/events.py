"""Module de gestion des évènements de la classe MainMenu."""

import sys

import pygame
from pygame.constants import MOUSEBUTTONDOWN


class EventsController:
    """Main lenu event's class."""

    def __init__(self, button_list, lost_connexion):
        """Initialisation."""
        self.go_to = ""
        self.button_list = button_list
        self.lost_connexion = lost_connexion

    def start(self, event, mouse):
        """On lance le testes d'évènements."""
        if event.type == MOUSEBUTTONDOWN and event.button == 1:

            if not self.lost_connexion.activated:
                for button in self.button_list:
                    if button.rect.collidepoint(mouse):
                        if button.name == "quitter":
                            pygame.display.quit()
                            pygame.quit()
                            sys.exit()
                        elif button.name == 'commencer':
                            self.go_to = 'select_level'
                        elif button.name == 'rejoindre':
                            self.go_to = 'game'

            else:
                if self.lost_connexion.button.rect.collidepoint(mouse):
                    self.lost_connexion.activated = False
