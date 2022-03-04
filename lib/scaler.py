from pathlib import Path
from posixpath import abspath

import yaml


class Scaler:
    """Pixel scaler thing."""

    def __init__(self, locations="conf/locations.yaml"):
        """Construct."""
        self.locations = locations
        self.absolutes = yaml.safe_load(Path(locations).read_text(encoding="UTF-8"))

        magic_number = find_largest_span(self.absolutes)
        self.scaled = []
        for light in self.absolutes["lights"]:
            scaled_light = {"index": light["index"]}
            for axis in ["x", "y", "z"]:
                scaled_light[axis] = (light[axis] - magic_number) / magic_number
            self.scaled.append(scaled_light)


def find_largest_span(absolutes):
    """Find the largest step from the centre, given some lists."""
    largest = 0
    centres = absolutes["centres"]
    deconstructed = deconstruct(absolutes["lights"])

    for axis in ["x", "y", "z"]:
        centre = centres[axis]
        for value in deconstructed[axis]:
            if value >= centre:
                if value - centre > largest:
                    largest = value - centre

            else:
                if centre - value > largest:
                    largest = centre - value

    return largest


def deconstruct(absolutes):
    """Pull the data to pieces."""
    deconstructed = {}

    for axis in ["x", "y", "z"]:
        deconstructed[axis] = list(map(lambda w: w[axis], absolutes))

    return deconstructed
