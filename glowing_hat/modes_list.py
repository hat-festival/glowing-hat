from glowing_hat.conf import conf
from glowing_hat.modes.address import Address
from glowing_hat.modes.binary_clock import Clock
from glowing_hat.modes.breather import Breather
from glowing_hat.modes.crawler import Crawler
from glowing_hat.modes.equaliser import Equaliser
from glowing_hat.modes.invaders import Invaders
from glowing_hat.modes.larsen import Larsen
from glowing_hat.modes.pulsator import Pulsator
from glowing_hat.modes.rainbow import Rainbow
from glowing_hat.modes.roller import Roller
from glowing_hat.modes.solid import Solid
from glowing_hat.modes.sweeper import Sweeper
from glowing_hat.modes.tapper import Tapper
from glowing_hat.modes.tilter import Tilter
from glowing_hat.modes.words import Words

lookups = {
    "address": Address,
    "breather": Breather,
    "clock": Clock,
    "crawler": Crawler,
    "equaliser": Equaliser,
    "invaders": Invaders,
    "larsen": Larsen,
    "pulsator": Pulsator,
    "rainbow": Rainbow,
    "roller": Roller,
    "solid": Solid,
    "sweeper": Sweeper,
    "tapper": Tapper,
    "tilter": Tilter,
    "words": Words,
}


modes = {}
for key in list(conf["modes"].keys()):
    modes[key] = lookups[key]


def load_modes(custodian):
    """Load the modes into the Custodian."""
    custodian.unset("hoop:mode")
    for mode in modes:
        custodian.add_item_to_hoop(mode, "mode")
