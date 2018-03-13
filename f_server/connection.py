"""Connection module, for server."""

import select
from itertools import product


class Connection:
    """Rule the connection between the server and clients."""

    def __init__(self, nb_players, client_sockets, socket):
        """Initialize the initialization."""
        self._nb_players = nb_players

        # SERVER AND CLIENTS SOCKETS
        self._socket = socket
        self._client_sockets = client_sockets
        self._player_sockets = []

        # PLAYERS DATAS
        self.players = []

        self.global_message = ""

    def init_players(self, player_sockets):
        """Initialize the player's list."""
        self._player_sockets = player_sockets

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

    def re_initialize_players_messages(self):
        """reinitialize 'msg' keys."""
        for player in self.players:
            player['msg'] = ''

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

            msg = player['to_send'].encode()
            player["socket"].send(msg)

    def _send_global_message(self):
        """Send a global message to each player."""
        if not self.global_message:
            return

        print(f"send: {self.global_message} to each player.")

        for player in self.players:

            msg = self.global_message.encode()
            player['socket'].send(msg)

    def receive(self):
        """Receive the player's messages."""
        players_to_read = []

        try:
            players_to_read, wlist, xlist = select.select(
                self._player_sockets, [], [], 0)
        except select.error:
            pass
        except ValueError as e:
            raise OSError  # We raise this to be catched by the baseserver try
        else:
            for client, player in product(players_to_read, self.players):
                if client is not player["socket"]:
                    continue

                msg = client.recv(1024)
                player["msg"] = msg.decode()

                if player["msg"]:
                    print(f"\n received from player {player['raddr']}:"
                          f" {player['msg']}.")

    def receive_from_clients(self):
        """Basic reveive from all others clients.

        Return a list of tuples: each tuple contains:
            - the client socket
            - his message.
        """
        client_messages = []
        client_to_read = []

        clients = self._client_sockets
        no_players = [s for s in clients if s not in self._player_sockets]

        try:
            client_to_read, _, _ = select.select(no_players, [], [], 0.05)
        except select.error:
            pass
        else:
            for client in client_to_read:

                message = client.recv(1024).decode()
                if message:
                    print(f'received: {message}')
                client_messages.append((client, message))

        return client_messages
