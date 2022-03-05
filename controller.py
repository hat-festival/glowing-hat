import signal
import sys
from multiprocessing import Process

from RPi import GPIO

from lib.modes.random import Random
from lib.modes.z_wave import ZWave
from lib.pixel_hat import PixelHat
from lib.redis_manager import RedisManager

class Controller:
    """Management class."""

    def __init__(self):
        """Construct."""
        self.hat = PixelHat()
        self.rm = RedisManager()
        self.mode_index = -1
        self.modes = [ZWave(self.hat), Random(self.hat)]

        self.process = None
        self.next_mode(None)

    def next_mode(self, _):
        if self.process and self.process.is_alive():
            self.process.terminate()

        self.mode_index = (self.mode_index + 1) % len(self.modes)
        mode = self.modes[self.mode_index]

        self.process = Process(target=mode.run)
        self.process.start()

        mode_name = type(mode).__name__
        print(f"Mode is now {mode_name}")
        self.rm.enter("mode", mode_name)

    def signal_handler(self, _, __):
        """Handle a Ctrl-C etc."""
        GPIO.cleanup()
        sys.exit(0)

    def manage(self):
        """Do the thing."""
        pin = 25  # from conf
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(
            pin,
            GPIO.FALLING,
            callback=self.next_mode,
            bouncetime=500,
        )
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.pause()


if __name__ == "__main__":
    con = Controller()
    con.manage()
