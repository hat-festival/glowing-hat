import concurrent.futures

import board
import keypad

from glowing_hat.tempo.tempo import Tempo
from glowing_hat.tools.tempo_queue import TempoQueue

keys = keypad.Keys((board.D26,), value_when_pressed=False, pull=True)
tq = TempoQueue(4)


class TempoPool:
    """Manage tempo for modes."""

    def __init__(self, parent):
        """Construct."""
        self.parent = parent

        self.pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        self.tempo = Tempo(self.parent)
        self.pool.submit(self.parent.reduce)  # TODO rename this?
        self.pool.submit(self.tempo.get_taps)
