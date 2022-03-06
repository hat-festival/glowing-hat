import json

from lib.redis_manager import RedisManager


class Mode:
    """Superclass for `modes`."""

    def __init__(self, hat):
        """Construct."""
        self.hat = hat
        self.redisman = RedisManager()
        self.register()

    def register(self):
        """Register ourself with Redis."""
        self.redisman.lpush(
            "modes",
            json.dumps({"class": type(self).__name__, "display-name": self.name}),
        )
