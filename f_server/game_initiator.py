"""Game init."""

import random


def test_server_status(players, orders):
    """Retourn les infos de jeu."""
    for i, player in enumerate(players):
        msg = player["msg"]

        if "is_game_init" in msg:
            orders[i] += "game_init_yes "
            orders[i] += "connected_clients:{} ".format(len(players))


def test_game_info(players, orders, map_content):
    """Test and take the game informations."""
    for i, player in enumerate(players):
        msg = player["msg"]

        if "need_map" in msg:
            orders[i] += f"map:{map_content} nb_players:{len(players)}"


def test_start_game(players, orders):
    """Voila."""
    for i, player in enumerate(players):
        msg = player["msg"]

        if "players?" in msg:
            orders[i] += "player_turn:1 players_ok "\
                f"player_number:{player['number']} nb_players:{len(players)}"


def test_synchro(synchro, players):
    """Test la synchronisation des données entre les joueurs."""
    for i, player in enumerate(players):
        msg = player["msg"]

        if "synchro_ok" in msg:
            synchro[i] = True


def init_heroes(players, orders, map_content):
    """Init thes hereos."""
    for i, order in enumerate(orders):
        orders[i] = "start_game player's list: nb_players:{} ".format(
            len(players))

    init_hereos_places(players, orders, map_content)


def init_hereos_places(players, orders, map_content):
    """héhéhé."""
    max_number = map_content.count(".")
    print("il existe {} cases spawners.".format(max_number))
    number_list = []

    for i, player in enumerate(players):

        while True:
            n = random.randint(1, max_number)
            if n in number_list:
                continue
            break
        print("n est egal à ", n)

        number_list.append(n)
        index = 0
        for y in range(1, n + 1):
            index = map_content.find(".", index)
            index += 1

        string_number = "{}".format(index)
        if index < 100:
            string_number = "0" + string_number
            if index < 10:
                string_number = "0" + string_number

        for y, order in enumerate(orders):
            orders[y] += "player{}_place:".format(i + 1) + string_number + " "
