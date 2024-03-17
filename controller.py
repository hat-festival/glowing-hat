import os
from collections import deque
from multiprocessing import Process
from random import shuffle
from signal import pause
from string import ascii_uppercase

import buttonshim

from lib.axis_manager import AxisManager
from lib.conf import conf
from lib.custodian import Custodian
from lib.hat import Hat
from lib.logger import logging
from lib.modes_list import load_modes, modes
from lib.oled import Oled

BUTTONS = {}

for index, data in enumerate(conf["buttons"]):
    BUTTONS[index] = data
    BUTTONS[index]["name"] = ascii_uppercase[index]
    BUTTONS[index]["held"] = False

BUTTON_IDS = list(BUTTONS.keys())


class Controller:
    """Hat controller."""

    def __init__(self):
        """Construct."""
        self.hat = Hat()
        self.conf = conf
        self.custodian = Custodian(conf=self.conf, namespace="hat")
        self.custodian.populate(flush=False)

        self.axis_manager = AxisManager(cube_radius=1.1)
        self.axis_manager.populate()

        # we pre-load all the modes because it takes a long time
        self.modes = modes
        load_modes(self.custodian)
        self.custodian.next("mode")

        self.oled = Oled(self.custodian)

        self.process = None

        self.boot_hat()
        self.restart_hat()

    def boot_hat(self):
        """Boot the hat."""
        self.custodian.set("display-type", "boot")
        self.custodian.rotate_until("colour-source", "wheel")
        self.oled.update()

        if os.environ.get("LOGLEVEL") != "debug":
            colour = self.custodian.get("colour")

            indeces = deque(list(range(len(self.hat))))
            while len(indeces):
                shuffle(indeces)
                victim = indeces.pop()
                self.hat.light_one(victim, colour)

            indeces = deque(list(range(len(self.hat))))
            while len(indeces):
                shuffle(indeces)
                victim = indeces.pop()
                self.hat.light_one(victim, [0, 0, 0])

        self.custodian.rotate_until("display-type", "hat-settings")

    def restart_hat(self):
        """Restart the hat."""
        logging.info("restarting hat")
        if self.process and self.process.is_alive():
            self.process.terminate()

        self.mode = self.modes[self.custodian.get("mode")](self.hat, self.custodian)

        self.process = Process(target=self.mode.run)
        self.process.start()

        self.hat.restart_normaliser()
        logging.info("hat restarted")
        self.oled.update()

    def bump(self, parameter):
        """Bump something."""
        logging.info("bumping `%s`", parameter)
        if parameter == "reset":
            self.custodian.set("display-type", "reset")
            self.oled.update()
            logging.info("doing hard reset")

            os.system("/usr/bin/sudo service controller restart")  # noqa: S605

        self.custodian.next(parameter)
        logging.info("`%s` is now `%s`", parameter, self.custodian.get(parameter))

        self.restart_hat()


c = Controller()


@buttonshim.on_release(BUTTON_IDS)
def release_handler(button, _):
    """Handle button release."""
    logging.debug(
        "button `%s` held-status: `%s`",
        BUTTONS[button]["name"],
        BUTTONS[button]["held"],
    )
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
    logging.debug(
        "button `%s` held-status: `%s`",
        BUTTONS[button]["name"],
        BUTTONS[button]["held"],
    )
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
