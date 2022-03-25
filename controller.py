import sys

# from collections import deque
from multiprocessing import Process
from signal import pause

from gpiozero import Button

from lib.conf import conf
from lib.custodian import Custodian

# from lib.mode import Mode
from lib.modes.bands import Bands
from lib.modes.larsen import Larsen
from lib.modes.rotator import Rotator
from lib.oled import Oled
from lib.pixel_hat import PixelHat


class Controller:
    """Management class."""

    def __init__(self):
        """Construct."""
        self.hat = PixelHat()
        self.conf = conf
        self.custodian = Custodian(conf=self.conf)
        self.custodian.populate(flush=True)
        self.buttons = {}
        self.oled = Oled()
        self.modes = {
            "bands": Bands,
            "rotator": Rotator,
            "larsen": Larsen,
        }
        for mode in self.modes:
            self.custodian.add_item_to_hoop(mode, "mode")

        self.mode = None
        self.process = None
        self.bump_mode(None)

    def restart_process(self):
        """Restart the process."""
        print("Restarting process")
        if self.process and self.process.is_alive():
            self.process.terminate()

        self.mode = self.modes[self.custodian.get("mode")](self.hat)
        self.process = Process(target=self.mode.run)
        self.process.start()
        self.oled.update()

    def bump_mode(self, _):
        """Bump mode."""
        self.custodian.next("mode")
        self.restart_process()

    def bump_colour(self, _):
        """Bump colour / colour-set."""
        if self.buttons["colour"]["was-held"]:
            print("Bumping colour-set")
            self.custodian.next("colour-set")
            self.custodian.set("colour-source", "redis")
            self.restart_process()
            self.buttons["colour"]["was-held"] = False

        print("Bumping colour")
        self.custodian.next("colour")
        self.restart_process()

    def bump_colour_source(self, _):
        """Bump colour-source."""
        print("Bumping colour-source")
        self.custodian.next("colour-source")
        self.restart_process()

    def bump_axis(self, _):
        """Bump axis / invert."""
        if self.buttons["axis"]["was-held"]:
            print("Bumping invert")
            self.custodian.next("invert")
            self.restart_process()
            self.buttons["axis"]["was-held"] = False

        else:
            print("Bumping axis")
            self.custodian.next("axis")
            self.restart_process()

    def held_mode(self, _):
        """Mode button held."""
        # self.oled.flash()
        self.buttons["mode"]["was-held"] = True

    def held_colour(self, _):
        """Colour button held."""
        self.oled.flash()
        self.buttons["colour"]["was-held"] = True

    def held_colour_source(self, _):
        """Colour-source button held."""
        # self.oled.flash()
        self.buttons["colour_source"]["was-held"] = True

    def held_axis(self, _):
        """Axis button held."""
        self.oled.flash()
        self.buttons["axis"]["was-held"] = True

    def manage(self):
        """Do the thing."""
        for name, pins in self.conf["buttons"].items():
            self.buttons[name] = {}
            self.buttons[name]["button"] = Button(pins["logical"])
            self.buttons[name]["was-held"] = False
            self.buttons[name]["button"].when_held = getattr(self, f"held_{name}")
            self.buttons[name]["button"].when_released = getattr(self, f"bump_{name}")

        pause()

    def signal_handler(self, _, __):
        """Handle a Ctrl-C etc."""
        sys.exit(0)


if __name__ == "__main__":
    con = Controller()
    con.manage()
