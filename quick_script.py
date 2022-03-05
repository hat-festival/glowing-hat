from lib.hat import Hat
from lib.pixel_hat import PixelHat
from lib.redis_manager import RedisManager

rm = RedisManager()
hat = PixelHat()
hat.off()

axes = ["x", "y", "z"]
divisions = 50

while True:
    for axis in axes:
        colour = rm.fetch_colour()
        for i in [x / divisions for x in range(-divisions, divisions, 1)]:
            things = list(
                filter(
                    lambda x: x.less_than(axis, i),
                    hat,
                )
            )
            indeces = list(map(lambda x: x["index"], things))
            hat.colour_indeces(indeces, colour)
