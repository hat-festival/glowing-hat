from pathlib import Path
from unittest import TestCase

import pytest

from lib.sorters.axis_manager import AxisManager


@pytest.mark.not_ci()
class TestAxisManager(TestCase):
    """Test the AxisManager."""

    def setUp(self):
        """Do some setup."""
        Path("tmp").mkdir(exist_ok=True)

    def test_archive_creation(self):
        """Test it creates an archive of `sorts`."""
        man = AxisManager(
            locations="tests/fixtures/hat/locations/simple.yaml",
            archive_path="tmp",
        )
        man.create_sorts(steps=2)

        assert len(man.sorts.keys()) == 125  # noqa: PLR2004
        assert man.sorts["sorts:(1.0, 0.0, -0.5)"] == (4, 3, 0, 1, 2)

        assert Path("tmp", "sorts-1x1.json.gz").exists()
        assert not Path("tmp", "sorts-1x1.json").exists()

    def test_populating_redis(self):
        """Test it saves the data."""
        man = AxisManager(
            locations="tests/fixtures/hat/locations/simple.yaml",
            archive_path="tmp",
        )
        man.create_sorts(steps=2)
        man.populate()

        assert man.get_sort((-0.5, -1.0, 0.5)) == (
            2,
            1,
            4,
            3,
            0,
        )
