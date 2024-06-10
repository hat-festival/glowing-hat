# TODO conf all this
import time
import board
import keypad

from glowing_hat.tools.tempo_queue import TempoQueue


class Tempo:
    """Tempo tapper."""

    def __init__(self, owner):
        """Construct."""
        self.owner = owner
        self.tq = TempoQueue(4)
        self.keys = keypad.Keys((board.D26,), value_when_pressed=False, pull=True)

    def pulse(self):
        """Do the work."""
        while True:
            if self.tq.interval < 2:
                self.owner.trigger()
                time.sleep(self.tq.interval)

    def get_taps(self):
        """Collect taps."""
        while True:
            event = self.keys.events.get()
            if event and event.pressed:
                self.tq.add(time.time())
            time.sleep(0.05)
