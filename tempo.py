import concurrent.futures
import time

import board
import keypad

from glowing_hat.tools.tempo_queue import TempoQueue

keys = keypad.Keys((board.D26,), value_when_pressed=False, pull=True)
tq = TempoQueue(4)


def get_input():
    """I don't care."""
    while True:
        event = keys.events.get()
        if event and event.pressed:
            tq.add(time.time())
            if tq.tempo:
                print(tq.tempo)


pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)
pool.submit(get_input)
