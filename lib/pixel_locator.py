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

    # @property
    # def consolidated_data(self):
    #     """Pull together the disparate data."""
    #     pjson = self.parsed_json
    #     cdata = {
    #         "x": [None] * 20,
    #         "y": [None] * 20,
    #         "z": [None] * 20,
    #     }
    #     for i in range(self.lights):
    #         key = str(i).zfill(3)
    #         for aspect in ASPECTS:
    #             if key in pjson[aspect]:
    #                 y_val = pjson[aspect][key]["y"]
    #                 if cdata["y"][i]:
    #                     cdata["y"][i] = [cdata["y"][i]]
    #                     cdata["y"][i].append(y_val)
    #                 else:
    #                     cdata["y"][i] = y_val

    #                 other_value = pjson[aspect][key]["x"]
    #                 if AXES[aspect]["direction"] == "negative":
    #                     other_value = self.picwidth - other_value

    #                 axis = AXES[aspect]["axis"]
    #                 if cdata[axis][i]:
    #                     cdata[axis][i] = [cdata[axis][i]]
    #                     cdata[axis][i].append(other_value)
    #                 else:
    #                     cdata[axis][i] = other_value

    #     return cdata

    @property
    def flattened_data(self):
        """Average-out the data."""
        cdata = self.consolidated_data
        fdata = {"x": [], "y": [], "z": []}
        for axis, values in cdata.items():
            for value in values:
                fdata[axis].append(average_out(value))

        return fdata

    @property
    def limits(self):
        """Find the mins and maxes."""
        fdata = self.flattened_data
        ldata = {"x": {}, "y": {}, "z": {}}

        for axis in ["x", "y", "z"]:
            ldata[axis]["max"] = float(max(filter(None, fdata[axis])))
            ldata[axis]["min"] = float(min(filter(None, fdata[axis])))

        return ldata

    # write YAML

    # @property
    # def scaled(self):
    #     """Scale the points.

    #     (-1, 1) along the shortest distance, the rest scaled accordingly
    #     """
    #     scale_to = 1


def scale(items, factor=1):
    """Scale some items."""
    shifted = list(map(lambda x: x - min(items), items))
    multiplier = (2 / max(shifted)) * factor
    normalised = list(map(lambda x: x * multiplier, shifted))
    centred = list(map(lambda x: x - factor, normalised))

    return centred


def average_out(items):
    """Find the mean value of a list."""
    if isinstance(items, list):
        return float(sum(items) / len(items))

    return float(items)


def collect_json(json_path):
    """Gather up the JSON files."""
    data = {}
    for aspect in ASPECTS:
        data[aspect] = {}
        directory = Path(json_path, aspect)
        data_files = Path(directory).glob("*[0-9]*json")
        for file in data_files:
            data[aspect][file.stem] = json.loads(file.read_text(encoding="UTF-8"))

    return data


def consolidate(parsed_data, pic_width=720):
    """Pull together the disparate data."""
    width = find_highest_key(parsed_data) + 1
    cdata = {
        "x": [None] * width,
        "y": [None] * width,
        "z": [None] * width,
    }

    for i in range(width):
        key = str(i).zfill(3)
        for aspect in ASPECTS:
            if aspect in parsed_data:
                if key in parsed_data[aspect]:
                    add_item(cdata["y"], i, parsed_data[aspect][key]["y"])

                    other_val = parsed_data[aspect][key]["x"]
                    if AXES[aspect]["direction"] == "negative":
                        other_val = pic_width - other_val

                    add_item(cdata[AXES[aspect]["axis"]], i, other_val)

    return cdata


def add_item(items, index, new_item):
    """Add an item to a list _or_ create a list at that index."""
    if items[index]:
        items[index] = [items[index]]
        items[index].append(new_item)
    else:
        items[index] = new_item


def find_highest_key(data):
    """Find the highest key."""
    highest = 0
    for key, values in data.items():
        for sub_key, _ in values.items():
            val = int(sub_key)
            if val > highest:
                highest = val

    return highest

def flatten_list(wonky_list):
    """Flatten a list (averaging any possible sublists)."""
    return list(map(lambda x: average_out(x), wonky_list))
