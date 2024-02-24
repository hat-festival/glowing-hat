from multiprocessing import Process, Value
from time import sleep

import numpy as np

from lib.conf import conf
from lib.gamma import gamma
from lib.tools import is_pi
import ctypes
if is_pi():
    import aubio
    import pyaudio

if is_pi():  # nocov
    from RPi import GPIO
else:
    import tests.fake_gpio as GPIO  # noqa: N812


class ColourNormaliser:
    """Normalises colours."""

    def __init__(self):
        """Construct."""
        self.max_brightness = Value("f", conf["max-brightness"])
        self.proportion =Value("f", 0.3)
        self.default_brightness = Value(
            "f", self.max_brightness.value * self.proportion.value
        )
        self.factor = Value("f", self.default_brightness.value)
        self.decay_interval = 0.03
        self.decay_amount = 0.05
        self.rotary_step_size = 0.05

        self.doing_fft = Value(ctypes.c_bool, True)

        self.processes = {}

    def adjust_brightness(self, direction):
        """Adjust brightness."""
        if direction == "down":
            self.max_brightness.value = max(
                self.max_brightness.value - self.rotary_step_size, 0
            )

        if direction == "up":
            self.max_brightness.value += self.rotary_step_size
            if self.max_brightness.value > conf["max-brightness"]:
                self.max_brightness.value = conf["max-brightness"]

        self.realign_brightnesses()

    def realign_brightnesses(self):
        """Recalculate brightness."""
        self.default_brightness.value = max(
            self.max_brightness.value * self.proportion.value, 0.0
        )
        self.factor.value = self.default_brightness.value

    def normalise(self, triple):
        """Normalise a colour."""
        factor = max(self.factor.value, 0)
        return tuple(int(x * factor) for x in gamma_correct(triple))

    def run(self):
        """Do the work."""
        # for name, process in self.processes.items():
        #     if process.is_alive():
        #         process.terminate()
        #     self.processes[name] = None
        #     sleep(1)

        self.run_reducer()
        self.run_fourier()
        self.run_rotary()

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
        # https://github.com/aubio/aubio/issues/78#issuecomment-268632493
        stream = get_stream()
        onset_detector = get_onset_detector()

        # Aubio's pitch detection.
        pDetection = aubio.pitch("default", 2048, 1024, 48000)
        # Set unit.
        pDetection.set_unit("Hz")
        pDetection.set_silence(-40)

        while True:
            audiobuffer = stream.read(
                conf["fourier"]["sound"]["buffer-size"],
                exception_on_overflow=False,
            )
            signal = np.frombuffer(audiobuffer, dtype=np.float32)
            pitch = pDetection(signal)[0]
            volume = np.sum(signal**2) / len(signal)

# https://aubio.org/manual/latest/cli.html#aubionotes seems relevant

            if onset_detector(signal):
                self.factor.value = self.max_brightness.value
            # if pitch < 80  and volume > 0.005:
            #     print("kick")
            #     self.factor.value = self.max_brightness.value


    def reduce(self):
        """Constantly reducing the brightness."""
        while True:
            if self.doing_fft.value:
                if self.factor.value > self.default_brightness.value:
                    self.factor.value -= self.decay_amount
                    sleep(self.decay_interval)


    def rotary(self):
        """Run the rotary-encoder."""
        clk = conf["rotary"]["pins"]["clk"]
        dt = conf["rotary"]["pins"]["dt"]
        sw = conf["rotary"]["pins"]["sw"]

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        clk_last_state = GPIO.input(clk)
        sw_last_state = GPIO.input(sw)

        while True:
            clk_state = GPIO.input(clk)
            dt_state = GPIO.input(dt)

            if clk_state != clk_last_state:
                if dt_state != clk_state:
                    self.adjust_brightness("up")
                else:
                    self.adjust_brightness("down")

            clk_last_state = clk_state

            new_sw_state = GPIO.input(sw)
            if new_sw_state != sw_last_state and new_sw_state == 0:
                print("click")
                if self.doing_fft.value:
                    self.doing_fft.value = False
                    self.max_brightness.value = self.default_brightness.value
                    self.realign_brightnesses()
                else:
                    self.max_brightness.value = conf["max-brightness"]
                    self.realign_brightnesses()
                    self.doing_fft.value = True

            sw_last_state = new_sw_state

            sleep(0.01)


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


def get_onset_detector():
    """Get an aubio onset-detector."""
    win_s = conf["fourier"]["onset"]["fft-size"]
    hop_s = conf["fourier"]["sound"]["buffer-size"]

    detector = aubio.onset(
        conf["fourier"]["onset"]["algorithm"],
        win_s,
        hop_s,
        conf["fourier"]["sound"]["sample-rate"],
    )
    detector.set_threshold(conf["fourier"]["onset"]["threshold"])

    return detector
