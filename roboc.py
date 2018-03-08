"""Client source.

Initialize pygame, and start the main loop of the game.
"""

import pygame
from pygame.locals import QUIT

import f_roboc.images as r_images
import f_roboc.connection as f_connection

from f_roboc.introduction.introduction import Introduction
from f_roboc.main_menu.main_menu import MainMenu
from f_roboc.select_level.select_level import SelectLevel
from f_roboc.game.game import Game


def start_loop(images, main_screen, connection):
    """Start the main loop."""
    running = True
    interface = Introduction(images['introduction'], connection)
    clock = pygame.time.Clock()

    while running:
        mouse = pygame.mouse.get_pos()

        # Change the interface if needed.
        interface = _change_interface(interface, images, connection)

        # Events section.
        for event in pygame.event.get():  # Events call.
            if event.type == QUIT:
                running = False
            interface.start_events(event, mouse)  # Ours variable events call.

        # Update section.
        interface.update()

        # Communication to the server.
        interface.transfer_datas()

        # Drawing section.
        interface.draw()
        main_screen.blit(interface.sprt.main_surface, (0, 0))

        # Screen refreshness.
        pygame.display.flip()

        # Control the frames per second (want 30 fps).
        clock.tick(30)

    return


def _check_if_create_or_join_the_game(interface, connection):
    """Check if the player creates the game, or if he joins a game.

    if he creates the game (from SelectLevel), some parameters will be added.
    He can join a game (from MainMenu), if another client has created a game.
    """
    if isinstance(interface, MainMenu):
        interface = Game(
            images["game"],
            hote=interface.hote)

    elif isinstance(interface, SelectLevel):
        interface = Game(
            images["game"],
            client=None,
            map_contents=interface.evt.map_content,
            map_name=interface.evt.map_name,
            nb_players=interface.nb_players)

    else:
        raise TypeError("You cannot create or join a game "
                        "while being: {}\n".format(type(interface)),
                        "Only 'MainMenu' and 'SelectLevel' are valid types.")


def _change_interface(interface, images, connection):
    """Change the interface if needed (by the go_to variable)."""
    if not interface.go_to:
        return interface

    elif 'main_menu' in interface.go_to:
        if '-LostConnexion' in interface.go_to:
            interface = MainMenu(images['main_menu'], connection, error=True)
        else:
            interface = MainMenu(images["main_menu"], connection)

    elif interface.go_to == 'select_level':
        interface = SelectLevel(images["select_level"], connection)

    elif interface.go_to == 'game':
        _check_if_create_or_join_the_game(interface, connection)

    else:
        raise ValueError("'go_to' must be equal to 'main_menu', "
                         "'select_level' or 'game'.\n"
                         "'go_to' is: {}".format(interface.go_to))
    return interface


"""This condition avoids starting the game by doing the tests."""
if __name__ == '__main__':

    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    """Initialisation of all Pygame modules."""

    pygame.display.set_caption('StarLab')  # We choose a title.
    main_screen = pygame.display.set_mode((1280, 720))  # the main window.

    images = r_images.get_content_of('f_roboc/assets/images/')
    r_images.find_characters_and_create_their_moove_r_folder(images)
    """Load of all project images.

    We add a 'moove-r' folder for each character,
    based on their moove_l folder.
    """
    connection = f_connection.ServerConnection()

    start_loop(images, main_screen, connection)
