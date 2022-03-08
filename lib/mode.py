import json
from pathlib import Path

import yaml

from lib.conf import conf
from lib.redis_manager import RedisManager


class Mode:
    """Superclass for `modes`."""

    def __init__(self, hat, name):
        """Construct."""
        self.hat = hat
        self.name = name
        self.conf = conf
        try:
            self.mode_conf = yaml.safe_load(
                Path("conf/modes.yaml").read_text(encoding="UTF-8")
            )[self.name]
        except KeyError:
            self.mode_conf = {}

        self.redisman = RedisManager()
        self.register()

    def register(self):
        """Register ourself with Redis."""
        self.redisman.lpush(
            "modes",
            json.dumps({"class": type(self).__name__, "display-name": self.name}),
        )

    def get_colour(self):
        """Retrieve the colour from Redis."""
        colour = self.redisman.get("colour")
        if colour == "free":
            return self.redisman.get_colour()

        return self.conf["colours"][colour]
