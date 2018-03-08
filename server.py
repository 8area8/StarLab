"""Server source."""

import socket
import select

from f_server.game_server_init import GameServerInit
from f_server.game_server import GameServer
from f_server.simple_server import SimpleServer


class BaseServer:
    """The server class."""

    def __init__(self):
        """Initialize the class."""
        self.hote = ''
        self.port = 12800

        self._socket = socket.socket()
        self._socket.bind((self.hote, self.port))
        self._socket.listen(5)
        print("The server listen now at the port: {}".format(self.port))

        self._running = True
        self.clients_sockets = []

        self._server = SimpleServer(self._socket, self.clients_sockets)

    def run(self):
        """Run the main loop."""
        while self._running:

            self._change_server_state()

            try:

                self._add_clients()
                self._server.run_a_turn()

            except OSError:

                self.clients_sockets = []
                self._server = SimpleServer(self._socket,
                                            self.clients_sockets)
                print('Connection error.\nServer reinitialized.')

        self._close()

    def _add_clients(self):
        """Add news clients to the server.

        For performances issues, i stop the clients connexion after 4 clients.
        """
        if self.clients_sockets and len(self.clients_sockets) > 4:
            return

        wanted_connexions, wlist, xlist = select.select([self._socket],
                                                        [], [], 0)

        for new_connection in wanted_connexions:

            client_socket, connexion_infos = new_connection.accept()
            self.clients_sockets.append(client_socket)

            print('added connection (from server): {0}'.format(
                connexion_infos))

    def _change_server_state(self):
        """Change the server's state if needed."""
        if self._server.go_to == 'init_game':
            nb_players = self._server.nb_players
            map_content = self._server.map_content
            host_player = self._server.host_player
            self._server = GameServerInit(nb_players, map_content,
                                          self.clients_sockets,
                                          host_player, self._socket)

        elif self._server.go_to == 'game_server':
            _map = self._server._map
            self._server = GameServer(self._server.connection, _map)

        elif self._server.go_to == 'default':
            self._server = SimpleServer(self._socket, self.clients_sockets)

    def _close(self):
        """Close the connection."""
        print("closing connections.")
        for client in self.clients_sockets:
            client.close()

        self._socket.close()


if __name__ == '__main__':
    BaseServer().run()
