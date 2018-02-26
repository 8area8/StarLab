"""Module de gestion des évènements de la classe MainMenu."""

import sys

import pygame
from pygame.constants import MOUSEBUTTONDOWN


class EventsController:
    """Main class."""

    def __init__(self, button_list):
        """Initialisation."""
        self.go_to_select = False
        self.button_list = button_list

    def start(self, event, mouse):
        """On lance le testes d'évènements."""
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            for button in self.button_list:
                if button.rect.collidepoint(mouse):
                    if button.name == "quitter":
                        pygame.display.quit()
                        pygame.quit()
                        sys.exit()
                    elif button.name == 'commencer':
                        self.go_to_select = True
