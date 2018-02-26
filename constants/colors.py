"""This module contains the color's treatment for some game's sprites."""

WHITE = (255, 241, 232, 255)
BLUE = (41, 173, 255, 255)


def find_color(color):
    """Define and return the true value of color's parameter.

    The possibles values are:

    - 'blue'
    - 'white'

    """
    if color == 'blue':
        true_color = BLUE
    elif color == 'white':
        true_color = WHITE
    else:
        raise ValueError(
            "Invalide color value.\n"
            "Valide values are 'blue' and 'white'.")

    return true_color
