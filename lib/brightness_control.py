from multiprocessing import Process, Value

from lib.brightness_controllers.rotator import Rotator
from lib.conf import conf
from lib.custodian import Custodian
from lib.gamma import gamma
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
            self.oled.update()

    def normalise(self, triple):
        """Normalise a colour."""
        factor = max(self.factor.value, 0)
        return tuple(int(x * factor) for x in gamma_correct(triple))

    def run(self):
        """Do the work."""
        self.run_rotary()

    def run_rotary(self):
        """Run the rotary."""
        if "rotary" not in self.processes:
            self.processes["rotary"] = Process(target=self.rotator.rotate)
            self.processes["rotary"].start()


def gamma_correct(triple):
    """Gamma-correct a colour."""
    return tuple(map(lambda n: gamma[int(n)], triple))  # noqa: C417
