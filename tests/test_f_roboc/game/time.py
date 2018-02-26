"""Gere le temps."""


class TimeController:
    """Main class."""

    def __init__(self):
        """Init."""
        self.current_milliseconds = 0.0

        self.current_dixseconds = 0

    def update(self):
        """Mise à jour."""
        self.current_milliseconds += 33.4

        if self.current_milliseconds >= 100:
            self.current_milliseconds = 0
            self.current_dixseconds += 1

        if self.current_dixseconds == 3:
            self.current_dixseconds = 0
            return "2/10 seconds"

        return ""
