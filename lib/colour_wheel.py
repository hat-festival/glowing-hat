from time import sleep

from lib.custodian import Custodian


class ColourWheel:
    """Spin the `hue` wheel round and round."""

    def __init__(self, interval=0.01, namespace="hat"):
        """Construct."""
        self.interval = interval
        self.custodian = Custodian(namespace=namespace)

    @property
    def start_hue(self):
        """Get the initial hue."""
        hue = self.custodian.get("hue")
        if not hue:
            self.custodian.set("hue", 0)

        return float(self.custodian.get("hue"))

    def rotate(self, testing=False, steps=250):
        """Spin the wheel."""
        offset = self.start_hue

        if testing:
            self.interval = 0

        while True:
            for i in range(steps):
                hue = ((i / steps) + offset) % 1
                self.custodian.set("hue", hue)
                sleep(self.interval)

            if testing:
                break
