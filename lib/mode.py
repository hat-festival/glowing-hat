import json
from pathlib import Path

import yaml

from lib.redis_manager import RedisManager


class Mode:
    """Superclass for `modes`."""

    def __init__(self, hat, name):
        """Construct."""
        self.hat = hat
        self.name = name
        try:
            self.conf = yaml.safe_load(
                Path("conf/modes.yaml").read_text(encoding="UTF-8")
            )[self.name]
        except KeyError:
            self.conf = {}

        self.redisman = RedisManager()
        self.register()

    def register(self):
        """Register ourself with Redis."""
        self.redisman.lpush(
            "modes",
            json.dumps({"class": type(self).__name__, "display-name": self.name}),
        )
