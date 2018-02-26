"""Gere le temps."""


class TimeController:
    """Main class."""

    def __init__(self):
        """Init."""
        self.init_zero()

    def update(self, player_msg, in_action):
        """Mise à jour."""
        if "next_turn" in player_msg:
            self.init_zero()
            return "next_turn"

        msg = ""

        if self.current_dixseconds == 10:
            if self.current_seconds == 9 and in_action:
                return msg
            self.current_seconds = (self.current_seconds + 1) % 10
            self.current_dixseconds = 0
            if self.current_seconds == 0:
                msg += "next_turn"
            else:
                msg += "new_second"

        if self.current_milliseconds >= 100:
            self.current_milliseconds = 0
            self.current_dixseconds += 1

        self.current_milliseconds += 33.4

        return msg

    def init_zero(self):
        """Initialize at 0."""
        self.current_milliseconds = 0.0

        self.current_dixseconds = 0
        self.current_seconds = 0
