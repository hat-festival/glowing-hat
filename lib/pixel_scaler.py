from pathlib import Path

import yaml


class PixelScaler:
    """Scale absolute HatSpace values to relatively-scaled values."""

    def __init__(self, locations="conf/locations.yaml"):
        """Construct."""
        self.locations = locations
        self.absolutes = yaml.safe_load(Path(locations).read_text(encoding="UTF-8"))
