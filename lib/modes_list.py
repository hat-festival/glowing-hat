from lib.modes.bands import Bands
from lib.modes.bigtop import BigTop
from lib.modes.brain_waves import BrainWaves
from lib.modes.cuttlefish import Cuttlefish
from lib.modes.larsen import Larsen
from lib.modes.pulsator import Pulsator
from lib.modes.sweeper import Sweeper

modes = {
    "cuttlefish": Cuttlefish,
    "sweeper": Sweeper,
    "pulsator": Pulsator,
    "brainwaves": BrainWaves,
    "bigtop": BigTop,
    "bands": Bands,
    "larsen": Larsen,
}


def load_modes(custodian):
    """Load the modes into the Custodian."""
    custodian.unset("hoop:mode")
    for mode in modes:
        custodian.add_item_to_hoop(mode, "mode")
