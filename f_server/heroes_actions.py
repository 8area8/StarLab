"""Controle les actions des héros."""


class Transform:
    """Class."""

    def __init__(self):
        """Init."""
        self.activated = False

        self.current_time = 0.0
        self.index = 0
        self.ascend = True

        self.str_coords = ""

    def activation(self, str_coords, orders):
        """Activation."""
        self.activated = True
        self.str_coords = str_coords

        for i in range(len(orders)):
            orders[i] += "transform:activated,coords:" + str_coords

    def update(self, orders):
        """Update."""
        if not self.activated:
            return

        msg = "transform:"
        self.current_time += 33.4
        if self.current_time >= 100:
            self.current_time = 0.0

            if self.ascend:
                if self.index == 8:
                    self.ascend = False
                    msg += "transfNow:" + self.str_coords
                else:
                    self.index += 1
                    msg += "index{}".format(self.index)
            else:
                if self.index == 0:
                    self.ascend = True
                    self.activated = False
                    msg += "end"
                else:
                    self.index -= 1
                    msg += "index{}".format(self.index)

        if msg == 'transform:':
            return

        for i in range(len(orders)):
            orders[i] += msg


class Moove:
    """Class."""

    def __init__(self):
        """Init."""
        self.hero_coords = ()
        self.list_coords = []

        self.v_x = 0
        self.v_y = 0

        self.index = 1

        self.activated = False

    def init_moove(self, hero_coords, directions):
        """Init. moove."""
        self.v_x = 0
        self.v_y = 0
        self.index = 0
        self.list_coords = []

        self.activated = True
        self.hero_coords = get_tuple_coords(hero_coords)

        x, y = self.hero_coords
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

    def update(self, orders):
        """Moove."""
        if not self.activated:
            return

        if self.hero_coords == self.list_coords[self.index][0]:
            self.index += 1
            if self.index == len(self.list_coords):
                self.activated = False
                for i in range(len(orders)):
                    orders[i] += "moove:end "
                return
            self.init_direction()

        x, y = self.hero_coords
        a, b = self.v_x, self.v_y
        x += a
        y += b
        self.hero_coords = x, y

        str_coords = get_string_coords(self.hero_coords)

        for i in range(len(orders)):
            orders[i] += "moove:{} ".format(str_coords)

    def init_direction(self):
        """Init."""
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
            raise ValueError("lettre invalide.")


def get_string_coords(coords):
    """Get."""
    str_coords = ""

    for number in coords:
        msg = ""
        if number < 1000:
            msg += "0"
            if number < 100:
                msg += "0"
                if number < 10:
                    msg += "0"
        msg += "{}".format(number)
        str_coords += msg + ","

    return str_coords


def get_tuple_coords(str_coords):
    """Get."""
    x = int(str_coords[:4])
    y = int(str_coords[5:])
    print(x, y)

    return x, y
