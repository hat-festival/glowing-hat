# http://docs.pimoroni.com/buttonshim/#module-buttonshim

from multiprocessing import Process
from signal import pause
from string import ascii_uppercase

import buttonshim

from lib.conf import conf
from lib.custodian import Custodian
from lib.logger import logging
from lib.modes_list import load_modes, modes

from lib.oled import Oled
from lib.pixel_hat import PixelHat

BUTTONS = {}

for index, data in enumerate(conf["shimbuttons"]):
    BUTTONS[index] = data
    BUTTONS[index]["name"] = ascii_uppercase[index]
    BUTTONS[index]["held"] = False

BUTTON_IDS = list(BUTTONS.keys())


class Controller:
    """Hat controller."""

    def __init__(self):
        """Construct."""
        self.hat = PixelHat()
        self.conf = conf
        self.custodian = Custodian(conf=self.conf)
        self.custodian.populate(flush=False)

        self.modes = modes
        load_modes(self.custodian)
        self.custodian.next("mode")

        self.oled = Oled()

        self.process = None
        self.restart_hat(is_mode=True)

    def restart_hat(self, is_mode=False):
        """Restart the hat."""
        logging.info("restarting hat")
        if self.process and self.process.is_alive():
            self.process.terminate()

        self.mode = self.modes[self.custodian.get("mode")](self.hat)
        if is_mode:
            self.mode.set_preferred_axis()

        self.process = Process(target=self.mode.run)
        self.process.start()
        logging.info("hat restarted")
        self.oled.update()

    def bump(self, parameter):
        """Bump something."""
        logging.info("bumping `%s`", parameter)
        self.custodian.next(parameter)
        logging.info("`%s` is now `%s`", parameter, self.custodian.get(parameter))

        is_mode = parameter == "mode"
        self.restart_hat(is_mode=is_mode)


c = Controller()


@buttonshim.on_release(BUTTON_IDS)
def release_handler(button, _):
    """Handle button release."""
    logging.debug("button `%s` released", BUTTONS[button]["name"])
    if not BUTTONS[button]["held"]:
        green()
        c.bump(BUTTONS[button]["press"])

    else:
        BUTTONS[button]["held"] = False

    off()


@buttonshim.on_hold(BUTTON_IDS, hold_time=1)
def held_handler(button):
    """Handle button hold."""
    logging.debug("button `%s` held", BUTTONS[button]["name"])
    if "hold" in BUTTONS[button]:
        blue()
        c.bump(BUTTONS[button]["hold"])

    else:
        red()

    BUTTONS[button]["held"] = True


def red():
    """LED red."""
    buttonshim.set_pixel(255, 0, 0)


def green():
    """LED green."""
    buttonshim.set_pixel(0, 255, 0)


def blue():
    """LED blue."""
    buttonshim.set_pixel(0, 0, 255)


def off():
    """LED off."""
    buttonshim.set_pixel(0, 0, 0)


def manage():
    """Loop forever."""
    pause()


if __name__ == "__main__":
    manage()
