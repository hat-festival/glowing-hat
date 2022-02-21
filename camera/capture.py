# pylint: skip-file

import json
import sys
from pathlib import Path
from time import sleep

import requests
from picamera import PiCamera

from conf import conf

hat = f"http://{sys.argv[1]}:{conf['webserver-port']}"
aspect = sys.argv[2]

root_dir = Path("/home", "pi", "analysis", aspect)
Path.mkdir(root_dir, parents=True, exist_ok=True)

camera = PiCamera()
camera.resolution = (2592, 1944)
camera.awb_mode = "off"
# camera.shutter_speed = 2000

input("Align hat and hit return when ready...")


def make_outdir(colour):
    """Make an outdir."""
    # odir = Path(root_dir, "-".join(map(lambda x: str(x).zfill(3), colour)))
    odir = root_dir
    Path.mkdir(odir, parents=True, exist_ok=True)

    return odir


def snap(index, colour, shutter_speed=2000, suffix=''):
    """Take a picture of light `i` with colour `colour`."""
    print(f"Capturing light {index} with colour {colour} at shutter-speed {shutter_speed}")

    outdir = make_outdir(colour)

    requests.post(
        f"{hat}/light",
        data=json.dumps({"index": index, "colour": colour}),
        headers={"Content-Type": "application/json"},
    )
    sleep(0.5)
    camera.shutter_speed = 2000
    camera.capture(f"{str(outdir)}/{str(index).zfill(3)}{suffix}.jpg")
    sleep(0.5)


# colour = [0, 0, 0]
# for j in range(25, 255, 50):
#     for i in range(3):
#         colour[i] = j

colour = [255, 0, 0]
for index in range(conf["lights"]):
    snap(index, colour)
    snap(index, [255, 255, 255], 1000000, "-long")

    # if index in  [52, 54, 77, 91, 96]:


requests.post(
    f"{hat}/light-all",
    data=json.dumps({"colour": colour}),
    headers={"Content-Type": "application/json"},
)
sleep(1)
camera.capture(f"{str(make_outdir(colour))}/all.jpg")
sleep(1)
