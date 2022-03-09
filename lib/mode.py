from lib.conf import conf
from lib.redis_manager import RedisManager


class Mode:
    """Superclass for `modes`."""

    def __init__(self, hat, name):
        """Construct."""
        self.hat = hat
        self.name = name
        self.conf = conf
        self.redisman = RedisManager()

        self.invert = False
        if self.redisman.get("invert") == "true":
            self.invert = True

        self.axis = self.redisman.get("axis")

    def get_colour(self):
        """Retrieve the colour from Redis."""
        colour = self.redisman.get("colour")
        if colour == "free":
            return self.redisman.get_colour()

        return self.conf["colours"][colour]
