from lib.modes.accelerator import Accelerator
from lib.modes.bigtop import BigTop
from lib.modes.brain_waves import BrainWaves
from lib.modes.crawler import Crawler
from lib.modes.cuttlefish import Cuttlefish
from lib.modes.larsen import Larsen
from lib.modes.music_bounce import MusicBounce
from lib.modes.pulsator import Pulsator
from lib.modes.sweeper import Sweeper

modes = {
    "cuttlefish": Cuttlefish,
    "musicbounce": MusicBounce,
    "pulsator": Pulsator,
    "accelerator": Accelerator,
    "larsen": Larsen,
    "bigtop": BigTop,
    "brainwaves": BrainWaves,
    "crawler": Crawler,
    "sweeper": Sweeper,
}


def load_modes(custodian):
    """Load the modes into the Custodian."""
    custodian.unset("hoop:mode")
    for mode in modes:
        custodian.add_item_to_hoop(mode, "mode")
