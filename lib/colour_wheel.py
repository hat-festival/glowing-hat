from time import sleep

from lib.redis_manager import RedisManager


class ColourWheel:
    """Spin the `hue` wheel round and round."""

    def __init__(self, interval=0.01, namespace="hat"):
        """Construct."""
        self.interval = interval
        self.redisman = RedisManager(namespace)

    @property
    def start_hue(self):
        """Get the initial hue."""
        hue = self.redisman.get("hue")
        if not hue:
            self.redisman.set("hue", 0)

        return float(self.redisman.get("hue"))

    def rotate(self, testing=False, steps=1000):
        """Spin the wheel."""
        offset = self.start_hue

        if testing:
            self.interval = 0

        while True:
            for i in range(steps):
                hue = ((i / 1000) + offset) % 1
                self.redisman.set("hue", hue)
                sleep(self.interval)

            if testing:
                break
