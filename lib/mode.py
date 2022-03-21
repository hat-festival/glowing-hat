import pickle
from pathlib import Path

from lib.conf import conf
from lib.redis_manager import RedisManager
import json

class Mode:
    """Superclass for `modes`."""

    def __init__(self, hat):
        """Construct."""
        self.hat = hat
        self.name = type(self).__name__.lower()
        self.conf = conf
        self.redisman = RedisManager()

        self.invert = False
        if self.redisman.get("invert") == "true":
            self.invert = True

        self.axis = self.redisman.get("axis")

    def get_colour(self):
        """Retrieve the colour from Redis."""
        colour = self.redisman.get("colour")
        if colour == "wheel":
            return self.redisman.get_colour()

        return json.loads(self.redisman.get("colour"))

    @property
    def frame_sets(self):
        """Load the frame data."""
        return pickle.loads(Path("renders", f"{self.name}.pickle").read_bytes())
