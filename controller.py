import os
from multiprocessing import Process
from signal import pause
from time import sleep

import buttonshim

from lib.axis_manager import AxisManager
from lib.boot_sequence import boot_hat
from lib.conf import conf
from lib.custodian import Custodian
from lib.hat import Hat
from lib.logger import logging
from lib.modes_list import load_modes, modes
from lib.oled import Oled


class Controller:
    """Hat controller."""

    def __init__(self):
        """Construct."""
        self.conf = conf
        self.custodian = Custodian(conf=self.conf, namespace="hat")
        self.custodian.populate(flush=False)

        # we pre-load all the modes because it takes a long time
        self.modes = modes
        load_modes(self.custodian)
        self.custodian.next("mode")

        self.hat = Hat()
        self.oled = Oled(self.custodian)

        self.process = None

        boot_hat(self.custodian, self.oled, self.hat)
        self.restart_hat()

    def restart_hat(self):
        """Restart the hat."""
        logging.info("restarting hat")
        if self.process and self.process.is_alive():
            self.process.terminate()

        self.mode = self.modes[self.custodian.get("mode")](self.hat)

        self.process = Process(target=self.mode.run)
        self.process.start()

        logging.info("hat restarted")
        self.oled.update()

    def next_mode(self):
        """Bump to next mode."""
        self.custodian.next("mode")
        logging.info("`mode` is now `%s`", self.custodian.get("mode"))

        self.restart_hat()

    def show_ip(self):
        """Show our IP."""
        self.custodian.set("display-type", "ip-address")
        self.oled.update()
        sleep(5)
        self.custodian.set("display-type", "show-mode")
        self.oled.update()

    def hard_reset(self):
        """Reset when we get stuck."""
        self.custodian.set("display-type", "reset")
        self.oled.update()
        logging.info("doing hard reset")

        os.system("/usr/bin/sudo service controller restart")  # noqa: S605


axis_manager = AxisManager(cube_radius=1.1)
axis_manager.populate()
controller = Controller()


@buttonshim.on_release(buttonshim.BUTTON_A)
def button_a_handler(_, __):
    """Handle button A release."""
    logging.debug("button A released")
    controller.next_mode()


@buttonshim.on_release(buttonshim.BUTTON_D)
def button_d_handler(_, __):
    """Handle button D release."""
    logging.debug("button D released")
    controller.show_ip()


@buttonshim.on_hold(buttonshim.BUTTON_E, hold_time=1)
def button_e_handler(_):
    """Handle button E hold."""
    logging.debug("button E held")
    controller.hard_reset()


def manage():
    """Loop forever."""
    pause()


if __name__ == "__main__":
    manage()
