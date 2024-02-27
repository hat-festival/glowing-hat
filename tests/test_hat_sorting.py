from unittest import TestCase
from unittest.mock import patch

from lib.conf import conf
from lib.hat import Hat


@patch.dict(conf, {"brightness-factor": 1.0})
class TestHat(TestCase):
    """Test the Hat."""

    def setUp(self):
        """Set things up."""
        self.simple_hat = Hat(
            locations="tests/fixtures/hat/locations/simple.yaml"
        )

    def test_simple_sort(self):
        """Try the simple sorts."""
        assert just_the_indeces(self.simple_hat) == [0, 1, 2, 3, 4]

        self.simple_hat.sort("x")
        assert just_the_indeces(self.simple_hat) == [2, 1, 0, 3, 4]

        self.simple_hat.sort("y")
        assert just_the_indeces(self.simple_hat) == [4, 3, 2, 1, 0]

        self.simple_hat.sort("z")
        assert just_the_indeces(self.simple_hat) == [3, 2, 0, 4, 1]

    def test_advanced_sorting(self):
        """Try the advanced sorter."""
        # straight line from left to right
        self.simple_hat.sort_from((0, 16, 16))
        assert just_the_indeces(self.simple_hat) == [2, 1, 0, 3, 4]


def just_the_indeces(hat):
    """Get just the indeces of the pixels."""
    return [x["index"] for x in hat.pixels]
