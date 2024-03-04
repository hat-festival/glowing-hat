from time import sleep

from lib.conf import conf
from lib.tools import is_pi

if is_pi():  # nocov
    from RPi import GPIO
else:
    import tests.fake_gpio as GPIO  # noqa: N812
import threading


class Rotator:
    """A rotary encoder."""

    def __init__(self, normaliser):
        """Construct."""
        self.normaliser = normaliser

    def rotate(self):
        """Run the rotary-encoder."""
        # https://forums.raspberrypi.com/viewtopic.php?p=929475&sid=ec5d74aaef7cf66029a48b04cbe1a1e1#p929475
        self.clk = conf["rotary"]["pins"]["clk"]
        self.dt = conf["rotary"]["pins"]["dt"]
        self.sw = conf["rotary"]["pins"]["sw"]

        self.current_clk = 1
        self.current_dt = 1
        self.lock_rotary = threading.Lock()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.clk, GPIO.IN)
        GPIO.setup(self.dt, GPIO.IN)
        GPIO.setup(self.sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self.clk, GPIO.RISING, callback=self.rotary_interrupt)
        GPIO.add_event_detect(self.dt, GPIO.RISING, callback=self.rotary_interrupt)

        sw_last_state = GPIO.input(self.sw)

        while True:
            new_sw_state = GPIO.input(self.sw)
            if new_sw_state != sw_last_state and new_sw_state == 0:
                self.normaliser.set_fft_state(not self.normaliser.doing_fft.value)

            sw_last_state = new_sw_state

            sleep(0.01)

    def rotary_interrupt(self, pin):
        """Rotary interrupt."""
        switch_clk = GPIO.input(self.clk)
        switch_dt = GPIO.input(self.dt)

        if self.current_clk == switch_clk and self.current_dt == switch_dt:
            return

        self.current_clk = switch_clk
        self.current_dt = switch_dt

        if switch_clk and switch_dt:
            self.lock_rotary.acquire()
            if pin == self.dt:
                self.normaliser.adjust_brightness("up")
            else:
                self.normaliser.adjust_brightness("down")
            self.lock_rotary.release()
