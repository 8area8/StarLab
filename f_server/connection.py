"""Connection module."""

import select


class Connection:
    """Rule the connection between the server and clients."""

    def __init__(self, nb_players, client_sockets, socket):
        """Initialize the initialization."""
        self._nb_players = nb_players

        # SERVER AND CLIENTS SOCKETS
        self._socket = socket
        self._client_sockets = client_sockets

        # PLAYERS DATAS
        self.players = []

        self.global_message = ""

    def init_players(self, player_sockets):
        """Initialize the player's list."""
        for i, socket in enumerate(player_sockets):
            player = {
                "socket": socket,
                "raddr": socket.getpeername(),
                "msg": "",
                "to_send": "",
                "digit": str(i + 1)}

            self.players.append(player)

    def re_initialize_server_messages(self):
        """Reinitialize 'to_send' keys and 'global_message'."""
        self.global_message = ""

        for player in self.players:
            player['to_send'] = ""

    def send_to(self, client, message):
        """Send a message to a client.

        Used when we wait for new players.
        """
        client.send(message.encode())

    def send(self):
        """Send messages to players."""
        self._send_global_message()
        self._send_private_messages()

    def _send_private_messages(self):
        """Send private messages for each player."""
        for player in self.players:

            if not player['to_send']:
                continue

            print(f"\n send: {player['to_send']} "
                  f"to player: {player['raddr']}")

            player['to_send'] = player['to_send'].encode()
            player["socket"].send(player['to_send'])

    def _send_global_message(self):
        """Send a global message to each player."""
        if not self.global_message:
            return

        print(f"send: {self.global_message} to each player.")

        for player in self.players:

            msg = self.global_message.encode()
            player['socket'].send(msg)

    def receive(self):
        """Receive the client's messages."""
        socket_list = (player['socket'] for player in self.players)
        self.clients_to_read = []

        try:
            self.clients_to_read, wlist, xlist = select.select(
                socket_list, [], [], 0)
        except select.error:
            pass
        else:
            for client, player in zip(self.clients_to_read, self.players):
                if client is not player["socket"]:
                    continue

                msg = client.recv(1024)
                player["msg"] = msg.decode()

                if player["msg"]:
                    print(f"\n received from player {player['raddr']}:"
                          f" {player['msg']}.")

    def receive_from_clients(self):
        """Basic reveive from all clients.

        Return a list of tuples: each tuple contains:
            - the client socket
            - his message.
        """
        client_messages = []
        client_to_read = []
        try:
            client_to_read, wlist, xlist = select.select(
                self._client_sockets, [], [], 0.05)
        except select.error:
            pass
        else:
            for client in client_to_read:

                message = client.recv(1024).decode()
                client_messages.append((client, message))

        return client_messages
