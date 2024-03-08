import pytest

from lib.conf import conf
from lib.custodian import Custodian
from lib.hat import Hat
from lib.modes_list import modes

custodian = Custodian(namespace="test", conf=conf)
custodian.populate(flush=True)
hat = Hat()


@pytest.mark.skip(reason="breaking modes")
def test_conf_overlaps():
    """Test we only have the conf we need."""
    assert set(modes.keys()) == set(conf["modes"].keys())
