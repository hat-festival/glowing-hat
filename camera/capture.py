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

camera = PiCamera()

outdir = Path("/home", "pi", "hat-analysis", aspect)
Path.mkdir(outdir, parents=True, exist_ok=True)

try:
    requests.post(f"{hat}/light-all", headers={"Content-Type": "application/json"})

except requests.exceptions.ConnectionError:
    print(f"I don't think the webserver at {hat} is running")
    sys.exit(1)

print(f"Analysing {aspect} side of hat\n\n")

input("Hit return to start...")

camera.capture(f"{outdir}/reference.jpg")

for i in range(conf["lights"]):
    print(f"Capturing light {str(i).zfill(3)}")
    requests.post(
        f"{hat}/light",
        data=json.dumps({"index": i, "colour": [255, 255, 0]}),
        headers={"Content-Type": "application/json"},
    )
    sleep(1)
    camera.capture(f"{outdir}/{str(i).zfill(3)}.jpg")
    sleep(1)
