# pylint: skip-file

import sys
import time
from pathlib import Path

import yaml

from lib.hat import Hat
from lib.pixel import Pixel

axis = sys.argv[1]
value = int(sys.argv[2])

data = yaml.safe_load(Path("..", "conf", "locations.yaml").read_text(encoding="UTF-8"))

lights = []
for index, point in enumerate(data):
    lights.append(Pixel(index, point))

red = [255, 0, 0]

hat = Hat()
hat.off()

indeces = []
print(f"Lighting for {axis} less than {value}")
for light in lights:
    if light.less_than(axis, value):
        indeces.append(light.index)

hat.colour_indeces(red, indeces)
