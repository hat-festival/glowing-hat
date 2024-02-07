import datetime
from random import random
from time import sleep

from lib.custodian import Custodian

cust = Custodian("test")


def pause():
    sleep(0.3 + random() / 10)


while True:
    cust.set("low", datetime.datetime.now().timestamp())
    pause()
    pause()
    cust.set("high", datetime.datetime.now().timestamp())
    pause()
    cust.set("mid", datetime.datetime.now().timestamp())
    pause()
    cust.set("low", datetime.datetime.now().timestamp())
    pause()
    cust.set("low", datetime.datetime.now().timestamp())
    pause()
    cust.set("high", datetime.datetime.now().timestamp())
    pause()
    cust.set("low", datetime.datetime.now().timestamp())
    pause()
