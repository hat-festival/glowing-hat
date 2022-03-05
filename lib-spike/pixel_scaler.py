from pathlib import Path

import yaml


class PixelScaler:
    """Scale absolute HatSpace values to relatively-scaled values."""

    def __init__(self, locations="conf/locations.yaml"):
        """Construct."""
        self.locations = locations
        self.absolutes = yaml.safe_load(Path(locations).read_text(encoding="UTF-8"))


def limits(data):
    """Find the mins and maxes."""
    ldata = {"x": {}, "y": {}, "z": {}}

    for axis in ["x", "y", "z"]:
        ldata[axis]["max"] = float(max(filter(None, data[axis])))
        ldata[axis]["min"] = float(min(filter(None, data[axis])))

    return ldata


def scale(items, centre, factor=1):
    """Scale some items."""
    shifted = list(map(lambda x: x - min(items), items))
    multiplier = (2 / max(shifted)) * factor
    normalised = list(map(lambda x: x * multiplier, shifted))
    centred = list(map(lambda x: x - factor, normalised))

    return centred


def split(items, centre):
    """Split a list about the centre."""
    splits = {
        "bigger": [],
        "littler": [],
    }

    for item in items:
        if item >= centre:
            splits["bigger"].append(item)

        if item < centre:
            splits["littler"].append(item)

    return splits
