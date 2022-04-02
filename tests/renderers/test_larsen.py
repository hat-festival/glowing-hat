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
                [0, 0, 1, 0.854],
                [0, 1, 0.854, 0.5],
                [1, 0.854, 0.5, 0.146],
                [0.854, 0.5, 0.146, 0],
                [0.5, 0.146, 0, 0],
                [0.146, 0, 0, 0],
            ],
        )


def test_middle_member():
    """Test it generates the middle-member correctly."""
    assert middle_member(2) == [1, 0.5]
    assert middle_member(4) == [1, 0.854, 0.5, 0.146]
    assert middle_member(8) == [1.0, 0.962, 0.854, 0.691, 0.5, 0.309, 0.146, 0.038]
