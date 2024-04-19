from multiprocessing import Value

from glowing_hat.button_bindings import brightness_bindings
from glowing_hat.conf import conf
from glowing_hat.custodian import Custodian
from glowing_hat.oled import Oled
from glowing_hat.tools.logger import logging
from glowing_hat.tools.utils import is_pi


class BrightnessControl:
    """Normalises colours."""

    def __init__(self):
        """Construct."""
        self.max_brightness = Value("f", conf["brightness"]["max"])
        self.factor = Value("f", conf["brightness"]["default"])
        self.step_size = 0.1

        self.custodian = Custodian("hat")
        self.oled = Oled(self.custodian)

        brightness_bindings(self)

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
