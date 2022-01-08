import signal
import sys
from multiprocessing import Process

import redis

# REMEMBER: check this as `from RPi import GPIO`
import RPi.GPIO as GPIO  # pylint:disable=R0402

from lib.colour_stepper import ColourStepper
from lib.colour_wheel import ColourWheel
from lib.tools import make_key

PINS = {"wheel": 17, "stepper": 23, "mode": 25}


class HatManager:
    """Class to manage modes and colours."""

    def __init__(self, namespace="hat"):
        """Construct."""
        self.namespace = namespace
        self.redis = redis.Redis()

        self.wheel = ColourWheel(namespace=self.namespace)
        self.stepper = ColourStepper(namespace=self.namespace)

        self.processes = {"colour-wheel": None}

    def run_wheel(self, _):
        """Run the ColourWheel."""
        if not self.processes["colour-wheel"]:
            self.processes["colour-wheel"] = Process(target=self.wheel.rotate)

        if not self.processes["colour-wheel"].is_alive():
            self.processes["colour-wheel"].start()

    def step_stepper(self, _):
        """Step to the next Single Colour."""
        # stop the ColourWheel, if it's running
        if self.processes["colour-wheel"]:
            if self.processes["colour-wheel"].is_alive():
                self.processes["colour-wheel"].terminate()
                self.processes["colour-wheel"] = None

        self.stepper.step()

    def bump_mode(self, _):
        """Step to the next mode."""
        current_mode = self.redis.get(make_key("mode", self.namespace)).decode()
        modes = list(
            map(
                lambda x: x.decode(),
                self.redis.lrange(make_key("modes", self.namespace), 0, -1),
            )
        )
        index = modes.index(current_mode)
        self.redis.set(
            make_key("mode", self.namespace), modes[(index + 1) % len(modes)]
        )

    def signal_handler(self, _, __):
        """Handle a Ctrl-C etc."""
        # kill the threads here?
        GPIO.cleanup()
        sys.exit(0)

    def manage(self):
        """Do the work."""
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(PINS["wheel"], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(PINS["stepper"], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(PINS["mode"], GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(
            PINS["wheel"], GPIO.FALLING, callback=self.run_wheel, bouncetime=500
        )
        GPIO.add_event_detect(
            PINS["stepper"], GPIO.FALLING, callback=self.step_stepper, bouncetime=500
        )
        GPIO.add_event_detect(
            PINS["mode"], GPIO.FALLING, callback=self.bump_mode, bouncetime=500
        )

        signal.signal(signal.SIGINT, self.signal_handler)
        signal.pause()


if __name__ == "__main__":
    hm = HatManager()
    hm.manage()
