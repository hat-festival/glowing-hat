import json
import sys
from pathlib import Path
from time import sleep

import requests
from picamera import PiCamera

HAT = "http://hatlights.local:5001/light"
camera = PiCamera()
aspect = sys.argv[1]

outdir = Path("/home", "pi", "hat-analysis", aspect)
Path.mkdir(outdir, parents=True, exist_ok=True)

for i in range(50):
    print(f"Capturing light {i}")
    requests.post(
        HAT, data=json.dumps({"index": i}), headers={"Content-Type": "application/json"}
    )
    sleep(1)
    camera.capture(f"{outdir}/{i:0>2}.jpg")
    sleep(1)
