# pylint: skip-file
# flake8: noqa

from pathlib import Path

import yaml

from hat import Hat
from lib.pixel import Pixel

data = yaml.safe_load(Path("..", "conf", "locations.yaml").read_text(encoding="UTF-8"))

lights = []

for index, point in enumerate(data["lights"]):
    lights.append(Pixel(point))

red = [127, 0, 0]
green = [0, 127, 0]
blue = [0, 0, 127]
off = [0, 0, 0]

axes = ["x", "y", "z"]

hat = Hat()
hat.off()
length = 0
while True:
    for index, colour in enumerate([red, green, blue]):
        for i in range(0, 2592, 30):
            things = list(
                filter(
                    lambda x: x.less_than("x", i),
                    # lambda x: x.less_than("z", i),
                    # lambda x: x.less_than("y", i),
                    lights,
                )
            )
            indeces = list(map(lambda x: x["index"], things))
            if indeces:
                hat.colour_indeces(indeces, colour)
            # time.sleep(0.05)
