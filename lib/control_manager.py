import buttonshim

from lib.controller import Controller
from lib.tools.logger import logging


def start():
    """Run the controller."""
    # this is horrible, but the buttons are tricky
    # TODO: make this less awful
    c = Controller()

    @buttonshim.on_release(buttonshim.BUTTON_A)
    def button_a_handler(_, __):
        """Handle button A release."""
        logging.debug("button A released")
        c.next_mode()

    @buttonshim.on_release(buttonshim.BUTTON_D)
    def button_d_handler(_, __):
        """Handle button D release."""
        logging.debug("button D released")
        c.show_ip()

    @buttonshim.on_hold(buttonshim.BUTTON_E, hold_time=1)
    def button_e_handler(_):
        """Handle button E hold."""
        logging.debug("button E held")
        c.hard_reset()
