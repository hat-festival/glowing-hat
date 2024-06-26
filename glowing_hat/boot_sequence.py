import os
from collections import deque
from random import shuffle

from glowing_hat.button_bindings import colour_from_hue, off
from glowing_hat.hue_sources.time_based_hue_source import TimeBasedHueSource


def boot_hat(custodian, oled, hat):
    """Boot the hat."""
    custodian.set("display-type", "boot")
    oled.update()

    if "LOGLEVEL" not in os.environ:
        hue_source = TimeBasedHueSource(seconds_per_rotation=5)
        for i in range(10, 3, -2):
            hue = hue_source.hue()
            colour_from_hue(hue)
            populate_hat(hat, hue=hue, value=i / 10)

        off()

    custodian.set("display-type", "show-mode")
    oled.update()


def populate_hat(hat, hue, value=1.0):
    """Populate all the pixels with a `hue`."""
    indeces = deque(list(range(len(hat))))
    while len(indeces):
        shuffle(indeces)
        victim = indeces.pop()
        pix = hat.pixels[victim]
        pix["hue"] = hue
        pix["value"] = value
        hat.light_one(pix)
        hat.show()
