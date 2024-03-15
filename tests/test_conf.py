import pytest

from lib.conf import conf


@pytest.mark.skip()
def test_default_prefs():
    """Test `modes` get the default prefs."""
    assert conf["modes"]["subtleroller"] == {
        "fft": True,
        "length-multiplier": 3,
        "roll-sorter-at": 7,
        "prefs": {"axis": "none", "invert": False},
    }
