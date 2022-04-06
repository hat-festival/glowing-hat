from lib.modes.bands import Bands
from lib.modes.brain_waves import BrainWaves
from lib.modes.cuttlefish import Cuttlefish
from lib.modes.larsen import Larsen
from lib.modes.pulsator import Pulsator
from lib.modes.quarters import Quarters
from lib.modes.rotator import Rotator

modes = {
    "cuttlefish": Cuttlefish,
    "brainwaves": BrainWaves,
    "pulsator": Pulsator,
    "bands": Bands,
    "rotator": Rotator,
    "larsen": Larsen,
    "quarters": Quarters,
}


def load_modes(custodian):
    """Load the modes into the Custodian."""
    custodian.unset("hoop:mode")
    for mode in modes:
        custodian.add_item_to_hoop(mode, "mode")
