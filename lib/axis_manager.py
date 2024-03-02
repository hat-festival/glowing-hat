import io
import pickle
import tarfile
from pathlib import Path

from redis import Redis

from lib.logger import logging
from lib.sorters.cube_sorter import CubeSorter


class AxisManager:
    """Manage the pre-rendered hat orderings."""

    def __init__(
        self, archive="sorts/sorts-1x1.tar.gz", locations="conf/locations.yaml"
    ):
        """Construct."""
        self.archive = archive
        self.sorter = CubeSorter(locations)
        self.redis = Redis()

    def populate_redis(self):
        """Send the sorts data to redis."""
        if not self.redis.get("sorts:(1.0, 1.0, 1.0)"):
            tar = tarfile.open(self.archive, "r")
            for member in tar:
                if not member.isfile():
                    continue

                key = f"sorts:{member.name}"
                logging.debug("loading sort-key `%s`", key)
                self.redis.set(key, tar.extractfile(member).read())

    def create_sorts(self, steps=20):
        """Create the sorts archive."""
        Path("sorts").mkdir(exist_ok=True)
        tar = tarfile.open(self.archive, "w:gz")
        r = range(-steps, steps + 1, 1)

        for x in r:
            for y in r:
                for z in r:
                    point = (x / steps, y / steps, z / steps)
                    filename = str(point)
                    logging.debug("sorting from `%s`", point)
                    pkl = pickle.dumps(self.sorter.sort_from(*point))
                    info = tarfile.TarInfo(name=filename)
                    info.size = len(pkl)
                    tar.addfile(info, io.BytesIO(pkl))

        tar.close()

    def get_sort(self, key):
        """Unpickle a `sort`."""
        return pickle.loads(self.redis.get(key))  # noqa: S301
