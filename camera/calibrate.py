import json
import sys
from pathlib import Path
from time import sleep

import requests
from picamera import PiCamera

from conf import conf

hat = f"http://{sys.argv[1]}:{conf['webserver-port']}"

outdir = Path("/home", "pi", "calibration")
Path.mkdir(outdir, parents=True, exist_ok=True)
camera = PiCamera()
camera.resolution = (2592, 1944)
camera.awb_mode = "off"

requests.post(
    f"{hat}/light-all",
    data=json.dumps({"colour": [255, 0, 0]}),
    headers={"Content-Type": "application/json"},
)

for i in range(0, 1000, 10):
    camera.shutter_speed = i
    print(f"Shutter-speed: {i}")
    camera.capture(f"{outdir}/{str(i).zfill(4)}.jpg")
    sleep(1)

# for i in range(255):
#     print(f"Capturing at {i}")
#     requests.post(
#         f"{hat}/light",
#         data=json.dumps({"index": int(light), "colour": [i, 0, 0]}),
#         headers={"Content-Type": "application/json"},
#     )
#     sleep(1)
#     camera.capture(f"{outdir}/{str(i).zfill(3)}.jpg")
#     sleep(1)
