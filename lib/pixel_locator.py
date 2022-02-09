import json
from pathlib import Path

from lib.conf import conf

ASPECTS = ["back", "front", "left", "right"]

AXES = {
    "front": {"axis": "x", "direction": "positive"},
    "left": {"axis": "z", "direction": "negative"},
    "back": {"axis": "x", "direction": "negative"},
    "right": {"axis": "z", "direction": "positive"},
}


class PixelLocator:
    """Class to consolidate bright-pixel data."""

    def __init__(self, picdimensions, data_root="/opt/hat-analysis", lights=None):
        """Construct."""
        self.picwidth = picdimensions[0]
        self.picheight = picdimensions[1]
        self.data_root = data_root
        if not lights:
            self.lights = conf["lights"]
        else:
            self.lights = lights

        self.limits = {
            "x": {
                "max": 0,
                "min": 100000,
            },
            "y": {
                "max": 0,
                "min": 100000,
            },
            "z": {
                "max": 0,
                "min": 100000,
            },
        }

    @property
    def parsed_json(self):
        """Collect up the raw data."""
        pjson = {}
        for aspect in ASPECTS:
            pjson[aspect] = {}
            directory = Path(self.data_root, aspect)
            data_files = Path(directory).glob("*[0-9]*json")
            for file in data_files:
                pjson[aspect][file.stem] = json.loads(file.read_text(encoding="UTF-8"))

        return pjson

    @property
    def consolidated_data(self):
        """Pull together the disparate data."""
        pjson = self.parsed_json
        cdata = {}
        for i in range(self.lights):
            key = str(i).zfill(2)
            cdata[key] = {"x": [], "y": [], "z": []}

            for aspect in ASPECTS:
                if key in pjson[aspect]:
                    cdata[key]["y"].append(pjson[aspect][key]["y"])

                    other_value = pjson[aspect][key]["x"]
                    if AXES[aspect]["direction"] == "negative":
                        other_value = self.picwidth - other_value

                    cdata[key][AXES[aspect]["axis"]].append(other_value)

        return cdata

    @property
    def normalised_data(self):
        """Average-out the data."""
        cdata = self.consolidated_data
        ndata = {}
        for key, points in cdata.items():
            ndata[key] = {}
            for axis, values in points.items():
                if values:
                    average = average_out(values)
                    ndata[key][axis] = average

                    if average > self.limits[axis]["max"]:
                        self.limits[axis]["max"] = average

                    if average < self.limits[axis]["min"]:
                        self.limits[axis]["min"] = average

        return ndata

    # Scale (which means we need PICHEIGHT, too, I guess)
    # write YAML


def average_out(items):
    """Find the mean value of a list."""
    return sum(items) / len(items)
