import threading
from time import sleep, time

from lib.conf import conf
from lib.logger import logging
from lib.tools import is_pi

if is_pi():  # nocov
    from RPi import GPIO
else:
    import tests.fake_gpio as GPIO  # noqa: N812


class Clicker:
    """Rotary encoder button."""

    def __init__(self, controller):
        """Construct."""
        self.controller = controller
        self.lock_clicker = threading.Lock()

    def watch(self):
        """Wait for a click."""
        self.sw = conf["rotary"]["pins"]["sw"]

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        sw_last_state = GPIO.input(self.sw)
        timestamp = 0
        duration = 0

        while True:
            new_sw_state = GPIO.input(self.sw)
            if new_sw_state != sw_last_state:
                self.lock_clicker.acquire()
                if new_sw_state == 0:
                    timestamp = time()

                if new_sw_state == 1:
                    duration = time() - timestamp
                    logging.debug("clicker released after `%f` seconds", duration)

                    if duration < 1:
                        self.controller.next_mode()
                    elif duration < 5:  # noqa: PLR2004
                        self.controller.show_ip()
                    else:
                        self.controller.hard_reset()

                self.lock_clicker.release()

            sw_last_state = new_sw_state

            sleep(0.1)
