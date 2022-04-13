from lib.modes.bands import Bands
from lib.modes.brain_waves import BrainWaves
from lib.modes.cuttlefish import Cuttlefish
from lib.modes.larsen import Larsen
from lib.modes.pulsator import Pulsator
from lib.modes.rotator import Rotator

# we pre-instantiate all the modes and hold on to them
modes = {
    "cuttlefish": Cuttlefish,
    "brainwaves": BrainWaves,
    "pulsator": Pulsator,
    "bands": Bands,
    "rotator": Rotator,
    "larsen": Larsen,
}


def load_modes(custodian):
    """Load the modes into the Custodian."""
    custodian.unset("hoop:mode")
    for mode in modes:
        custodian.add_item_to_hoop(mode, "mode")
