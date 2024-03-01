import io
import pickle
import tarfile

from redis import Redis

from lib.logger import logging
from lib.pixel import Pixel
from lib.scaler import Scaler


class AxisManager:
    """Manage the pre-rendered hat orderings."""

    def __init__(self, locations="conf/locations.yaml", archive="sorts.tar.gz"):
        """Construct."""
        self.locations = locations
        self.archive = archive
        self.redis = Redis()

        self.scaler = Scaler(locations, auto_centre=False)
        self.pixels = list(map(Pixel, self.scaler))

    def populate_redis(self):
        """Send the sorts data to redis."""
        tar = tarfile.open(self.archive, "r")

        for member in tar:
            if not member.isfile():
                continue

            key = f"sorts:{member.name}"
            self.redis.set(key, tar.extractfile(member).read())

    def create_sorts(self, steps=10):
        """Create the sorts archive."""
        tar = tarfile.open(self.archive, "w:gz")
        r = range(-steps, steps + 1, 1)

        for x in r:
            for y in r:
                for z in r:
                    point = (x / steps, y / steps, z / steps)
                    filename = str(point)
                    logging.debug("sorting from `%s`", point)
                    pkl = pickle.dumps(self.sort_from(point))
                    info = tarfile.TarInfo(name=filename)
                    info.size = len(pkl)
                    tar.addfile(info, io.BytesIO(pkl))

        tar.close()

    def sort_from(self, point):
        """Sort from a point."""
        arranged = []
        # body diagonal of a 2x2x2 cube is 2*sqrt(3)
        for r in range(0, 3500, 1):
            radius = r / 1000
            arranged += list(
                filter(
                    lambda pixel: is_inside_sphere(pixel, point, radius)
                    and pixel not in arranged,
                    self.pixels,
                )
            )

        return arranged


def is_inside_sphere(pixel, centre, radius):
    """Is this pixel inside this sphere."""
    # https://math.stackexchange.com/a/3118250
    return (
        (pixel["x"] - centre[0]) ** 2
        + (pixel["y"] - centre[1]) ** 2
        + (pixel["z"] - centre[2]) ** 2
    ) < radius**2
