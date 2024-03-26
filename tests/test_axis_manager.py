import hashlib
import pickle
import tarfile
from unittest import TestCase

import pytest
from redis import Redis

from lib.axis_manager import AxisManager


@pytest.mark.not_ci()
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
            archive_path="tmp",
        )
        man.create_sorts(steps=2)

        result = tarfile.open("tmp/sorts-1x1.tar.gz", "r")
        specimen = pickle.loads(result.extractfile("(1.0, 0.0, -0.5)").read())  # noqa: S301
        assert tuple(x["index"] for x in specimen) == (4, 3, 0, 1, 2)

    def test_populating_redis(self):
        """Test it saves the data."""
        man = AxisManager(
            locations="tests/fixtures/hat/locations/simple.yaml",
            archive_path="tmp",
        )
        man.create_sorts(steps=2)
        man.populate()
        assert (
            hashlib.sha256(self.redis.get("sorts:(-0.5, -1.0, 0.5)")).hexdigest()
            == "289c29690d0c54808a8f3f18fab3f899fd7789b95ed74ae182351f76088f2be3"
        )

        assert tuple(x["index"] for x in man.get_sort((-0.5, -1.0, 0.5))) == (
            2,
            1,
            4,
            3,
            0,
        )

    def test_a_bigger_cube(self):
        """Test it generates sorts for a larger cube."""
        man = AxisManager(
            locations="tests/fixtures/hat/locations/simple.yaml",
            archive_path="tmp",
            cube_radius=2,
        )
        man.create_sorts(steps=2)

        result = tarfile.open("tmp/sorts-2x2.tar.gz", "r")
        specimen = pickle.loads(result.extractfile("(2.0, 0.0, -1.0)").read())  # noqa: S301
        assert tuple(x["index"] for x in specimen) == (4, 3, 0, 1, 2)
