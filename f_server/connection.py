"""Connection module."""

import select


class ConnectionController:
    """Class."""

    def __init__(self, nb_players, connected_clients, main_connection):
        """Init."""
        self._nb_players = nb_players
        self._main_connection = main_connection
        self._connected_clients = connected_clients
        self.wait_for_new_players()

        self.players = []
        self.create_players_dicts(connected_clients)

    def create_players_dicts(self, connected_clients):
        """Crete."""
        for i, client in enumerate(connected_clients):
            player = {
                "socket": client,
                "raddr": client.getpeername(),
                "msg": "",
                "number": str(i + 1)}

            self.players.append(player)

    def send(self, orders):
        """Send."""
        for i, player in enumerate(self.players):
            msg = orders[i]

            if msg is "e":
                continue

            msg = msg.encode()
            print("\n envoit de: {} à joueur {}".format(
                msg, player["raddr"]))

            player["socket"].send(msg)

    def receive(self):
        """Recoit les messages des clients."""
        self.clients_to_read = []
        try:
            self.clients_to_read, wlist, xlist = select.select(
                self._connected_clients, [], [], 0)
        except select.error:
            pass
        else:
            # On parcourt la liste des clients à lire
            for client in self.clients_to_read:
                for player in self.players:
                    if client is player["socket"]:
                        plr = player

                plr["msg"] = client.recv(1024)
                plr["msg"] = plr["msg"].decode()
                if plr["msg"]:
                    print("\n recu de joueur {}: {}.".format(
                        plr["raddr"], plr["msg"]))
