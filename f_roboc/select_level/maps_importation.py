"""Traitement des cartes."""

import glob


def list_maps():
    """List les maps présentes dans le dossier 'map'.

    Retourne ensuite le nom de la map, et son contenu.

    Attention: seul les cinq premières maps seront
    prises en compte (par soucis de simplicité)!
    """
    # maps_path = glob.glob('maps/*.txt')
    maps_path = glob.glob('f_roboc/maps/*.txt')
    maps_name = []
    contents = []

    too_much_maps = False
    invalide_files = False

    for i, file in enumerate(maps_path):
        if i > 4:
            too_much_maps = True
            break

        file_content = import_map(file)

        if valide_file(file_content, file[13:-4], i):
            maps_name.append(file[13:-4])
            contents.append(file_content)
        else:
            invalide_files = True

    return maps_name, contents, too_much_maps, invalide_files


def import_map(file):
    """Import le contenu du fichier map choisit.

    Retourne une liste.
    """
    contents = []

    with open(file) as f:
        for line in f:
            contents.append(list(line))

            if '\n' in contents[-1]:
                contents[-1].remove('\n')

    return contents


def valide_file(file, name, i):
    """Test si le fichier est valide."""
    possibles_keys = ['O', ' ', '.', 'T', 'V']
    teleporters = 0
    start_path = 0
    victory = 0
    if len(file) != 9:
        error_msg(name, i, "la map ne fait pas 9 cases de haut.", file)
        return False
    for line in file:
        if len(line) != 20:
            error_msg(name, i,
                      "Une ligne de la map ne fait pas 20 cases de long.",
                      file)
            return False
        for key in line:
            if key not in possibles_keys:
                error_msg(name, i,
                          'un ou plusieurs caracteres sont invalides.',
                          file)
                print("caractere invalide: '{0}'".format(key))
                print("caracteres possibles: 'O', ' ', '.', 'T' et 'V'.")
                return False
            if key == 'T':
                teleporters += 1
            if key == '.':
                start_path += 1
            if key == 'V':
                victory += 1

    if teleporters != 2 and teleporters != 0:
        error_msg(name, i,
                  "le nombre de teleporters ('T') doit etre egal a 0 ou 2.",
                  file)
        print('nombre de teleporters: {0}'.format(teleporters))
        return False
    """if start_path < 4:
        error_msg(name, i,
                  "la map doit posseder au moins 4 caractères de type '.'",
                  file)
        return False"""
    if victory != 1:
        error_msg(name, i,
                  "la map doit posseder un seul caractère de type 'V'.",
                  file)
        return False

    return True


def error_msg(map_name, i, message, file):
    """Définit les messages d'erreur affichés dans le terminal."""
    i += 1
    print("\nErreur sur la map {0}, titre '{1}'.".format(i, map_name))
    print(message)
    print("Details de la map:")
    for line in file:
        good_line = ''.join(line)
        print(good_line)
