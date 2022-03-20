from unittest import TestCase

from lib.colour_roller import ColourRoller


class TestColourRoller(TestCase):
    """Test the ColourRoller."""

    def test_rolling(self):
        """Test it rolls."""
        roller = ColourRoller({"red": [255, 0, 0], "blue": [0, 0, 255]})

        results = []
        for _ in range(3):
            results.append(roller.next)

        self.assertEqual(results, [[255, 0, 0], [0, 0, 255], [255, 0, 0]])
