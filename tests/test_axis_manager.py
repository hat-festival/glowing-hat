import hashlib
import pickle
import tarfile
from unittest import TestCase

from redis import Redis

from lib.axis_manager import AxisManager


class TestAxisManager(TestCase):
    """Test the AxisManager."""

    def setUp(self):
        """Do some setup."""
        self.redis = Redis()
        self.redis.flushall()

    def test_archive_creation(self):
        """Test it creates an archive of `sorts`."""
        man = AxisManager(
            locations="tests/fixtures/hat/locations/simple.yaml",
            archive="/tmp/sorts.tar.gz",  # noqa: S108
        )
        man.create_sorts(steps=2)

        result = tarfile.open("/tmp/sorts.tar.gz", "r")  # noqa: S108
        specimen = pickle.loads(result.extractfile("(1.0, 0.0, -0.5)").read())  # noqa: S301
        assert tuple(x["index"] for x in specimen) == (4, 3, 0, 1, 2)

    def test_populating_redis(self):
        """Test it saves the data."""
        man = AxisManager(
            locations="tests/fixtures/hat/locations/simple.yaml",
            archive="/tmp/sorts.tar.gz",  # noqa: S108
        )
        man.create_sorts(steps=2)
        man.populate_redis()

        assert (
            hashlib.sha256(self.redis.get("sorts:(-0.5, -1.0, 0.5)")).hexdigest()
            == "9ede5937c278f4d826b70295cfa845e01b288cc93820a69ec802aee7099d033f"
        )

    def test_sort_from(self):
        """Test it sorts good."""
        man = AxisManager(locations="tests/fixtures/hat/locations/simple.yaml")
        expectations = (
            # straight line from left to right
            ((-1, 0, 0), [2, 1, 0, 3, 4]),
            # bottom to top
            ((0, -1, 0), [4, 3, 2, 1, 0]),
            # left back bottom corner
            ((-1, -1, -1), [2, 3, 0, 4, 1]),
            # right front top corner
            ((1, 1, 1), [1, 4, 0, 3, 2]),
        )

        for point, ordering in expectations:
            assert just_the_indeces(man.sort_from(point)) == ordering


def just_the_indeces(pixel_list):
    """Get just the indeces of the pixels."""
    return [x["index"] for x in pixel_list]
