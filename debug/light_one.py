# pylint: skip-file
# flake8: noqa

import sys

from glowing_hat.hat import Hat

index = int(sys.argv[1])

red = [255, 0, 0]

hat = Hat()
hat.off()
hat.light_one(index, red)
