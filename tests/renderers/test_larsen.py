from unittest import TestCase

from lib.renderers.larsen import Larsen, middle_member, range_finder


class TestLarsen(TestCase):
    """Test Larsen."""

    def test_two(self):
        """Test the noddiest case."""
        larsen = Larsen(2)

        larsen.populate()
        self.assertEqual(  # noqa: PT009
            larsen,
            [
                [0, 1],
                [1, 0.293],
                [0.293, 0],
            ],
        )

    def test_four(self):
        """Test a slightly harder case."""
        larsen = Larsen(4)

        larsen.populate()
        self.assertEqual(  # noqa: PT009
            larsen,
            [
                [0, 0, 0, 1],
                [0, 0, 1.0, 0.617],
                [0, 1, 0.617, 0.293],
                [1, 0.617, 0.293, 0.076],
                [0.617, 0.293, 0.076, 0],
                [0.293, 0.076, 0, 0],
                [0.076, 0, 0, 0],
            ],
        )


def test_middle_member():
    """Test it generates the middle-member correctly."""
    assert middle_member(2) == [1, 0.293]
    assert middle_member(4) == [1.0, 0.617, 0.293, 0.076]
    assert middle_member(8) == [
        1.0,
        0.805,
        0.617,
        0.444,
        0.293,
        0.169,
        0.076,
        0.019,
    ]


def test_range_finder():
    """Test it makes a good range."""
    assert range_finder(2) == [0.5, 0.75]
    assert range_finder(4) == [0.5, 0.625, 0.75, 0.875]
