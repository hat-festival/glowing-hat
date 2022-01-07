import json
import time
from random import randint
from time import sleep

import redis

from lib.hat import Hat
from lib.tools import gamma_correct

redis = redis.Redis()
hat = Hat()
redis.set("mode", "blend")
redis.set("colour", "[255, 0, 0]")
redis.set("chase-index", 0)


def flash(interval=1):
    """Flash the lights on and off with a single colour."""
    colour = json.loads(redis.get("colour"))
    hat.light_all(gamma_correct(colour))
    sleep(interval)
    hat.light_all([0, 0, 0])
    sleep(interval)


def blend(interval=1):
    """Recolour the lights every `interval` seconds."""
    colour = json.loads(redis.get("colour"))
    hat.light_all(colour)
    sleep(interval)


def chase(interval=1):
    """Chase a colour up the string."""
    colour = json.loads(redis.get("colour"))
    hat.light_all([0, 0, 0])
    index = int(redis.get("chase-index").decode())
    hat.light_one(index, colour)
    redis.set("chase-index", ((index + 1) % 50))
    sleep(0.01)


def random(interval=1):
    colour = json.loads(redis.get("colour"))
    hat.light_all([0, 0, 0])
    hat.light_one(randint(0, 49), colour)
    sleep(0.01)


if __name__ == "__main__":
    mode = redis.get("mode").decode()
    chase_index = 0
    while True:
        globals()[mode](0.1)
        mode = redis.get("mode").decode()
