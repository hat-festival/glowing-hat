import json
from pathlib import Path

import cv2

THRESHOLD = 250

axes = {
    "front": {"axis": "x", "direction": "positive"},
    "left": {"axis": "z", "direction": "negative"},
    "back": {"axis": "x", "direction": "negative"},
    "right": {"axis": "z", "direction": "positive"},
}

print("Looking for bright spots")
for aspect in ["back", "front", "left", "right"]:
    directory = Path("/opt", "hat-analysis", aspect)
    for file in directory.glob("*"):
        if file.suffix == ".jpg":
            image = cv2.imread(str(file))
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
            if maxVal > THRESHOLD:
                # other_axis = axes[aspect]["axis"]
                value = maxLoc[0]
                if axes[aspect]["direction"] == "negative":
                    value = 0 - value

                coords = {"y": maxLoc[1], axes[aspect]["axis"]: value}
                print(f"{aspect} {file.stem}: {coords}")
                Path(directory, f"{file.stem}.json").write_text(
                    json.dumps(coords), encoding="UTF-8"
                )
