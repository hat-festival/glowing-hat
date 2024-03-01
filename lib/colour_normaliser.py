import ctypes
import threading
from multiprocessing import Process, Value
from time import sleep

import numpy as np

from lib.conf import conf
from lib.custodian import Custodian
from lib.gamma import gamma
from lib.logger import logging
from lib.oled import Oled
from lib.tools import is_pi

if is_pi():
    import aubio
    import pyaudio
    import sounddevice  # noqa: F401

if is_pi():  # nocov
    from RPi import GPIO
else:
    import tests.fake_gpio as GPIO  # noqa: N812


class ColourNormaliser:
    """Normalises colours."""

    def __init__(self):
        """Construct."""
        self.max_brightness = Value("f", conf["max-brightness"])
        self.proportion = Value("f", 0.3)
        self.default_brightness = Value(
            "f", self.max_brightness.value * self.proportion.value
        )
        self.factor = Value("f", self.default_brightness.value)
        self.decay_interval = 0.05
        self.decay_amount = 0.05
        self.rotary_step_size = 0.05

        self.doing_fft = Value(ctypes.c_bool, True)  # noqa: FBT003

        self.custodian = Custodian("hat")
        self.oled = Oled(self.custodian)

        self.processes = {}

    def set_fft_state(self, state):
        """Set the `doing_fft` state."""
        logging.info("setting `FFT` to `%s`", state)
        self.doing_fft.value = state
        self.custodian.set("fft-on", state)
        self.oled.update()

    def adjust_brightness(self, direction):
        """Adjust brightness."""
        logging.debug("turning brightness `%s`", direction)
        logging.debug("old value: `%f`", self.max_brightness.value)
        if direction == "down":
            self.max_brightness.value = max(
                self.max_brightness.value - self.rotary_step_size, 0
            )

        if direction == "up":
            self.max_brightness.value = min(
                self.max_brightness.value + self.rotary_step_size,
                conf["max-brightness"],
            )

        logging.debug("new value: `%f`", self.max_brightness.value)

        self.realign_brightnesses()
        if is_pi():
            self.oled.update()

    def realign_brightnesses(self):
        """Recalculate brightness."""
        self.default_brightness.value = max(
            self.max_brightness.value * self.proportion.value, 0.0
        )
        self.factor.value = self.default_brightness.value
        self.custodian.set(
            "brightness",
            (
                1
                / (conf["max-brightness"] * self.proportion.value)
                * self.default_brightness.value
            ),
        )

    def normalise(self, triple):
        """Normalise a colour."""
        factor = max(self.factor.value, 0)
        return tuple(int(x * factor) for x in gamma_correct(triple))

    def run(self):
        """Do the work."""
        self.run_reducer()
        self.run_fourier()
        self.run_rotary()
        logging.debug(self.processes)

    def run_reducer(self):
        """Run the reducer."""
        self.processes["reduce"] = Process(target=self.reduce)
        self.processes["reduce"].start()

    def run_fourier(self):
        """Run the Fourier Transformer."""
        self.processes["fourier"] = Process(target=self.fourier)
        self.processes["fourier"].start()

    def run_rotary(self):
        """Run the rotary."""
        self.processes["rotary"] = Process(target=self.rotary)
        self.processes["rotary"].start()

    def fourier(self):
        """Do the work."""
        stream = get_stream()

        detector = aubio.notes(
            "default",
            2048,
            1024,
            conf["fourier"]["sound"]["sample-rate"],
        )

        # detector = aubio.tempo(
        #     "default",
        #     2048,
        #     1024,
        #     conf["fourier"]["sound"]["sample-rate"],
        # )

        # detector = aubio.onset(
        #     "default",
        #     2048,
        #     1024,
        #     conf["fourier"]["sound"]["sample-rate"],
        # )
        detector.set_silence(-40)

        while True:
            audiobuffer = stream.read(
                conf["fourier"]["sound"]["buffer-size"],
                exception_on_overflow=False,
            )

            signal = np.frombuffer(audiobuffer, dtype=np.float32)

            new_note = detector(signal)

            if new_note[0]:
                self.factor.value = self.max_brightness.value

    def reduce(self):
        """Constantly reducing the brightness."""
        while True:
            if self.doing_fft.value:
                if self.factor.value > self.default_brightness.value:
                    self.factor.value -= self.decay_amount
                    sleep(self.decay_interval)
            else:
                sleep(1)

    def rotary(self):
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
                self.set_fft_state(not self.doing_fft.value)

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
                self.adjust_brightness("up")
            else:
                self.adjust_brightness("down")
            self.lock_rotary.release()


def gamma_correct(triple):
    """Gamma-correct a colour."""
    return tuple(map(lambda n: gamma[int(n)], triple))  # noqa: C417


def get_stream():
    """Get a pyaudio stream."""
    audio = pyaudio.PyAudio()
    pyaudio_format = pyaudio.paFloat32
    n_channels = 1

    return audio.open(
        input_device_index=conf["fourier"]["sound"]["device-index"],
        format=pyaudio_format,
        channels=n_channels,
        rate=conf["fourier"]["sound"]["sample-rate"],
        input=True,
        frames_per_buffer=conf["fourier"]["sound"]["buffer-size"],
    )
