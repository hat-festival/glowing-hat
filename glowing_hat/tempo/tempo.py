# TODO conf all this
import time

import board
import keypad

from glowing_hat.conf import conf


class Tempo:
    """Tempo tapper."""

    def __init__(self, owner):
        """Construct."""
        self.owner = owner
        self.keys = keypad.Keys(
            (getattr(board, f"D{conf['tempo-pin']}"),),
            value_when_pressed=False,
            pull=True,
        )

    def get_taps(self):
        """Collect taps."""
        while True:
            event = self.keys.events.get()
            if event and event.pressed:
                self.owner.trigger()
            time.sleep(0.1)
