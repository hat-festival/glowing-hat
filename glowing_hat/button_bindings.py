from time import sleep, time

from glowing_hat.tools.logger import logging
from glowing_hat.tools.utils import is_pi, rgb_from_hsv

if is_pi():
    import buttonshim

reboot_consensus = {"A": 0, "D": 0}


def controller_bindings(controller):
    """Bind the buttons to the controller."""
    if is_pi():

        @buttonshim.on_release(buttonshim.BUTTON_A)
        def button_a_release_handler(_, __):
            """Handle button A release."""
            logging.debug("button A released")
            blue()
            controller.next_mode()
            sleep(1)
            off()

        @buttonshim.on_release(buttonshim.BUTTON_D)
        def button_d_release_handler(_, __):
            """Handle button D release."""
            logging.debug("button D released")
            blue()
            controller.show_ip()
            off()

        @buttonshim.on_release(buttonshim.BUTTON_E)
        def button_e_release_handler(_, __):
            """Handle button E release."""
            logging.debug("button E released")
            blue()
            controller.next_string()
            off()

        @buttonshim.on_hold(buttonshim.BUTTON_E, hold_time=1)
        def button_e_hold_handler(_):
            """Handle button E hold."""
            logging.debug("button E held")
            red()
            controller.reset_hat()

        @buttonshim.on_hold(buttonshim.BUTTON_A, hold_time=3)
        def button_a_hold_handler(_):
            """Handle button A hold."""
            from glowing_hat.tools.logger import logging

            logging.debug("button A held")
            reboot_consensus["A"] = time()
            check_for_reboot(reboot_consensus)

        @buttonshim.on_hold(buttonshim.BUTTON_D, hold_time=3)
        def button_d_hold_handler(_):
            """Handle button D hold."""
            from glowing_hat.tools.logger import logging

            logging.debug("button D held")
            reboot_consensus["D"] = time()
            check_for_reboot(reboot_consensus)

        def check_for_reboot(reboot_consensus):
            """Check if we should reboot."""
            timestamps = tuple(reboot_consensus.values())
            if abs(timestamps[0] - timestamps[1]) < 1:
                red()
                logging.debug("rebooting pi")
                controller.reboot()


def brightness_bindings(controller):
    """Bind the buttons to the brightness-controller."""
    if is_pi():

        @buttonshim.on_press(buttonshim.BUTTON_B, repeat=True, repeat_time=0.2)
        def button_b_press_handler(_, __):
            """Handle button B press."""
            logging.debug("button B pressed")
            colour_from_hue(0.8)
            controller.adjust("down")
            off()

        @buttonshim.on_press(buttonshim.BUTTON_C, repeat=True, repeat_time=0.2)
        def button_c_press_handler(_, __):
            """Handle button C press."""
            logging.debug("button C pressed")
            colour_from_hue(0.2)
            controller.adjust("up")
            off()


def red():
    """Make the pixel red."""
    colour_from_hue(1)


def green():
    """Make the pixel green."""
    colour_from_hue(1 / 3)


def blue():
    """Make the pixel blue."""
    colour_from_hue(2 / 3)


def off():
    """TUrn the pixel off."""
    buttonshim.set_pixel(0, 0, 0)


def colour_from_hue(hue):
    """Set the colour from the hue."""
    rgb = rgb_from_hsv(hue)
    buttonshim.set_pixel(*rgb)
