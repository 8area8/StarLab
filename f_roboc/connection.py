"""this module contains the client connection."""

import socket
import select
from threading import Thread


class ServerConnection():
    """Client class."""

    def __init__(self):
        """Initialize the client."""
        super().__init__()
        self.hote = "localhost"
        self.port = 12800

        self._socket = socket.socket()

        self._thread = SocketCreator(self)
        self._thread.start()

    @property
    def connected(self):
        """Test if the socket is connected."""
        try:
            self._socket.send(b'')
        except OSError:
            return False
        else:
            return True

    def close(self):
        """Close the client."""
        self._socket.close()

    def send(self, message):
        """Send strings message to the server."""
        if not message:
            return

        print("send: {}".format(message))

        message = message.encode()
        self._socket.send(message)

    def receive(self):
        """Reception of data's server.

        select's module is not a good way,
        so that code is bad.
        """
        msg = ''
        server_list = []
        try:
            server_list, wlist, xlist = select.select(
                [self._socket], [], [], 0.01)
        except select.error:
            pass
        else:
            for server in server_list:
                msg = server.recv(1024)
                msg = msg.decode()
        if msg:
            print("received: {}".format(msg))
        return msg

    def connect(self):
        """Try to connect to the server.

        I actually use a thread to do this,
        because i have a slowdown problem with this task.
        """
        if self._thread.is_alive():  # avoid duplicates
            return

        self._thread = SocketCreator(self)
        self._thread.start()


class SocketCreator(Thread):
    """Thread that create sockets because creating socket is too slow.

    I do not have answers for this problem,
    so if someone know why creating socket slow the program,
    please contact me..!
    """

    def __init__(self, connection):
        """Thread init."""
        super().__init__()

        self.connection = connection
        self._hote = self.connection.hote
        self._port = self.connection.port

        self._socket = socket.socket()

    def run(self):
        """Run the thread."""
        try:
            self.connect()
            print(f"\nconnected to the port: {self._port}")

        except ConnectionRefusedError:
            self._socket.close()
            return

    def connect(self):
        """Connect the thread."""
        self._socket.connect((self._hote, self._port))
        self.connection._socket = self._socket


if __name__ == '__main__':

    sock = ServerConnection()
    print(sock.connected)
