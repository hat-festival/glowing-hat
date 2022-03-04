import signal
import sys
from multiprocessing import Process

from RPi import GPIO

from lib.colour_stepper import ColourStepper
from lib.colour_wheel import ColourWheel
from lib.redis_manager import RedisManager

PINS = {
    "run_wheel": 17,
    "step_stepper": 23,
    "bump_mode": 25,
}


class HatManager:
    """Class to manage modes and colours."""

    def __init__(self, namespace="hat"):
        """Construct."""
        self.redisman = RedisManager(namespace)

        self.wheel = ColourWheel(namespace=namespace)
        self.stepper = ColourStepper(namespace=namespace)

        self.processes = {"colour-wheel": None}

    def run_wheel(self, _):
        """Run the ColourWheel."""
        if not self.processes["colour-wheel"]:
            self.processes["colour-wheel"] = Process(target=self.wheel.rotate)

        if not self.processes["colour-wheel"].is_alive():
            self.processes["colour-wheel"].start()
            self.redisman.enter("wheel", "rotating")

    def step_stepper(self, _):
        """Step to the next Single Colour."""
        # stop the ColourWheel, if it's running
        if self.processes["colour-wheel"]:
            if self.processes["colour-wheel"].is_alive():
                self.processes["colour-wheel"].terminate()
                self.processes["colour-wheel"] = None
                self.redisman.enter("wheel", "stationary")

        self.stepper.step()

    def bump_mode(self, _):
        """Step to the next mode."""
        current_mode = self.redisman.retrieve("mode")
        modes = self.redisman.range("modes")
        index = modes.index(current_mode)
        self.redisman.enter("mode", modes[(index + 1) % len(modes)])
        self.redisman.enter("break-mode", "true")

    def signal_handler(self, _, __):
        """Handle a Ctrl-C etc."""
        # kill the processes
        for _, process in self.processes.items():
            if process:
                if process.is_alive():
                    process.terminate()
                    process = None

        GPIO.cleanup()
        sys.exit(0)

    def manage(self):
        """Do the work."""
        GPIO.setmode(GPIO.BCM)

        for method, pin in PINS.items():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(
                pin,
                GPIO.FALLING,
                callback=getattr(self, method),
                bouncetime=500,
            )

        signal.signal(signal.SIGINT, self.signal_handler)
        signal.pause()


if __name__ == "__main__":
    hm = HatManager()
    hm.manage()
