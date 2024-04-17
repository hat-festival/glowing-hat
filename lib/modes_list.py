from lib.conf import conf
from lib.modes.binary_clock import Clock
from lib.modes.breather import Breather
from lib.modes.crawler import Crawler
from lib.modes.equaliser import Equaliser
from lib.modes.larsen import Larsen
from lib.modes.pulsator import Pulsator
from lib.modes.rainbow import Rainbow
from lib.modes.roller import Roller
from lib.modes.sweeper import Sweeper

lookups = {
    "breather": Breather,
    "clock": Clock,
    "crawler": Crawler,
    "equaliser": Equaliser,
    "larsen": Larsen,
    "pulsator": Pulsator,
    "rainbow": Rainbow,
    "roller": Roller,
    "sweeper": Sweeper,
}


modes = {}
for key in list(conf["modes"].keys()):
    modes[key] = lookups[key]


def load_modes(custodian):
    """Load the modes into the Custodian."""
    custodian.unset("hoop:mode")
    for mode in modes:
        custodian.add_item_to_hoop(mode, "mode")
