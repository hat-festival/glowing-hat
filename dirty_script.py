# pylint: skip-file

import sys
import time
from pathlib import Path

import yaml

from lib.hat import Hat
from lib.pixel import Pixel

data = yaml.safe_load(Path("conf", "locations.yaml").read_text(encoding="UTF-8"))

lights = []

for index, point in enumerate(data):
    lights.append(Pixel(index, point))

red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
off = [0, 0, 0]

hat = Hat()
hat.off()
length = 0
while True:
    for colour in [red, green, blue]:
        for i in range(0, 2592, 10):
            things = list(
                filter(
                    lambda x: x.less_than("x", i) or x.less_than("z", i),
                    # lambda x: x.less_than("z", i),
                    # lambda x: x.less_than("y", i),
                    lights,
                )
            )
            indeces = list(map(lambda x: x.index, things))
            if indeces:
                hat.colour_indeces(colour, indeces)
            # time.sleep(0.05)
