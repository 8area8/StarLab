"""This is the test module for server.py."""

import unittest
import time
from threading import Thread

from server import BaseServer
from f_server.game_server_init import GameServerInit
from f_roboc.connection import ServerConnection


class Server(Thread):
    """This thread run the server."""

    def __init__(self):
        """Initialize the server."""
        super().__init__()
        self.server = BaseServer()

    @property
    def current_server(self):
        """Return the _server variable of self.server."""
        return self.server._server

    def run(self):
        """Run the server if executed."""
        self.server.run()

    def close_server(self):
        """Close the server."""
        self.server._running = False


class TestServer(unittest.TestCase):
    """The testing class for server.py."""

    def setUp(self):
        """The unittest __init__."""
        self._hote = "localhost"
        self._port = 12800

        self.clients = [ServerConnection() for i in range(10)]
        self.server = Server()

    def test_the_connection(self):
        """Test the server connection."""
        self.server.start()

        for client in self.clients:
            client.connect()

        self._test_creating_game()
        self._test_is_game_init()
        self._test_joining_game()
        self._test_if_map_is_received()
        self._test_if_synchronisation_is_ok()

        self._close()

    def _close(self):
        """Close the server."""
        self.server.close_server()
        self.server.join()

    def _test_creating_game(self):
        """Test if a client can create a game.

        The _server variable of server's thread has to change.
        """
        host_player = self.clients[0]
        host_player.send('create_game: nb_players:2 map:'
                         '...      O   OO   .O'
                         'O OOOOOO         O O'
                         'O O    OOOOOOOOO  OO'
                         'O O OOOO  OV O O  OO'
                         'O OT      O  O O   O'
                         'O OOOO OOOO  O O O O'
                         'O O  O O  O      O O'
                         'O    O O  O OOOOOOTO'
                         'OOOOOO O  O O  ...OO')

        time.sleep(0.5)
        self.assertIsInstance(self.server.current_server, GameServerInit)

    def _test_is_game_init(self):
        """Test if another client can join a game."""
        potential_player = self.clients[1]

        potential_player.send('is_game_init?')

        for i in range(10):
            msg = potential_player.receive()
            if msg:
                self.assertIn('game_init_yes', msg)
                break

            if i == 9:
                raise TimeoutError()

    def _test_joining_game(self):
        """Test if a player can join the game."""
        potential_player = self.clients[1]  # Again him.

        potential_player.send('joining_game')
        time.sleep(0.5)
        self.assertIsInstance(self.server.current_server.players, list)

    def _test_if_map_is_received(self):
        """Test if the second player receive a map."""
        player = self.clients[1]  # Now he's a player!

        player.send('need_map')
        time.sleep(0.5)

        for i in range(10):
            msg = player.receive()
            if msg:
                self.assertIn('map:', msg)
                break

            if i == 9:
                raise TimeoutError()

    def _test_if_synchronisation_is_ok(self):
        """Test if the synchronisation between server and clients works."""
        host, player = self.clients[0:2]

        host.send('synchro_ok')
        player.send('synchro_ok')

        time.sleep(0.1)
        self.assertEqual(self.server.current_server._step, 4)
