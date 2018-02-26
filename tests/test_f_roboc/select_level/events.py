"""Events de la partie select_level."""


from pygame.constants import MOUSEBUTTONDOWN


class EventsController:
    """Class."""

    def __init__(self, button_list, not_imlplemented, map_buttons):
        """Initialisation."""
        self.go_to_game = False
        self.back_to_main = False
        self.map_content = None
        self.map_name = None

        self.button_list = button_list
        self.not_imlplemented = not_imlplemented
        self.map_buttons = map_buttons

    def start(self, event, mouse):
        """On lance les testes d'évènements."""
        if event.type == MOUSEBUTTONDOWN and event.button == 1:

            for button in self.button_list:
                if button.rect.collidepoint(mouse):
                    if button.name == 'return':
                        self.back_to_main = True
                    elif button.name == 'left_arrow':
                        button.in_animation = True
                        self.not_imlplemented.activated = True
                    elif button.name == 'right_arrow':
                        button.in_animation = True
                        self.not_imlplemented.activated = True

            for button in self.map_buttons:
                pos = mouse
                pos = pos[0] - 259 * 2, pos[1] - 160 * 2
                if button.rect.collidepoint(pos):
                    self.go_to_game = True
                    self.map_content = button.contents
                    self.map_name = button.text
