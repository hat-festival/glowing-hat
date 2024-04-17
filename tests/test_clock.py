from datetime import datetime

from lib.modes.binary_clock import bin_string_to_values, binary_hms


def test_easy_binary_hms():
    """Test we get the binary pieces for the HMS."""
    timestamp = datetime.strptime("00:00:00", "%H:%M:%S")  # noqa: DTZ007
    assert binary_hms(timestamp) == {
        "hours": "00000",
        "minutes": "000000",
        "seconds": "000000",
    }


def test_richer_binary_hms():
    """Test we get the pieces for a richer HMS."""
    timestamp = datetime.strptime("12:34:56", "%H:%M:%S")  # noqa: DTZ007
    assert binary_hms(timestamp) == {
        "hours": "01100",
        "minutes": "100010",
        "seconds": "111000",
    }


def test_bin_string_to_values():
    """Test converting a binary-string to some values."""
    assert bin_string_to_values("0") == [0.0]
    assert bin_string_to_values("00") == [0.0, 0.0]
    assert bin_string_to_values("010") == [0.0, 1.0, 0.0]
    assert bin_string_to_values("0101") == [0.0, 1.0, 0.0, 1.0]
