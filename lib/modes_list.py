from lib.modes.equaliser import Equaliser
from lib.modes.pulsator import Pulsator
from lib.modes.roller import Roller

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
