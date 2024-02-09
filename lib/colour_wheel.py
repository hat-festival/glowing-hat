from time import sleep

from lib.conf import conf
from lib.custodian import Custodian


class ColourWheel:
    """Spin the `hue` wheel round and round."""

    def __init__(self, namespace="hat"):
        """Construct."""
        self.conf = conf
        self.interval = self.conf["wheel"]["interval"]
        self.steps = self.conf["wheel"]["steps"]
        self.custodian = Custodian(namespace=namespace)

    @property
    def start_hue(self):
        """Get the initial hue."""
        hue = self.custodian.get("hue")
        if not hue:
            self.custodian.set("hue", 0)

        return float(self.custodian.get("hue"))

    def rotate(self, testing=False):  # noqa: FBT002
        """Spin the wheel."""
        offset = self.start_hue

        if testing:
            self.interval = 0

        while True:
            for i in range(self.steps):
                hue = ((i / self.steps) + offset) % 1
                self.custodian.set("hue", hue)
                sleep(self.interval)

            if testing:
                break
