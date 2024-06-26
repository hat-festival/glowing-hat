# pylint: skip-file
# pyflakes: noqa

import sys
from pathlib import Path

import yaml
from hat import Hat

from glowing_hat.pixel import Pixel

axis = sys.argv[1]
value = int(sys.argv[2])

data = yaml.safe_load(Path("..", "conf", "locations.yaml").read_text(encoding="UTF-8"))

lights = []
for index, point in enumerate(data["lights"]):  # noqa: B007
    lights.append(Pixel(point))

red = [255, 0, 0]

hat = Hat()
hat.off()

indeces = []
print(f"Lighting for {axis} less than {value}")
for light in lights:
    if light.less_than(axis, value):
        indeces.append(light["index"])  # noqa: PERF401

hat.colour_indeces(indeces, red)
