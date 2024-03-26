from multiprocessing import Process, Value

from lib.brightness_controllers.rotator import Rotator
from lib.conf import conf
from lib.custodian import Custodian
from lib.logger import logging
from lib.oled import Oled
from lib.tools import is_pi


class BrightnessControl:
    """Normalises colours."""

    def __init__(self):
        """Construct."""
        self.max_brightness = Value("f", conf["brightness"]["max"])
        self.factor = Value("f", conf["brightness"]["default"])
        self.step_size = 0.1

        self.custodian = Custodian("hat")
        self.oled = Oled(self.custodian)
        self.rotator = Rotator(self)
        self.processes = {}

        self.update_display()

    def adjust(self, direction):
        """Adjust brightness."""
        logging.debug("turning brightness `%s`", direction)
        logging.debug("old value: `%f`", self.factor.value)

        if direction == "down":
            self.factor.value = max(self.factor.value - self.step_size, 0)

        if direction == "up":
            self.factor.value = min(
                self.factor.value + self.step_size, self.max_brightness.value
            )

        logging.debug("new value: `%f`", self.factor.value)

        self.update_display()

    def update_display(self):
        """Update the brightness-bar."""
        self.custodian.set("brightness", self.factor.value)
        if is_pi():
            self.oled.update()  # nocov

    def run(self):
        """Do the work."""
        self.run_rotary()

    def run_rotary(self):
        """Run the rotary."""
        # TODO: this could be just a single process now
        if "rotary" not in self.processes:
            self.processes["rotary"] = Process(target=self.rotator.rotate)
            self.processes["rotary"].start()
