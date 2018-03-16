"""This is the test module for server.py."""

from threading import Thread

from server import BaseServer


class Server(Thread):
    """This thread run the server."""

    def __init__(self):
        """Initialize the server."""
        super().__init__()
        self.server = BaseServer()

    @property
    def current_server(self):
        """Return the _server variable of self.server."""
        return self.server._server

    def run(self):
        """Run the server if executed."""
        self.server.run()

    def close_server(self):
        """Close the server."""
        self.server._running = False
