"""Server source."""

import socket
import select

from f_server.game_server import GameServerInit
from f_server.simple_server import SimpleServer


class BaseServer:
    """The server class."""

    def __init__(self):
        """Initialize the class."""
        self.hote = ''
        self.port = 12800

        self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connexion.bind((self.hote, self.port))
        self.connexion.listen(5)
        print("The server listen now at the port: {}".format(self.port))

        self._running = True
        self.clients_sockets = []

        self._server = SimpleServer(self.connexion,
                                    self.clients_sockets)

    def run(self):
        """Run the main loop."""
        while self._running:

            self._change_server_state(self._server)

            try:

                self._add_clients()
                self._server.run_a_turn()

            except OSError:

                self.clients_sockets = []
                self._server = SimpleServer(self.connexion,
                                            self.clients_sockets)

        self._close()

    def _add_clients(self):
        """Add news clients to the server.

        For performances issues, i stop the clients connexions from 4 clients.
        """
        if len(self.clients_sockets) > 4:
            return

        wanted_connexions, wlist, xlist = select.select(
            [self.connexion], [], [], 0)

        for connexion in wanted_connexions:

            conexion_to_client, connexion_infos = connexion.accept()
            self.clients_sockets.append(conexion_to_client)

            print('added connection (from server): {0}'.format(
                connexion_infos))

    def _change_server_state(self):
        """Change the server's state if needed."""
        if isinstance(self._server, SimpleServer):
            if self._server.go_to_game:

                self._server = GameServerInit(self.connexion,
                                              self.clients_sockets)

    def _close(self):
        """Close the connection."""
        print("closing connections.")
        for client in self.clients_sockets:
            client.close()

        self.connexion.close()


if __name__ == '__main__':
    BaseServer().run()
