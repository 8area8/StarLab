"""Events de la partie select_level."""


from pygame.constants import MOUSEBUTTONDOWN


class EventsController:
    """Class."""

    def __init__(self, button_list, not_implemented, map_buttons):
        """Initialisation."""
        self.go_to = ""

        self.button_list = button_list
        self.not_implemented = not_implemented
        self.map_buttons = map_buttons

    def start(self, event, mouse, connected, game_launched, _map):
        """On lance les testes d'évènements."""
        if event.type == MOUSEBUTTONDOWN and event.button == 1:

            for button in self.button_list:
                if button.rect.collidepoint(mouse):
                    if button.name == 'return':
                        self.go_to = 'main_menu'
                    elif button.name == 'left_arrow':
                        button.activated = True
                        self.not_implemented.activated = True
                    elif button.name == 'right_arrow':
                        button.activated = True
                        self.not_implemented.activated = True

            if not connected or game_launched:
                return

            for button in self.map_buttons:
                pos = mouse
                pos = pos[0] - 259 * 2, pos[1] - 160 * 2
                if button.rect.collidepoint(pos):
                    self.go_to = 'game_init'
                    _map.append(button.contents)
