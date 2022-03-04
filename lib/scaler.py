from pathlib import Path

import yaml


class Scaler:
    """Pixel scaler thing."""

    def __init__(self, locations="conf/locations.yaml"):
        """Construct."""
        self.locations = locations
        self.absolutes = yaml.safe_load(Path(locations).read_text(encoding="UTF-8"))

        self.scaled = [
            {"index": 0, "x": -1, "y": -1, "z": -1},
            {"index": 1, "x": -0.5, "y": -0.5, "z": -0.5},
            {"index": 2, "x": 0, "y": 0, "z": 0},
            {"index": 3, "x": 0.5, "y": 0.5, "z": 0.5},
            {"index": 4, "x": 1, "y": 1, "z": 1},
        ]
