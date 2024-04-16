from lib.modes.breather import Breather
from lib.modes.crawler import Crawler
from lib.modes.equaliser import Equaliser
from lib.modes.larsen import Larsen
from lib.modes.pulsator import Pulsator
from lib.modes.roller import Roller
from lib.modes.sweeper import Sweeper

modes = {
    "sweeper": Sweeper,
    "breather": Breather,
    "crawler": Crawler,
    "equaliser": Equaliser,
    "larsen": Larsen,
    "pulsator": Pulsator,
    "roller": Roller,
}


def load_modes(custodian):
    """Load the modes into the Custodian."""
    custodian.unset("hoop:mode")
    for mode in modes:
        custodian.add_item_to_hoop(mode, "mode")
