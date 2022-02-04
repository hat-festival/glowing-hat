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

input("Align hat and press any key when ready...")

camera.capture(f"{outdir}/reference.jpg")

for i in range(conf["lights"]):
    print(f"Capturing light {i}")
    requests.post(
        f"{hat}/light",
        data=json.dumps({"index": i}),
        headers={"Content-Type": "application/json"},
    )
    sleep(0.5)
    camera.capture(f"{outdir}/{i:0>2}.jpg")
    sleep(0.5)
