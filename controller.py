import json
import sys
from collections import deque
from multiprocessing import Process
from signal import pause

from gpiozero import Button

from lib.conf import conf
from lib.mode import Mode
from lib.modes.bands import Bands  # noqa
from lib.modes.larsen import Larsen  # noqa
from lib.modes.rotator import Rotator  # noqa
from lib.pixel_hat import PixelHat
from lib.redis_manager import RedisManager
from lib.rollers.free_roller import FreeRoller
from lib.rollers.random_roller import RandomRoller
from lib.rollers.set_roller import SetRoller


class Controller:
    """Management class."""

    def __init__(self):
        """Construct."""
        self.hat = PixelHat()
        self.redisman = RedisManager()
        self.redisman.populate()
        self.conf = conf
        self.buttons = {}
        self.modes = deque(Mode.__subclasses__())

        self.rollers = deque(
            [
                SetRoller("rgb", self.conf["colour-sets"]["rgb"]),
                SetRoller("rainbow", self.conf["colour-sets"]["rainbow"]),
                FreeRoller(),
                RandomRoller(),
            ]
        )

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
        if self.buttons["colour"]["was-held"]:
            print("Changing roller")
            self.rollers.rotate(-1)
            self.redisman.set("roller", self.rollers[0].name)
            self.restart_process()
            self.buttons["colour"]["was-held"] = False

        print("Bumping colour")

        clr = self.rollers[0].next
        if type(clr).__name__ == "list":
            clr = json.dumps(clr)
        self.redisman.set("colour", clr)
        self.restart_process()

    def signal_handler(self, _, __):
        """Handle a Ctrl-C etc."""
        sys.exit(0)

    def held_mode(self, _):
        """Mode button held."""
        self.buttons["mode"]["was-held"] = True

    def held_colour(self, _):
        """Colour button held."""
        self.buttons["colour"]["was-held"] = True

    def held_axis(self, _):
        """Axis button held."""
        self.buttons["axis"]["was-held"] = True

    def held_invert(self, _):
        """Invert button held."""
        self.buttons["invert"]["was-held"] = True

    def manage(self):
        """Do the thing."""
        for name, pins in self.conf["buttons"].items():
            self.buttons[name] = {}
            self.buttons[name]["button"] = Button(pins["logical"])
            self.buttons[name]["was-held"] = False
            self.buttons[name]["button"].when_held = getattr(self, f"held_{name}")
            self.buttons[name]["button"].when_released = getattr(self, f"bump_{name}")

        pause()


if __name__ == "__main__":
    con = Controller()
    con.manage()
