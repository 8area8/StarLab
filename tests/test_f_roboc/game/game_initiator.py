"""Game initiator."""


def return_game_infos(nb_players, map_content):
    """Send game."""
    temp_map = []

    for line in map_content:
        temp_map.append("".join(line))
    temp = "Q".join(temp_map)

    orders = "new_game:{},{}".format(nb_players, temp)
    return orders


def wait_game_infos(clt):
    """Attend les données du jeu."""
    print("En attente des infos de connection:")

    orders = "need_map"
    clt.send(orders)
    received = False

    while not received:
        msg = clt.receive()
        if 'new_game' in msg:

            map_contents = []
            temp_map_contents = msg[12:].split("Q")
            for line in temp_map_contents:
                map_contents.append(list(line))

            received = True
            print('informations de jeu recues.')
            print('map recue: ', map_contents)
            return map_contents


def wait_new_players(msg):
        """Attend de nouvelles connections."""
        player_turn = None
        player_number = None
        nb_players = None

        if "players_ok" in msg:

            i = msg.find("player_number:")
            i += 14
            player_number = int(msg[i])

            index = msg.find("player_turn:") + 12
            player_turn = int(msg[index])

            index = msg.find("nb_players:") + 11
            nb_players = int(msg[index])

        return (player_turn, player_number, nb_players)


def define_players(msg, player_number, players):
    """Define the player's list."""
    index = msg.find("nb_players:") + 11
    nb_players = int(msg[index])

    for i in range(nb_players):
        i += 1

        is_yours = False
        if player_number == i:
            is_yours = True

        index = msg.find("player{}_place:".format(i)) + 14
        spawn = int(msg[index:index + 3])
        print("dans g_i. spawn du joueur: ", spawn)

        if i == 1:
            players.append([i, "superstar", is_yours, spawn])
        else:
            players.append([i, "superalien", is_yours, spawn])
