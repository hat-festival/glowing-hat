from lib.axis_rotator import AxisRotator


class TestAxisRotator:
    """Test the Rotator."""

    def test_live_axes(self):
        """Test it knows which axes are in play."""
        rotator = AxisRotator(("z", "x"))
        assert rotator.live_axes == [2, 0]

    def test_start_corner(self):
        """Test it works out the starting corner."""
        rotator = AxisRotator(("z", "x"))
        assert rotator.start_corner.tuple == (-1.0, 0.0, -1.0)

    def test_simple_circle(self):
        """Test going round in a circle."""
        rotator = AxisRotator(("z", "x"), interval=1)
        rotator.make_circle()
        assert rotator.as_tuples == [
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
        rotator = AxisRotator(("z", "x"), interval=0.5)
        rotator.make_circle()
        assert rotator.as_keys == [
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
        rotator = AxisRotator(("z", "x"), interval=1)
        rotator.make_circle(direction="backwards")
        assert rotator.as_keys == [
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
        rotator = AxisRotator(("y", "z"), interval=1)
        rotator.make_circle()
        assert rotator.as_keys == [
            "sorts:(0.0, -1.0, -1.0)",
            "sorts:(0.0, 0.0, -1.0)",
            "sorts:(0.0, 1.0, -1.0)",
            "sorts:(0.0, 1.0, 0.0)",
            "sorts:(0.0, 1.0, 1.0)",
            "sorts:(0.0, 0.0, 1.0)",
            "sorts:(0.0, -1.0, 1.0)",
            "sorts:(0.0, -1.0, 0.0)",
        ]
