from unittest import TestCase

from glowing_hat.sorters.cube_sorter import CubeSorter


class TestCubeSorter(TestCase):
    """Test the CubeSorter."""

    def setUp(self):
        """Set things up."""
        self.sorter = CubeSorter(locations="tests/fixtures/hat/locations/simple.yaml")

    def test_sorting(self):
        """Try the sorter."""
        expectations = (
            ((-1, 0, 0), (2, 1, 0, 3, 4)),
            ((0, -1, 0), (4, 3, 2, 1, 0)),
            ((-1, -1, -1), (2, 3, 0, 4, 1)),
            ((1, 1, 1), (1, 4, 0, 3, 2)),
        )

        for location, indeces in expectations:
            assert self.sorter.sort_from(*location) == indeces

    def test_sorting_a_bigger_cube(self):
        """Test we can sort for a bigger cube."""
        # we can go arbitrarily large but it breaks these orderings
        assert self.sorter.sort_from(0, -2, 0) == (4, 3, 2, 1, 0)
