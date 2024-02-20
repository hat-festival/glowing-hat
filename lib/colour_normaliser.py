from multiprocessing import Process, Value
from time import sleep

from RPi import GPIO

from lib.conf import conf
from lib.custodian import Custodian
from lib.gamma import gamma


class ColourNormaliser:
    """Normalises colours."""

    def __init__(self):
        """Construct."""
        self.custodian = Custodian("hat")
        self.max_brightness = conf["max-brightness"]
        self.default_brightness = self.max_brightness / 2
        self.factor = Value("f", self.default_brightness)
        self.step_size = 0.02

        self.set_up_rotary()

    def normalise(self, triple):
        """Normalise a colour."""
        return tuple(int(x * self.factor.value) for x in gamma_correct(triple))

    def set_up_rotary(self):
        """Configure the rotary encoder."""
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
        norm_proc = Process(target=self.loop)
        norm_proc.start()

    def loop(self):
        """Run forever."""
        clk_last_state = GPIO.input(self.clk)
        sw_last_state = GPIO.input(self.sw)
        on = True

        while True:
            clk_state = GPIO.input(self.clk)
            dt_state = GPIO.input(self.dt)

            if clk_state != clk_last_state:
                if dt_state != clk_state:
                    self.factor.value = min(
                        self.factor.value + self.step_size, self.max_brightness
                    )
                else:
                    self.factor.value = max(
                        self.factor.value - self.step_size, 0.005
                    )
            clk_last_state = clk_state

            new_sw_state = GPIO.input(self.sw)
            if new_sw_state != sw_last_state:
                if new_sw_state == 0:
                    if on:
                        on = False
                        self.factor.value = 0
                    else:
                        on = True
                        self.factor.value = self.default_brightness


                sw_last_state = new_sw_state
            sleep(0.001)


def gamma_correct(triple):
    """Gamma-correct a colour."""
    return tuple(map(lambda n: gamma[int(n)], triple))  # noqa: C417
