import json
from pathlib import Path

import cv2

print("Looking for bright spots")
directory = Path("/opt", "calibration")
for file in directory.glob("*"):
    image = cv2.imread(str(file))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    coords = {"x": maxLoc[0], "y": maxLoc[1]}
    print(f"{file.stem}: {coords}")
    # Path(directory, f"{file.stem}.json").write_text(
    #     json.dumps(coords), encoding="UTF-8"
    # )
