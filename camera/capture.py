import json
import sys
from pathlib import Path
from time import sleep

import requests
from picamera import PiCamera

HAT = "http://hatlights.local:5001"
camera = PiCamera()
aspect = sys.argv[1]

outdir = Path("/home", "pi", "hat-analysis", aspect)
Path.mkdir(outdir, parents=True, exist_ok=True)

requests.post(
     f"{HAT}/light-all", headers={"Content-Type": "application/json"}
)

input("Align hat and press any key when ready...")

sleep(1)
print(f"Capturing reference image")
camera.capture(f"{outdir}/reference.jpg")
sleep(1)

for i in range(50):
    print(f"Capturing light {i}")
    requests.post(
        f"{HAT}/light", data=json.dumps({"index": i}), headers={"Content-Type": "application/json"}
    )
    sleep(1)
    camera.capture(f"{outdir}/{i:0>2}.jpg")
    sleep(1)
