from lib.modes.brain_waves import BrainWaves
from lib.modes.crawler import Crawler
from lib.modes.equaliser import Equaliser
from lib.modes.larsen import Larsen
from lib.modes.pulsator import Pulsator
from lib.modes.roller import Roller
from lib.modes.sweeper import Sweeper

modes = {
    "roller": Roller,
    "equaliser": Equaliser,
    "pulsator": Pulsator,
    # "sweeper": Sweeper,
    # "larsen": Larsen,
    # "crawler": Crawler,
    # "brainwaves": BrainWaves,
}


def load_modes(custodian):
    """Load the modes into the Custodian."""
    custodian.unset("hoop:mode")
    for mode in modes:
        custodian.add_item_to_hoop(mode, "mode")
