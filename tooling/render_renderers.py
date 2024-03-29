from lib.renderers.larsen import Larsen
from lib.renderers.pulsator import Pulsator
from lib.renderers.rotator import Rotator
from lib.renderers.sweeper import Sweeper

for renderer in [Larsen, Rotator, Pulsator, Sweeper]:
    r = renderer()
    r.render()
