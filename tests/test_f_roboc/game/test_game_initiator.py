"""The the game_initiator module."""

import unittest
import time

from tests.test_server import Server
from f_roboc.game.game_initiator import GameInitiator
from f_roboc.connection import ServerConnection


class TestGameInit(unittest.TestCase):
    """The testing class."""

    def setUp(self):
        """Before the tests.

        We start with a server thread,
        and a list of two game_initiators (2 players).
        """
        _map = ('...      O   OO   .OQ'
                'O OOOOOO         O OQ'
                'O O    OOOOOOOOO  OOQ'
                'O O OOOO  OV O O  OOQ'
                'O OT      O  O O   OQ'
                'O OOOO OOOO  O O O OQ'
                'O O  O O  O      O OQ'
                'O    O O  O OOOOOOTOQ'
                'OOOOOO O  O O  ...OO')
        _map = _map.split('Q')

        self.server = Server()

        player_one = GameInitiator(ServerConnection(), _map, 2, True)
        player_two = GameInitiator(ServerConnection())
        self.players = [player_one, player_two]

        for player in self.players:
            player.connection.connect()

    def test(self):
        """Test if."""
        self.server.start()

        self.players[0].transfer_datas()
        time.sleep(0.3)
        self.players[1].connection.send('joining_game')

        for x in range(10):
            for player in self.players:
                player.transfer_datas()

        self._close()

    def _close(self):
        """Close the server."""
        self.server.close_server()
        self.server.join()
