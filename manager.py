from signal import pause

import buttonshim

from lib.controller import Controller
from lib.sorters.axis_manager import AxisManager
from lib.tools.logger import logging


def load_sorts():
    """Load the sorts into Redis if required."""
    axis_manager = AxisManager(cube_radius=1.1)
    axis_manager.populate()


def manage():
    """Loop forever."""
    pause()


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


if __name__ == "__main__":
    load_sorts()
    manage()
