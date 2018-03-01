"""The basic server."""

import select


class SimpleServer:
    """The basic server, the first used."""

    def __init__(self, main_connection, connected_clients):
        """Initialize the server."""
        self.go_to = ''

        self.main_connection = main_connection
        self.connected_clients = connected_clients

        self.nb_players = 0
        self.map_content = ""

    def run_a_turn(self):
        """Run server's instruction for a turn."""
        client_to_read = []
        self._receive(client_to_read)

        print(client_to_read)

        if client_to_read:
            for client in client_to_read:
                self._deal_and_send_to(client)

    def _receive(self, client_to_read):
        """Receive datas from the clients."""
        try:
            client_to_read, wlist, xlist = select.select(
                self.connected_clients, [], [], 0.05)
        except select.error:
            pass

    def _deal_and_send_to(self, client):
        """Send datas to each client."""
        msg = client.recv(1024)
        msg = msg.decode()
        new_msg = ''

        if not msg or 'players?' in msg:
            return

        print("Received: {0}".format(msg))

        if "in_game" in msg:
            new_msg = "in_game:False "
            new_msg += "connected_clients:{}".format(
                len(self.connected_clients))

        if "new_game" in msg:
            self.nb_players = int(msg[9])
            self.map_content = msg[11:]
            self.go_to_game_server = True

        if new_msg:
            new_msg = new_msg.encode()
            client.send(b'send by server:')
            client.send(new_msg)
