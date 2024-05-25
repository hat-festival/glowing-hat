from glowing_hat.tools.sin_looper import SinLooper, number_scaler


def test_defaults():
    """Test default behaviour."""
    sl = SinLooper()

    results = [next(sl) for _ in range(10)]
    assert results == [
        0.5,
        0.7938926261462366,
        0.9755282581475768,
        0.9755282581475768,
        0.7938926261462367,
        0.5000000000000001,
        0.2061073738537635,
        0.024471741852423234,
        0.02447174185242318,
        0.20610737385376332,
    ]


def test_scaled():
    """Test it takes some scaling."""
    sl = SinLooper(low=0, high=4)

    results = [next(sl) for _ in range(10)]
    assert results == [
        2.0,
        3.1755705045849463,
        3.9021130325903073,
        3.9021130325903073,
        3.1755705045849467,
        2.0000000000000004,
        0.824429495415054,
        0.09788696740969294,
        0.09788696740969272,
        0.8244294954150533,
    ]


def test_number_scaler():
    """Test we can scale numbers."""
    assert number_scaler(0, 2, 0) == 1
    assert number_scaler(0, 4, 0) == 2  # noqa: PLR2004
    assert number_scaler(0.1, 8.1, -0.5) == 2.1  # noqa: PLR2004
    assert number_scaler(10, 20, 0) == 15  # noqa: PLR2004
