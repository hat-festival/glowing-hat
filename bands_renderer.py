import pickle
from collections import deque
from pathlib import Path

from lib.pixel_hat import PixelHat
from lib.renderers.bands import Band

hat = PixelHat(auto_centre=True)
bands = {"data": []}  # this needs a total_length

count = 4
steps = 100
width = 0.5
rotation = steps * (width / 2)

prime = Band(width, "y", "down", steps=steps, hat=hat)


for i in range(count):
    # foo = deque(prime.copy())
    # foo.rotate(int(rotation * i))
    bands["data"].append(deque(prime.copy()))
    bands["data"][-1].rotate(int(rotation * i))
    bands["data"][-1] = list(bands["data"][-1])

bands["total-length"] = int(rotation * count)

Path("renders/bands.pickle").write_bytes(pickle.dumps(bands))
