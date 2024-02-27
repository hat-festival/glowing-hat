from lib.space_solver import SpaceSolver


def test_easy_case():
    """Test the easy case."""
    point = (-1.0, -1.0, -1.0)
    solver = SpaceSolver(point, steps=1)

    assert solver.increments == (1.0, 1.0, 1.0)

    assert solver.states == [
        (-1.0, -1.0, -1.0),
        (0.0, 0.0, 0.0),
        (1.0, 1.0, 1.0),
    ]


def test_with_positives():
    """Test starting somewhere positive."""
    point = (1.0, -1.0, -1.0)
    solver = SpaceSolver(point, steps=1)

    assert solver.increments == (-1.0, 1.0, 1.0)

    assert solver.states == [
        (1.0, -1.0, -1.0),
        (0.0, 0.0, 0.0),
        (-1.0, 1.0, 1.0),
    ]
