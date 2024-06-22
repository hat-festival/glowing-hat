import time

import board
import keypad

from glowing_hat.conf import conf


class Tempo:
    """Tempo tapper."""

    def __init__(self, owner):
        """Construct."""
        self.owner = owner
        self.key_low = keypad.Keys(
            (getattr(board, f"D{conf['tempo-pins']['low']}"),),
            value_when_pressed=False,
            pull=True,
        )
        self.key_high = keypad.Keys(
            (getattr(board, f"D{conf['tempo-pins']['high']}"),),
            value_when_pressed=False,
            pull=True,
        )

        try:
            self.method_high = self.owner.trigger_low
            self.method_low = self.owner.trigger_high

        except AttributeError:
            self.method_low = self.method_high = self.owner.trigger

    def get_taps(self):
        """Collect taps."""
        while True:
            event_low = self.key_low.events.get()
            if event_low and event_low.pressed:
                self.method_low()

            event_high = self.key_high.events.get()
            if event_high and event_high.pressed:
                self.method_high()

            time.sleep(0.1)
