from lib.modes.brain_waves import BrainWaves
from lib.modes.crawler import Crawler
from lib.modes.equaliser import Equaliser
from lib.modes.larsen import Larsen
from lib.modes.pulsator import Pulsator
from lib.modes.roller import Roller
from lib.modes.spots import Spots
from lib.modes.sweeper import Sweeper

modes = {
    "spots": Spots,
    "sweeper": Sweeper,
    "crawler": Crawler,
    "pulsator": Pulsator,
    "brainwaves": BrainWaves,
    "equaliser": Equaliser,
    "larsen": Larsen,
    "roller": Roller,
}


def load_modes(custodian):
    """Load the modes into the Custodian."""
    custodian.unset("hoop:mode")
    for mode in modes:
        custodian.add_item_to_hoop(mode, "mode")
