"""Connection module."""

import select


class Connection:
    """Class."""

    def __init__(self, nb_players, clients_sockets, socket):
        """Initialize the initialization."""
        self._nb_players = nb_players

        # SERVER AND CLIENTS SOCKETS
        self._socket = socket
        self._clients_sockets = clients_sockets

        # PLAYERS DATAS
        self.players = []
        self.create_players_dicts(clients_sockets)

        self.global_message = ""

    def create_players_dicts(self, clients_sockets):
        """Crete."""
        for i, socket in enumerate(clients_sockets):
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

    def send(self, message='private'):
        """Send messages to players.

        You can send privates messages (from "player['to_send']" key),
        or one global message for all players (wich use 'global_message').

        specify to message's parameter:
            - 'private' for private sendings
            - 'global' for global sendings
        """
        if message == 'global':
            self._send_global_message()
        else:
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
        """Receive the player's messages."""
        self.clients_to_read = []
        try:
            self.clients_to_read, wlist, xlist = select.select(
                self._clients_sockets, [], [], 0)
        except select.error:
            pass
        else:
            for client, player in zip(self.clients_to_read, self.players):
                if client is player["socket"]:

                    msg = client.recv(1024)
                    player["msg"] = msg.decode()

                    if player["msg"]:
                        print(f"\n recu de joueur {player['raddr']}:"
                              f" {player['msg']}.")
