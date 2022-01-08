import signal
import sys
import multiprocessing
from time import sleep

import RPi.GPIO as GPIO
wheel_thread = None


def do_wheel():
    count = 0
    while True:
        print(f"wheel {count}")
        count += 1
        sleep(0.5)

def my_callback(channel):
    print("falling edge detected on 17")
    global wheel_thread
    if not wheel_thread:
        wheel_thread = multiprocessing.Process(target=do_wheel,)

    if not wheel_thread.is_alive():
        wheel_thread.start()


def my_callback2(channel):
    print("falling edge detected on 23")
    global wheel_thread
    if wheel_thread:
        if wheel_thread.is_alive():
            wheel_thread.terminate()
            wheel_thread = None


def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(17, GPIO.FALLING, callback=my_callback, bouncetime=300)
    GPIO.add_event_detect(23, GPIO.FALLING, callback=my_callback2, bouncetime=300)

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
