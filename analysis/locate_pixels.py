# pylint: skip-file

import json
from collections import OrderedDict
from pathlib import Path

import yaml

from conf import conf

PICWIDTH = 2592  # GET THIS FROM THE IMAGES

axes = {
    "front": {"axis": "x", "direction": "positive", "data": {}},
    "left": {"axis": "z", "direction": "negative", "data": {}},
    "back": {"axis": "x", "direction": "negative", "data": {}},
    "right": {"axis": "z", "direction": "positive", "data": {}},
}

lights = OrderedDict()

# gather the data
for aspect in ["back", "front", "left", "right"]:
    directory = Path("/opt", "analysis", aspect)
    data_files = Path(directory).glob("*[0-9]*json")
    for file in data_files:
        axes[aspect]["data"][file.stem] = json.loads(file.read_text(encoding="UTF-8"))

# assemble a dict like
#
# {'00': {'x': [347], 'y': [391, 340], 'z': [93]}, '01': {'x': [544], 'y': [177, 220], 'z': [59]}}  # noqa: E501
#
# etc

for i in range(conf["lights"]):
    key = str(i).zfill(3)
    lights[key] = {"x": [], "y": [], "z": []}
    for aspect, stuff in axes.items():
        if key in stuff["data"]:
            lights[key]["y"].append(stuff["data"][key]["y"])
            del stuff["data"][key]["y"]

            for k, v in stuff["data"][key].items():  # noqa: B007, PERF102
                if axes[aspect]["direction"] == "negative":
                    v = PICWIDTH - v  # noqa: PLW2901

                lights[key][stuff["axis"]].append(v)

# take a mean of the value lists
final_lights = {"lights": [], "centres": {}}
index = 0
for key, points in lights.items():
    final_lights["lights"].append({"index": index})
    for axis, values in points.items():
        if values:
            final_lights["lights"][int(key)][axis] = sum(values) / len(values)
    index += 1  # noqa: SIM113

Path("..", "conf", "locations.yaml").write_text(
    yaml.dump(final_lights), encoding="UTF-8"
)

# front / back: 337
