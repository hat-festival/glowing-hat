# pylint: skip-file


import sys

from lib.hat import Hat

index = int(sys.argv[1])

red = [255, 0, 0]

hat = Hat()
hat.off()
hat.light_one(index, red)
