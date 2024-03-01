from unittest import TestCase

from lib.sorters.cube_sorter import CubeSorter


class TestCubeSorter(TestCase):
    """Test the CubeSorter."""

    def setUp(self):
        """Set things up."""
        self.sorter = CubeSorter(locations="tests/fixtures/hat/locations/simple.yaml")

    def test_sorting(self):
        """Try the sorter."""
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
            assert just_the_indeces(self.sorter.sort_from(point)) == ordering


def just_the_indeces(pixel_list):
    """Get just the indeces of the pixels."""
    return [x["index"] for x in pixel_list]
