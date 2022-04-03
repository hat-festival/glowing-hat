import sys

from lib.modes_list import modes
from lib.pixel_hat import PixelHat

m = modes[sys.argv[1]](PixelHat())
m.run()
