import signal
import sys
from collections import deque
from multiprocessing import Process

from RPi import GPIO

from lib.conf import conf
from lib.mode import Mode
from lib.modes.random_lights import RandomLights  # noqa
from lib.modes.rotator import Rotator  # noqa
from lib.modes.wave import Wave  # noqa
from lib.pixel_hat import PixelHat
from lib.redis_manager import RedisManager


class Controller:
    """Management class."""

    def __init__(self):
        """Construct."""
        self.hat = PixelHat()
        self.redisman = RedisManager()
        self.redisman.populate(flush=True)
        self.conf = conf

        self.modes = deque(Mode.__subclasses__())

        self.mode = None
        self.process = None
        self.bump_mode(None)

    def restart_process(self):
        """Restart the process."""
        print("Restarting process")
        if self.process and self.process.is_alive():
            self.process.terminate()

        self.mode = self.mode_class(self.hat)
        self.redisman.set("mode", self.mode.name)
        self.process = Process(target=self.mode.run)
        self.process.start()

    def bump_mode(self, _):
        """Bump mode."""
        self.mode_class = self.modes.pop()
        self.modes.appendleft(self.mode_class)

        self.restart_process()

    def bump_axis(self, _):
        """Bump mode."""
        print("Bumping axis")
        axes = ["x", "y", "z"]
        current_axis = self.redisman.get("axis")
        self.redisman.set("axis", axes[(axes.index(current_axis) + 1) % 3])

        self.restart_process()

    def bump_invert(self, _):
        """Bump mode."""
        print("Bumping invert")
        current_invert = self.redisman.get("invert")
        if current_invert == "true":
            self.redisman.set("invert", "false")
        else:
            self.redisman.set("invert", "true")

        self.restart_process()

    def bump_colour(self, _):
        """Bump mode."""
        print("Bumping colour")
        colours = list(self.conf["colours"].keys())
        current_colour = self.redisman.get("colour")
        self.redisman.set(
            "colour", colours[(colours.index(current_colour) + 1) % len(colours)]
        )

        self.restart_process()

    def signal_handler(self, _, __):
        """Handle a Ctrl-C etc."""
        GPIO.cleanup()
        sys.exit(0)

    def manage(self):
        """Do the thing."""
        GPIO.setmode(GPIO.BCM)
        for name, pins in self.conf["buttons"].items():
            GPIO.setup(pins["logical"], GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(
                pins["logical"],
                GPIO.FALLING,
                callback=getattr(self, f"bump_{name}"),
                bouncetime=500,
            )

        signal.signal(signal.SIGINT, self.signal_handler)
        signal.pause()


if __name__ == "__main__":
    con = Controller()
    con.manage()
