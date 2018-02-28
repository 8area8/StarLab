"""this module contains the client connection."""

import socket
import select


class ServerConnection:
    """Class client."""

    def __init__(self):
        """Initialize the client."""
        self._hote = "localhost"
        self._port = 12800

        self._socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)

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
                [self._socket], [], [], 0)
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
        """Try to connect to the server."""
        self._socket.connect((self._hote, self._port))

        print("\nconnected to the port: {}".format(self._port))


if __name__ == '__main__':

    sock = ServerConnection()
    print(sock.connected)
