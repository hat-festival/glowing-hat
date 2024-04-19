from glowing_hat.renderers.larsen import Larsen
from glowing_hat.renderers.pulsator import Pulsator
from glowing_hat.renderers.rotator import Rotator
from glowing_hat.renderers.sweeper import Sweeper

for renderer in [Larsen, Rotator, Pulsator, Sweeper]:
    r = renderer()
    r.render()
