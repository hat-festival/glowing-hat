import platform
from unittest.mock import patch

from glowing_hat.conf import HatConf


def test_populating():
    """Test it takes a `conf_root`."""
    hc = HatConf(conf_root="tests/fixtures/conf/just-conf")
    assert hc == {"lights": 100, "data-pin": 21, "random-hue": {"distance": 0.3}}


def test_merging():
    """Test it can combine some conf."""
    with patch.object(platform, "node", return_value="test-hat"):
        hc = HatConf(conf_root="tests/fixtures/conf/with-overrides")
        assert hc == {"lights": 50, "data-pin": 22, "random-hue": {"distance": 0.3}}
