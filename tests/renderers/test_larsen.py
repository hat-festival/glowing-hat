from unittest import TestCase

from lib.renderers.larsen import Larsen


class TestLarsen(TestCase):
    """Test Larsen."""

    def test_easy(self):
        """Test the noddiest case."""
        larsen = Larsen(2)

        larsen.populate()
        self.assertEqual(larsen, [[1], [1, 0.5]])
