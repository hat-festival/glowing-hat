from multiprocessing import Value
from time import sleep

from RPi import GPIO

from lib.conf import conf


class RotatingScaler:
    """Scales colours with a rotary-encoder."""

    def __init__(self, normaliser):
        """Construct."""
        self.normaliser = normaliser
        self.normaliser.factor = Value("f", self.normaliser.default_brightness)
        self.step_size = 0.02
        self.conf = conf["rotary"]

        self.clk = self.conf["pins"]["clk"]
        self.dt = self.conf["pins"]["dt"]
        self.sw = self.conf["pins"]["sw"]

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def run(self):
        """Do the work."""
        clk_last_state = GPIO.input(self.clk)
        sw_last_state = GPIO.input(self.sw)
        on = True

        while True:
            clk_state = GPIO.input(self.clk)
            dt_state = GPIO.input(self.dt)

            if clk_state != clk_last_state:
                if dt_state != clk_state:
                    self.normaliser.factor.value = min(
                        self.normaliser.factor.value + self.step_size,
                        self.max_brightness,
                    )
                else:
                    self.normaliser.factor.value = max(
                        self.normaliser.factor.value - self.step_size, 0.005
                    )
            clk_last_state = clk_state

            new_sw_state = GPIO.input(self.sw)
            if new_sw_state != sw_last_state:
                if new_sw_state == 0:
                    if on:
                        on = False
                        self.normaliser.factor.value = 0
                    else:
                        on = True
                        self.normaliser.factor.value = (
                            self.normaliser.default_brightness
                        )

                sw_last_state = new_sw_state
            sleep(0.001)
