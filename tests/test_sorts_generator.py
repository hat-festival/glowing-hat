from lib.sorters.sorts_generator import SortsGenerator


class TestSortsGenerator:
    """Test the SortsGenerator."""

    def test_live_axes(self):
        """Test it knows which axes are in play."""
        generator = SortsGenerator("z", "x")
        assert generator.live_indeces == [2, 0]

    def test_start_corner(self):
        """Test it works out the starting corner."""
        generator = SortsGenerator("z", "x")
        assert generator.start_corner.tuple == (-1.0, 0.0, -1.0)

    def test_simple_circle(self):
        """Test going round in a circle."""
        generator = SortsGenerator("z", "x", interval=1)
        generator.make_circle()
        assert generator.as_tuples == [
            (-1.0, 0.0, -1.0),  # back left
            (-1.0, 0.0, 0.0),
            (-1.0, 0.0, 1.0),  # front left
            (0.0, 0.0, 1.0),
            (1.0, 0.0, 1.0),  # front right
            (1.0, 0.0, 0.0),
            (1.0, 0.0, -1.0),  # back right
            (0.0, 0.0, -1.0),
        ]

    def test_richer_circle(self):
        """Test going round in a denser circle."""
        generator = SortsGenerator("z", "x", interval=0.5)
        generator.make_circle()
        assert generator.as_keys == [
            "sorts:(-1.0, 0.0, -1.0)",  # back left
            "sorts:(-1.0, 0.0, -0.5)",
            "sorts:(-1.0, 0.0, 0.0)",
            "sorts:(-1.0, 0.0, 0.5)",
            "sorts:(-1.0, 0.0, 1.0)",  # front left
            "sorts:(-0.5, 0.0, 1.0)",
            "sorts:(0.0, 0.0, 1.0)",
            "sorts:(0.5, 0.0, 1.0)",
            "sorts:(1.0, 0.0, 1.0)",  # front right
            "sorts:(1.0, 0.0, 0.5)",
            "sorts:(1.0, 0.0, 0.0)",
            "sorts:(1.0, 0.0, -0.5)",
            "sorts:(1.0, 0.0, -1.0)",  # back right
            "sorts:(0.5, 0.0, -1.0)",
            "sorts:(0.0, 0.0, -1.0)",
            "sorts:(-0.5, 0.0, -1.0)",
        ]

    def test_reverse_circle(self):
        """Test going round in a circle the other way."""
        generator = SortsGenerator("z", "x", interval=1)
        generator.make_circle(direction="backwards")
        assert generator.as_keys == [
            "sorts:(-1.0, 0.0, -1.0)",
            "sorts:(0.0, 0.0, -1.0)",
            "sorts:(1.0, 0.0, -1.0)",
            "sorts:(1.0, 0.0, 0.0)",
            "sorts:(1.0, 0.0, 1.0)",
            "sorts:(0.0, 0.0, 1.0)",
            "sorts:(-1.0, 0.0, 1.0)",
            "sorts:(-1.0, 0.0, 0.0)",
        ]

    def test_y_z_circle(self):
        """Test going round in a circle."""
        generator = SortsGenerator("y", "z", interval=1)
        generator.make_circle()
        assert generator.as_keys == [
            "sorts:(0.0, -1.0, -1.0)",
            "sorts:(0.0, 0.0, -1.0)",
            "sorts:(0.0, 1.0, -1.0)",
            "sorts:(0.0, 1.0, 0.0)",
            "sorts:(0.0, 1.0, 1.0)",
            "sorts:(0.0, 0.0, 1.0)",
            "sorts:(0.0, -1.0, 1.0)",
            "sorts:(0.0, -1.0, 0.0)",
        ]

    def test_with_altitude(self):
        """Test a circle with altitude."""
        generator = SortsGenerator("y", "z", interval=1)
        generator.make_circle(altitude=0.5)
        assert generator.as_keys == [
            "sorts:(0.5, -1.0, -1.0)",
            "sorts:(0.5, 0.0, -1.0)",
            "sorts:(0.5, 1.0, -1.0)",
            "sorts:(0.5, 1.0, 0.0)",
            "sorts:(0.5, 1.0, 1.0)",
            "sorts:(0.5, 0.0, 1.0)",
            "sorts:(0.5, -1.0, 1.0)",
            "sorts:(0.5, -1.0, 0.0)",
        ]
