from unittest import TestCase

from lib.renderers.larsen import Larsen, middle_member


class TestLarsen(TestCase):
    """Test Larsen."""

    def test_two(self):
        """Test the noddiest case."""
        larsen = Larsen(2)

        larsen.populate()
        self.assertEqual(
            larsen,
            [
                [0, 1],
                [1, 0.5],
                [0.5, 0],
            ],
        )

    def test_four(self):
        """Test a slightly harder case."""
        larsen = Larsen(4)

        larsen.populate()
        self.assertEqual(
            larsen,
            [
                [0, 0, 0, 1],
                [0, 0, 1, 0.75],
                [0, 1, 0.75, 0.5],
                [1, 0.75, 0.5, 0.25],
                [0.75, 0.5, 0.25, 0],
                [0.5, 0.25, 0, 0],
                [0.25, 0, 0, 0],
            ],
        )


def test_middle_member():
    """Test it generates the middle-member correctly."""
    assert middle_member(2) == [1, 0.5]
    assert middle_member(8) == [1.0, 0.875, 0.75, 0.625, 0.5, 0.375, 0.25, 0.125]
