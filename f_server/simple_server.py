"""The basic server."""

import select

import constants.find as fd


class SimpleServer:
    """The basic server, the first used."""

    def __init__(self, main_connection, client_sockets):
        """Initialize the server."""
        self.go_to = ''

        self.main_connection = main_connection
        self.client_sockets = client_sockets

        self.nb_players = 0
        self.map_content = ""

    def run_a_turn(self):
        """Run server's instruction for a turn."""
        self._receive_and_return()

    def _receive_and_return(self):
        """Receive datas from the clients."""
        client_to_read = []
        try:
            client_to_read, wlist, xlist = select.select(
                self.client_sockets, [], [], 0.05)
        except select.error:
            pass
        else:
            for client in client_to_read:
                self._deal_and_send_to(client)

    def _deal_and_send_to(self, client):
        """Send datas to each client."""
        msg = client.recv(1024)
        msg = msg.decode()
        new_msg = ''

        if not msg or 'players?' in msg:
            return

        print("Received: {0}".format(msg))

        if "is_game_init" in msg:
            new_msg += "game_init_no "

        if "is_game_running" in msg:
            new_msg += "game_running_no "

        if "create_game" in msg:
            self.nb_players = fd.find_number_after('nb_players:', msg)
            self.map_content = fd.find_text_after('map:', msg)
            self.go_to = 'init_game'

        if new_msg:
            new_msg = new_msg.encode()
            client.send(b'send by server:')
            client.send(new_msg)
