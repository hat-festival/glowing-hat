import io
import pickle
import tarfile
from pathlib import Path

from redis import Redis

from lib.logger import logging
from lib.sort_key import SortKey
from lib.sorters.cube_sorter import CubeSorter


class AxisManager:
    """Manage the pre-rendered hat orderings."""

    def __init__(
        self, archive_path="sorts", locations="conf/locations.yaml", cube_radius=1
    ):
        """Construct."""
        self.archive_path = archive_path
        self.cube_radius = cube_radius
        self.archive = Path(archive_path, f"sorts-{cube_radius}x{cube_radius}.tar.gz")
        self.sorter = CubeSorter(locations)
        self.redis = Redis()

    def populate(self):
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
                    point = tuple(
                        round(a * self.cube_radius / steps, 1) for a in (x, y, z)
                    )
                    filename = str(point)
                    logging.debug("sorting from `%s`", point)
                    pkl = pickle.dumps(self.sorter.sort_from(*point))
                    info = tarfile.TarInfo(name=filename)
                    info.size = len(pkl)
                    tar.addfile(info, io.BytesIO(pkl))

        tar.close()

    def get_sort(self, key):
        """Unpickle a `sort`."""
        if type(key).__name__ == "tuple":
            key = SortKey(key).as_key
        return pickle.loads(self.redis.get(key))  # noqa: S301

    # TODO: this should be the default, the rest is redundant
    def get_sort_indeces(self, key):
        """Get just the indeces from a sort."""
        return tuple(x["index"] for x in self.get_sort(key))
