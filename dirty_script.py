# pylint: skip-file

import time
from pathlib import Path

import yaml

from lib.hat import Hat
from lib.pixel import Pixel

# from random import randint


data = yaml.safe_load(Path("conf", "locations.yaml").read_text(encoding="UTF-8"))

lights = []

for index, point in enumerate(data):
    lights.append(Pixel(index, point))

print(len(lights))

red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
off = [0, 0, 0]

hat = Hat()
hat.off()
length = 0
while True:
    # colour = [randint(0, 127), randint(0, 127), randint(0, 127)]
    for colour in [red, off]:
        for i in range(720):
            things = list(
                filter(
                    lambda x: x.less_than("x", i),
                    lights,
                )
            )
            indeces = list(map(lambda x: x.index, things))
            if indeces:
                hat.colour_indeces(colour, indeces)
            # print(i)
            time.sleep(0.05)

# 2
# 15
# 31
# 54
# 56
# 76
# 96