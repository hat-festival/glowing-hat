from collections import deque
from random import shuffle

from lib.hue_sources.random_hue_source import RandomHueSource


def boot_hat(custodian, oled, hat):
    """Boot the hat."""
    custodian.set("display-type", "boot")
    oled.update()

    hue_source = RandomHueSource()
    for i in range(10, 3, -1):
        populate_hat(hat, hue=hue_source.hue(), value=i / 10)

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
