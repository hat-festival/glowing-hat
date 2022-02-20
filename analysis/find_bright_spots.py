import json
from pathlib import Path

import cv2

THRESHOLD = 130

source_dir = Path("/opt", "analysis")
# circles_dir = Path("/opt", "circles")

print("Looking for bright spots")
for aspect in ["back", "front", "left", "right"]:
    directory = Path(source_dir, aspect)
    for file in directory.glob("*"):
        if file.suffix == ".jpg":
            image = cv2.imread(str(Path(directory, f"{file.stem}.jpg")))
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)

            if maxVal > THRESHOLD:
                coords = {"x": maxLoc[0], "y": maxLoc[1]}
                # print(f"{aspect} {file.stem}: {coords}")
                Path(directory, f"{file.stem}.json").write_text(
                    json.dumps(coords), encoding="UTF-8"
                )
            else:
                print(f"{aspect} {file.stem}")
