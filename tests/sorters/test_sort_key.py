from unittest import TestCase

from glowing_hat.sorters.sort_key import SortKey


class TestSortKey(TestCase):
    """Test the SortKey."""

    def test_with_list(self):
        """Construct with a list."""
        sk = SortKey([1, 2, 3])
        assert sk.tuple == (1, 2, 3)

    def test_with_tuple(self):
        """Construct with a tuple."""
        sk = SortKey((3, 2, 1))
        assert sk.tuple == (3, 2, 1)

    def test_with_splat(self):
        """Construct with free-floating objects."""
        sk = SortKey(4, 5, 6)
        assert sk.tuple == (4, 5, 6)

    def test_as_key(self):
        """Test it gives as a Redis key."""
        sk = SortKey(6, 5, 4)
        assert sk.as_key == "sorts:(6, 5, 4)"

    def test_copying(self):
        """Test it copies good."""
        sk = SortKey(1, 2, 3)
        sj = sk.clone()

        sj[0] = 5

        assert sk.tuple == (1, 2, 3)
        assert sj.tuple == (5, 2, 3)
