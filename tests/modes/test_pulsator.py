from unittest import TestCase

from lib.modes.pulsator import Throbber


class TestThrobber(TestCase):
    """Test the throbber."""

    def test_easy(self):
        """Test the stupid case."""
        throb = Throbber(0, 4)
        self.assertEqual(list(throb), [0, 0.5, 1, 0.5])

    def test_with_seed(self):
        """Test the seeded case."""
        throb = Throbber(0.5, 4)
        self.assertEqual(list(throb), [0.5, 1, 0.5, 0])

    def test_with_more_steps(self):
        """Test the more-steps case."""
        throb = Throbber(0, 16)
        self.assertEqual(
            list(throb),
            [
                0.0,
                0.038,
                0.146,
                0.309,
                0.5,
                0.691,
                0.854,
                0.962,
                1.0,
                0.962,
                0.854,
                0.691,
                0.5,
                0.309,
                0.146,
                0.038,
            ],
        )

    def test_iterator(self):
        """Test it gives values."""
        throb = Throbber(0, 4)
        self.assertEqual(list(throb), [0, 0.5, 1, 0.5])

        results = []
        for _ in range(8):
            results.append(throb.next())

        self.assertEqual(results, [0.0, 0.5, 1.0, 0.5, 0.0, 0.5, 1.0, 0.5])
