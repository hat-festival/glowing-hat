import datetime
from time import sleep

from lib.custodian import Custodian

cust = Custodian(namespace="hat")


def pause():
    """Sleep."""
    sleep(0.2)


while True:
    cust.set("mid", datetime.datetime.now(tz=datetime.UTC).timestamp())
    pause()
    pause()
    pause()
    pause()
    cust.set("high", datetime.datetime.now(tz=datetime.UTC).timestamp())
    pause()
    pause()
    pause()
    pause()
    cust.set("low", datetime.datetime.now(tz=datetime.UTC).timestamp())
    pause()
    pause()
    pause()
    pause()
    cust.set("high", datetime.datetime.now(tz=datetime.UTC).timestamp())
    pause()
    pause()
    pause()
    pause()
