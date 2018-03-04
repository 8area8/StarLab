"""This module has different methods of processing coordinates."""

from constants.game_sizes import CASE_SIZE


"""RELATIVE PATH.
_________________

Defines the set of possible coordinates
for displacements, in a relative path.
"""

MAX_MOOVE = 7


def get_relatives_moove_coords(relatives_coords=[], moove=MAX_MOOVE):
    """Return a list who contains the possibilities of movements.

    for each moove point, the list get a list of relatives coordinates.


    TIP: the 'relative_coords' parameter is created only ONE time,
    at the first function's call. As it is a mutable object,
    if we manipulate the parameter, it will save the changes.
    """
    relatives_coords.append([])

    for i in range(1, moove + 1):

        actual_list = relatives_coords[-1]
        a = moove - i
        b = i

        actual_list.append((a, b))
        actual_list.append((b, a))

        if a != 0:
            actual_list.append((-a, b))
            actual_list.append((b, -a))
        if b != 0:
            actual_list.append((a, -b))
            actual_list.append((-b, a))
        if a != 0 and b != 0:
            actual_list.append((-a, -b))
            actual_list.append((-b, -a))

    relatives_coords[-1] = list(set(actual_list))  # remove duplicates.
    relatives_coords[-1].sort(key=lambda x: max(abs(x[0]), abs(x[1])))
    """Wtf sorting. Not usefull but funny."""

    if moove > 1:
        get_relatives_moove_coords(moove=moove - 1)

    return relatives_coords


RELATIVES_COORDS = get_relatives_moove_coords()
RELATIVES_COORDS.sort(key=lambda x: [len(y) for y in x])


"""COORDINATES MANIPULATIONS.
_____________________________

These functions transform coordinates into various types and values.
"""


def transform_coords_to(value, coords):
    """Transform coordinates to another value.

    The 'value' parameter must be a string and be equal to:

    - 'real'
    - 'abstract'
    - 'string'
    - 'tuple'

    Be carefull, 'real' and 'abstract' methods does not test if your coords
    are already real or abstract..!
    """
    if value == 'real':
        coords = _get_real_coords_from(coords)
    elif value == 'abstract':
        coords = _get_abstract_coords_from(coords)
    elif value == 'string':
        coords = _get_string_coords_from(coords)
    elif value == 'tuple':
        coords = _get_tuple_coords_from(coords)
    else:
        raise ValueError(f"Wrong value.\n'value' is: {value}")

    return coords


def _get_real_coords_from(abstract_coords):
    """Return real coordinates."""
    x, y = abstract_coords
    x = x * CASE_SIZE
    y = y * CASE_SIZE
    return x, y


def _get_abstract_coords_from(real_coords):
    """Return abstract coordinates."""
    x, y = real_coords
    x = x // CASE_SIZE
    y = y // CASE_SIZE
    return x, y


def _get_string_coords_from(tuple_coords):
    """Return a string version of coordinates."""
    if not isinstance(tuple_coords, tuple):
        raise TypeError('tuple_coords must be a tuple.')

    string_coords = ""

    for number in tuple_coords:
        str_number = ('0' for x in range(4) if number < 10**x)
        string_coords += f"{str_number},"

    return string_coords


def _get_tuple_coords_from(string_coords):
    """Return a tuple from the string version of coordinates."""
    if not isinstance(string_coords, str):
        raise TypeError('string_coords must be a str.')

    x = int(string_coords[:4])
    y = int(string_coords[5:9])

    return x, y


if __name__ == '__main__':
    for line in RELATIVES_COORDS:
        print(line, "\n")
