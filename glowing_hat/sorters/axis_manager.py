import gzip
import json
import platform
import shutil
from pathlib import Path
from random import randint

from redis import Redis

from glowing_hat.sorters.cube_sorter import CubeSorter
from glowing_hat.sorters.sort_key import SortKey
from glowing_hat.tools.logger import logging


class AxisManager:
    """Manage the pre-rendered hat orderings."""

    def __init__(self, archive_path="sorts", locations=None, cube_radius=1):
        """Construct."""
        self.archive_path = archive_path
        self.cube_radius = cube_radius
        self.archive = Path(archive_path, f"sorts-{cube_radius}x{cube_radius}.json.gz")

        if not locations:
            locations = f"conf/{platform.node()}/locations.yaml"
        self.sorter = CubeSorter(locations)
        self.redis = Redis()

    def populate(self):
        """Send the sorts data to redis."""
        if not self.redis.get("sorts:(1.0, 1.0, 1.0)"):
            archive = json.loads(gzip.open(self.archive).read().decode())
            for key, value in archive.items():
                logging.debug("loading sort-key `%s`", key)
                self.redis.set(key, str(value))

    def create_sorts(self, steps=20):
        """Create the sorts archive."""
        Path("sorts").mkdir(exist_ok=True)
        self.sorts = {}
        r = range(-steps, steps + 1, 1)

        for x in r:
            for y in r:
                for z in r:
                    point = tuple(
                        round(a * self.cube_radius / steps, 1) for a in (x, y, z)
                    )
                    logging.debug("sorting from `%s`", point)
                    self.sorts[SortKey(point).as_key] = self.sorter.sort_from(*point)

        temp_file = Path("/tmp", "foo.json")  # noqa: S108
        Path(temp_file).write_text(json.dumps(self.sorts))

        with (
            Path.open(temp_file, "rb") as f_in,
            gzip.open(self.archive, "wb") as f_out,
        ):
            shutil.copyfileobj(f_in, f_out)

        temp_file.unlink()

    def get_sort(self, key):
        """Unpickle a `sort`."""
        if type(key).__name__ == "tuple":
            key = SortKey(key).as_key
        return tuple(json.loads(self.redis.get(key).decode()))

    def get_random_sort(self):
        """Get a random `sort`."""
        origin = [self.random_position()] * 3

        # at least one point must be `1.0` or the sorts can be shorter than 100
        origin[randint(0, 2)] = 1.0  # noqa: S311
        return self.get_sort(tuple(origin))

    def random_position(self):
        """Get a random position."""
        return randint(-self.cube_radius * 10, self.cube_radius * 10) / 10  # noqa: S311
