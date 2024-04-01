from lib.tools.logger import logging
from lib.tools.utils import is_pi

if is_pi():
    import buttonshim


def controller_bindings(controller):
    """Bind the buttons to the controller."""
    if is_pi():

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

        @buttonshim.on_hold(buttonshim.BUTTON_D, hold_time=1)
        def button_d_handler(_):
            """Handle button D hold."""
            logging.debug("button D held")
            controller.rediscover_wifi()

        @buttonshim.on_hold(buttonshim.BUTTON_E, hold_time=1)
        def button_e_handler(_):
            """Handle button E hold."""
            logging.debug("button E held")
            controller.hard_reset()


def brightness_bindings(controller):
    """Bind the buttons to the brightness-controller."""
    if is_pi():

        @buttonshim.on_press(buttonshim.BUTTON_B, repeat=True)
        def button_a_handler(_, __):
            """Handle button B press."""
            logging.debug("button B pressed")
            controller.adjust("down")

        @buttonshim.on_press(buttonshim.BUTTON_C, repeat=True)
        def button_d_handler(_, __):
            """Handle button C press."""
            logging.debug("button C pressed")
            controller.adjust("up")
