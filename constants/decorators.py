"""Module who contains some decorators for testing code."""

import time


def print_time_each_call(function):
    """Print call number and time spend after function."""

    def wrapper(self, method, time_now=time.time(), *args, **kwargs):
        """Wrappe the function."""
        function(self, method, *args, **kwargs)

        since_last = time.time() - time_now
        print(f"time since the last call: {since_last}")
        time_now = time.time()

    return wrapper
