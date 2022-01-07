import json

import redis

redis = redis.Redis()
from time import sleep

from lib.tools import hue_to_grb

interval = 0.01

while True:
    for i in range(1000):
        redis.set("colour", json.dumps(hue_to_grb(i / 1000)))
        sleep(interval)
