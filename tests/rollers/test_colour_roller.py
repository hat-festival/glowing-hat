from unittest import TestCase

from lib.rollers.set_roller import SetRoller


class TestSetRoller(TestCase):
    """Test the SetRoller."""

    def test_rolling(self):
        """Test it rolls."""
        roller = SetRoller("test", {"red": [255, 0, 0], "blue": [0, 0, 255]})

        results = []
        for _ in range(3):
            results.append(roller.next)

        self.assertEqual(results, [[255, 0, 0], [0, 0, 255], [255, 0, 0]])
