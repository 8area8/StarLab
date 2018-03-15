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

        # END MOOVE OPTIONS
        self.tp = None
        self.victory = False

    def init_moove(self, hero_coords, directions, tp, victory):
        """Initalization of the movement.

        Create a list of coordinates.
        """
        self.tp = csc.transform_coords_to('string', tp) if tp else None
        self.victory = victory

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

                if self.victory:
                    msg += " victory! "
                elif self.tp:
                    msg += f" teleportation:{self.tp} "
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


class Teleportation:
    """Teleportation class."""

    def __init__(self):
        """Initialization."""
        self.coords = ()

        self.activated = False
        self.name = ""

        self.key = 'starting'
        self.index = 0
        self.current_time = 0.0

    def activate(self, coords, name):
        """Activate the teleportation."""
        self.coords = csc.transform_coords_to('string', coords)
        self.activated = True
        self.index = 0
        self.key = 'starting'
        self.name = name

    def update(self):
        """Update the teleportation."""
        if not self.activated:
            return ""

        if self.name == "superstar":
            max_imgs = {"starting": 23, "landed": 13}
        else:
            max_imgs = {"starting": 20, "landed": 10}

        msg = "teleport:"

        self.current_time += 33.4
        if not self.current_time >= 100:
            return ""

        self.current_time = 0.0

        if self.index < max_imgs[self.key]:
            index = str(self.index)
            index = '0' + index if self.index < 10 else index
            msg += f"{self.key}:{index} "
            self.index += 1

        else:

            if self.key == "starting":
                msg += f"teleportNow:{self.coords} "
                self.key = "landed"
                self.index = 0
            else:
                msg += "end"
                self.activated = False

        return msg if msg != 'teleport:' else ''
