"""This module contains some specials 'string find' functions."""

from constants.coordinates import transform_coords_to


def find_and_get_coords_after(sub_message, message):
    """Return coordinates after the sub_message.

    get the string version of coordinates then transform it into tuple.
    """
    index = message.find(sub_message) + len(sub_message)
    string_coordinates = message[index:index + 9]

    coordinates = transform_coords_to('tuple', string_coordinates)

    return coordinates


def find_number_after(sub_message, message):
    """Return a number after the sub_message.

    Only the first digit is returned.
    """
    index = message.find(sub_message) + len(sub_message)
    number = int(message[index])

    return number


def find_text_after(sub_message, message):
    """Return some text, after the sub_message.

    The text ends at the first character space from sub_message,
    or the end of message.
    """
    is_a_map = True if sub_message == 'map:' else False

    index = message.find(sub_message) + len(sub_message)
    endex = (index + 180) if is_a_map else message.find(' ', index)

    if endex == -1:  # if no space found (return -1), endex = end of message.
        endex = len(message)

    text = message[index:endex]

    return text
