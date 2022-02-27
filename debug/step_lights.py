import time

from lib.hat import Hat

hat = Hat()
from lib.conf import conf

hat.off()

colour = [0, 255, 0]
for i in range(conf["lights"]):
    print(i)
    hat.light_one(i, colour)
    time.sleep(0.5)
