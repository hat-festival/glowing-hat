# pylint: skip-file

import time
from pathlib import Path

import yaml

from lib.hat import Hat
from lib.pixel import Pixel

# from random import randint


data = yaml.safe_load(Path("conf", "locations.yaml").read_text(encoding="UTF-8"))
import ipdb

ipdb.set_trace()
lights = []

for index, point in enumerate(data):
    lights.append(Pixel(index, point))

print(len(lights))

import ipdb

ipdb.set_trace()

red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
off = [0, 0, 0]

hat = Hat()
hat.off()
length = 0
while True:
    # colour = [randint(0, 127), randint(0, 127), randint(0, 127)]
    for colour in [off, red]:
        for i in range(0, 1000, 10):
            things = list(
                filter(
                    lambda x: x.less_than("x", ((i / 1000) * 720))
                    and x.less_than("y", ((i / 1000) * 480)),
                    lights,
                )
            )
            indeces = list(map(lambda x: x.index, things))
            if indeces:
                hat.colour_indeces(colour, indeces)
            print(i)
            time.sleep(1)
