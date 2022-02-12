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
<<<<<<< HEAD
            key = str(i).zfill(3)
=======
            key = str(i).zfill(2)
>>>>>>> 540f64d9bb82af8e33c99611998b287552349274
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

        return ndata

    @property
    def limits(self):
        """Find the mins and maxes."""
        ndata = self.normalised_data
        ldata = {}
        just_points = list(map(lambda a: a[1], ndata.items()))

        for axis in ["x", "y", "z"]:
            ldata[axis] = {}
            all_values = list(
                filter(
                    # pylint: disable=W0640
                    None,
                    map(lambda b: b.get(axis), just_points),
                )
            )

            ldata[axis]["max"] = max(all_values)
            ldata[axis]["min"] = min(all_values)

        return ldata

    # scale
    # write YAML


def average_out(items):
    """Find the mean value of a list."""
    return sum(items) / len(items)
