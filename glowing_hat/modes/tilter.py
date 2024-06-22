from time import sleep

import adafruit_adxl34x
import board

from glowing_hat.hue_sources.time_based_hue_source import TimeBasedHueSource
from glowing_hat.mode import Mode
from glowing_hat.sorters.axis_manager import AxisManager
from glowing_hat.tempo.tempo_pool import TempoPool
from glowing_hat.tools.tilt_to_sort import tilt_to_sort


class Tilter(Mode):
    """Tilt."""

    def configure(self):
        """Configure ourself."""
        i2c = board.I2C()
        self.accelerometer = adafruit_adxl34x.ADXL345(i2c)
        self.accelerometer.enable_motion_detection()
        self.axis_manager = AxisManager()
        self.hue_source = TimeBasedHueSource(
            seconds_per_rotation=self.conf["hue-seconds-per-rotation"]
        )
        self.value = self.conf["base-value"]

        self.tempo_pool = TempoPool(self)

    def run(self):
        """Do the work."""
        self.configure()
        self.hat.apply_value(self.conf["base-value"])

        while True:
            try:
                x, y, _ = self.accelerometer.acceleration
            except OSError:
                from glowing_hat.tools.logger import logging

                logging.debug("wtf")

            self.hat.sort_by_indeces(self.axis_manager.get_sort(tilt_to_sort(x, y)))

            self.hat.apply_value(self.value)

            for i in range(len(self.hat)):
                if i < self.conf["unlit-lights"]:
                    self.hat.pixels[i]["hue"] = self.hue_source.hue()
                else:
                    self.hat.pixels[i]["hue"] = self.hue_source.inverse_hue()

            self.hat.light_up()

            sleep(0.1)

    def trigger(self):
        """Spike the value."""
        self.value = 1.0

    def reduce(self):
        """Constantly resaturating."""
        while True:
            if self.value > self.conf["base-value"]:
                self.value -= self.conf["decay"]["amount"]

            sleep(self.conf["decay"]["interval"])
