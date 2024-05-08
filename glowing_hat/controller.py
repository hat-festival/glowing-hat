import os
from multiprocessing import Process
from time import sleep

from glowing_hat.boot_sequence import boot_hat
from glowing_hat.button_bindings import controller_bindings
from glowing_hat.conf import conf
from glowing_hat.custodian import Custodian
from glowing_hat.hat import Hat
from glowing_hat.modes_list import load_modes, modes
from glowing_hat.oled import Oled
from glowing_hat.strings_list import load_strings
from glowing_hat.tools.logger import logging


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

        load_strings(self.custodian)
        self.custodian.next("string")

        self.hat = Hat()
        self.oled = Oled(self.custodian)

        controller_bindings(self)

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

    def next_string(self):
        """Bump to next string."""
        self.custodian.next("string")
        logging.info("`string` is now `%s`", self.custodian.get("string"))

        self.restart_hat()

    def show_ip(self):
        """Show our IP."""
        self.custodian.set("display-type", "ip-address")
        self.oled.update()
        sleep(5)
        self.custodian.set("display-type", "show-mode")
        self.oled.update()

    def reset_hat(self):
        """Reset when we get stuck."""
        self.custodian.set("display-type", "reset")
        self.oled.update()
        logging.info("resetting hat")

        service = "manager"
        os.system(f"/usr/bin/sudo service {service} restart")  # noqa: S605

    def reboot(self):
        """If we get really stuck."""
        self.custodian.set("display-type", "reboot")
        self.oled.update()
        logging.info("rebooting pi")

        os.system("/usr/sbin/reboot")  # noqa: S605
