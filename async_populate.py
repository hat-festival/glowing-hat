import datetime
from random import random
from time import sleep

from lib.custodian import Custodian

cust = Custodian(namespace="hat")


def pause():
    sleep(0.2)


while True:
    cust.set("mid", datetime.datetime.now().timestamp())
    pause()
    pause()
    pause()
    pause()
    cust.set("high", datetime.datetime.now().timestamp())
    pause()
    pause()
    pause()
    pause()
    cust.set("low", datetime.datetime.now().timestamp())
    pause()
    pause()
    pause()
    pause()
    cust.set("high", datetime.datetime.now().timestamp())
    pause()
    pause()
    pause()
    pause()
