"""Class who rules the presentation."""

import pygame
import sys

from f_roboc.introduction.sprites import SpritesController
import f_roboc.movie.movie as mv


class Introduction:
    """Main class."""

    def __init__(self, imgs, client, connection):
        """Init."""
        self.to_select_level = False
        self.to_game = False
        self.to_main_menu = False

        self.hote = True

        self.sprt = SpritesController(imgs)
        self.clt = client
        self.connection = connection
        self.movie = False

        self.orders = ""
        self.status = ""

        self.max_time = 1500
        self.current_time = 0.0

    def events(self, event, mouse):
        """Update."""
        pass

    def update(self):
        """Update."""
        self.sprt.hors_line.update()
        self.sprt.presentation.update()

        if self.movie:
            self.current_time += 33.4
            if self.current_time >= 2000:
                    mv.Movie()
                    self.to_main_menu = True

        if self.connection and not self.status:

            self.orders = "connected_clients in_game"
            self.clt.send(self.orders)
            msg = self.clt.receive()

            if "in_game" in msg:
                if "True" in msg:
                    self.status = "guest"
                    print("status: guest.")
                else:
                    self.status = "hote"
                    print("status: hote.")
                    self.sprt.presentation.activated = True

                    if "connected_clients" in msg:
                        if "connected_clients:1" not in msg:
                            print("Un client hote est déjà connecte.")
                            pygame.display.quit()
                            pygame.quit()
                            sys.exit()

        # Now we define the operations in fuction of the class's status.

        if not self.connection:
            self.sprt.hors_line.activated = True
            self.current_time += 33.4
            if self.current_time >= self.max_time:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

        elif self.status and self.status == "hote":
                self.current_time += 33.4
                if self.current_time >= self.max_time:
                    self.sprt.presentation.activated = False
                    self.movie = True

        elif self.status and self.status == "guest":
            self.hote = False
            self.to_game = True

    def draw(self):
        """Draw."""
        self.sprt.main_surface.fill((0, 0, 0))
        self.sprt.main_surface.blit(self.sprt.hors_line.image, (0, 0))
        self.sprt.main_surface.blit(self.sprt.presentation.image, (0, 0))
