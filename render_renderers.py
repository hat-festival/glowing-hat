from lib.renderers.larsen import Larsen
from lib.renderers.pulsator import Pulsator
from lib.renderers.rotator import Rotator

for renderer in [Larsen, Rotator, Pulsator]:
    r = renderer()
    r.render()
