# http://docs.pimoroni.com/buttonshim/#module-buttonshim

from signal import pause

import buttonshim

from lib.conf import conf

FUNCTIONS = {}

for index, data in enumerate(conf["shimbuttons"]):
    FUNCTIONS[index] = data
    FUNCTIONS[index]["held"] = False


BUTTONS = [
    buttonshim.BUTTON_A,
    buttonshim.BUTTON_B,
    buttonshim.BUTTON_C,
    buttonshim.BUTTON_D,
    buttonshim.BUTTON_E,
]


class Controller:
    """Fake controller."""

    def bump_axis(self):
        """Bump axis."""
        print("bumping axis")

    def bump_invert(self):
        """Bump invert."""
        print("bumping invert")

    def bump_colour(self):
        """Bump colour."""
        print("bumping colour")

    def bump_mode(self):
        """Bump mode."""
        print("bumping mode")

    def bump_colour_source(self):
        """Bump colour-source."""
        print("bumping colour source")

    def bump_colour_set(self):
        """Bump colour-set."""
        print("bumping colour set")


c = Controller()


@buttonshim.on_release(BUTTONS)
def release_handler(button, _):
    """Handle button release."""
    if not FUNCTIONS[button]["held"]:
        getattr(c, f"bump_{FUNCTIONS[button]['press']}")()

    else:
        FUNCTIONS[button]["held"] = False

    buttonshim.set_pixel(0, 0, 0)


@buttonshim.on_hold(BUTTONS, hold_time=1)
def held_handler(button):
    """Handle button hold."""
    buttonshim.set_pixel(255, 0, 0)
    if "hold" in FUNCTIONS[button]:
        getattr(c, f"bump_{FUNCTIONS[button]['hold']}")()
        FUNCTIONS[button]["held"] = True


def manage():
    """Loop forever."""
    pause()


if __name__ == "__main__":
    manage()
