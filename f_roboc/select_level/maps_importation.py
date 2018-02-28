"""List all game's maps."""

import glob


def list_maps():
    """List all maps in 'maps' folder.

    Return the name and the content of each map.

    !! Only the 5 first maps will be read !!
    """
    maps_path = glob.glob('f_roboc/assets/maps/*.txt')
    maps_name = []
    contents = []

    too_much_maps = False
    invalide_files = False

    for i, file in enumerate(maps_path):
        if i > 4:
            too_much_maps = True
            break

        file_content = _import_map_from(file)

        if _is_valid(file_content, file[13:-4], i):
            maps_name.append(file[13:-4])
            contents.append(file_content)
        else:
            invalide_files = True

    return maps_name, contents, too_much_maps, invalide_files


def _import_map_from(file):
    """Import the content of  the selected file.

    Return a list.
    """
    contents = []

    with open(file) as f:
        for line in f:
            contents.append(list(line))

            if '\n' in contents[-1]:
                contents[-1].remove('\n')

    return contents


def _is_valid(file, name, i):
    """Test if the file is valid."""
    possibles_keys = ['O', ' ', '.', 'T', 'V']
    teleporters = 0
    start_path = 0
    victory = 0
    if len(file) != 9:
        error_msg(name, i, "the map is not 9 boxes high.", file)
        return False
    for line in file:
        if len(line) != 20:
            error_msg(name, i,
                      "A line of the map is not 20 boxes long.",
                      file)
            return False
        for key in line:
            if key not in possibles_keys:
                error_msg(name, i,
                          'one or more characters are invalid.',
                          file)
                print("invalid character: '{0}'".format(key))
                print("possible characters: 'O', ' ', '.', 'T' et 'V'.")
                return False
            if key == 'T':
                teleporters += 1
            if key == '.':
                start_path += 1
            if key == 'V':
                victory += 1

    if teleporters != 2 and teleporters != 0:
        error_msg(name, i,
                  "the number of teleporters ('T') must be equal to 0 or 2.",
                  file)
        print('number of teleporters: {0}'.format(teleporters))
        return False
    """if start_path < 4:
        error_msg(name, i,
                  "the map must have at least 4 characters of type '.'",
                  file)
        return False"""
    if victory != 1:
        error_msg(name, i,
                  "the map must have a single type character 'V'.",
                  file)
        return False

    return True


def error_msg(map_name, i, message, file):
    """Display error messages in the terminal."""
    i += 1
    print("\nError on the map {0}, title '{1}'.".format(i, map_name))
    print(message)
    print("Map Details:")
    for line in file:
        good_line = ''.join(line)
        print(good_line)
