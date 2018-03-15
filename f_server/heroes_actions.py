"""Controle les actions des héros."""

import constants.coordinates as csc


class Transform:
    """Transform class.

    This class manages the transform animation of the cases.
    """

    def __init__(self):
        """Initialization of the class."""
        self.activated = False

        # MANAGEMENT OF TIME
        self.current_time = 0.0
        self.index = 0
        self.pingpong = 'ping'

        # TRANSFORM COORDINATES
        self.s_coords = ""

    def activate(self, coords):
        """Event activation."""
        self.activated = True
        self.s_coords = csc.transform_coords_to('string', coords)

        return f"transform: activated coords:{self.s_coords}"

    def update(self):
        """Event update.

        Return a message who contains the current index of the animation,
        and when to transform the image.
        """
        if not self.activated:
            return ""

        msg = "transform: "

        self.current_time += 33.4
        if not self.current_time >= 100:
            return ""

        self.current_time = 0.0

        if self.pingpong == 'ping':
            if self.index == 8:
                self.pingpong = 'pong'
                msg += f"transfNow:{self.s_coords}"
            else:
                self.index += 1
                msg += f"index:{self.index}"

        elif self.pingpong == 'pong':
            if self.index == 0:
                self.pingpong = 'ping'
                self.activated = False
                msg += "end."
            else:
                self.index -= 1
                msg += f"index:{self.index}"

        return msg if msg != 'transform ' else ''


class Moove:
    """Moove class.

    This class manages the hero's mooving.
    From a path, the class will calculate a movement per frame,
    and change this movement according to the path.
    """

    def __init__(self):
        """Initialization of the class."""
        self.activated = False

        # PATH AND COORDINATES
        self.hero_coords = ()
        self.list_coords = []
        self.index = 1

        # SPEED MOVEMENT AND DIRECTION
        self.v_x = 0
        self.v_y = 0

    def init_moove(self, hero_coords, directions):
        """Initalization of the movement.

        Create a list of coordinates.
        """
        self.v_x = 0
        self.v_y = 0
        self.index = 0
        self.list_coords = []

        self.activated = True
        self.hero_coords = hero_coords

        x, y = hero_coords
        for letter in directions:

            if letter == "l":
                x -= 64
            elif letter == "r":
                x += 64
            elif letter == "t":
                y -= 64
            elif letter == "d":
                y += 64

            self.list_coords.append(((x, y), letter))

        self.init_direction()

    def update(self):
        """Moove the active hero.

        Return a message who contains the new hero's coordinates.
        """
        if not self.activated:
            return ""

        msg = 'moove:'

        if self.hero_coords == self.list_coords[self.index][0]:
            self.index += 1

            if self.index == len(self.list_coords):
                self.activated = False
                msg += "end "
                return msg

            self.init_direction()

        x, y = self.hero_coords
        a, b = self.v_x, self.v_y
        x += a
        y += b
        self.hero_coords = x, y

        msg += csc.transform_coords_to('string', self.hero_coords)

        return msg if msg != 'moove:' else ''

    def init_direction(self):
        """Initialize a new direction according by the index."""
        self.v_x = 0
        self.v_y = 0

        letter = self.list_coords[self.index][1]
        if letter == "l":
            self.v_x = -4
        elif letter == "r":
            self.v_x = 4
        elif letter == 't':
            self.v_y = -4
        elif letter == "d":
            self.v_y = 4
        else:
            raise ValueError("invalid letter.")
