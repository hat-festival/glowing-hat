import signal
import sys
from collections import deque
from multiprocessing import Process

from RPi import GPIO

from lib.mode import Mode

from lib.modes.random_lights import RandomLights  # noqa
from lib.modes.z_wave import ZWave  # noqa
from lib.modes.rotator import Rotator  # noqa
from lib.pixel_hat import PixelHat
from lib.redis_manager import RedisManager


class Controller:
    """Management class."""

    def __init__(self):
        """Construct."""
        self.hat = PixelHat()
        self.redisman = RedisManager()
        self.redisman.populate(flush=True)
        self.mode_index = -1

        self.modes = deque(Mode.__subclasses__())

        self.process = None
        self.next_mode(None)

    def next_mode(self, _):
        """Bump to the next mode."""
        if self.process and self.process.is_alive():
            self.process.terminate()

        mode_class = self.modes.pop()
        self.modes.appendleft(mode_class)

        mode = mode_class(self.hat)
        self.process = Process(target=mode.run)
        self.process.start()

        print(f"Mode is now {mode.name}")
        self.redisman.set("mode", mode.name)

    def signal_handler(self, _, __):
        """Handle a Ctrl-C etc."""
        GPIO.cleanup()
        sys.exit(0)

    def manage(self):
        """Do the thing."""
        pin = 25  # from conf
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(
            pin,
            GPIO.FALLING,
            callback=self.next_mode,
            bouncetime=500,
        )
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.pause()


if __name__ == "__main__":
    con = Controller()
    con.manage()
