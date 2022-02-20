import json
from pathlib import Path

import cv2

circles_dir = Path("/opt", "circles")
circles_dir.mkdir(exist_ok=True)

bottom_left = (10, 1920)
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 4
font_color = (255, 255, 255)
thickness = 4
lineType = 2
circle_size = 128

print("Circling bright spots")
for aspect in ["back", "front", "left", "right"]:

    Path(circles_dir, aspect).mkdir(exist_ok=True)
    for tag in ["good", "bad", "unclear"]:
        Path(circles_dir, aspect, tag).mkdir(exist_ok=True)

    directory = Path("/opt", "analysis", aspect)
    for file in directory.glob("*"):
        if file.suffix == ".jpg":
            print(f"Analysing {aspect} {file.stem}")
            image = cv2.imread(str(file))
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            (min_val, max_val, min_loc, max_loc) = cv2.minMaxLoc(gray)

            cv2.putText(
                image,
                str(max_val),
                bottom_left,
                font,
                font_scale,
                font_color,
                thickness,
                lineType,
            )

            cv2.circle(image, max_loc, circle_size, (255, 0, 0), 2)

            tag = "good"
            if 240 > max_val >= 75:
                tag = "unclear"
            if max_val < 75:
                tag = "bad"

            cv2.imwrite(f"/opt/circles/{aspect}/{file.stem}.jpg", image)
