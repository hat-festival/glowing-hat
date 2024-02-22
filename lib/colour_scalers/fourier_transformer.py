from multiprocessing import Process, Value
from time import sleep

import numpy as np

from lib.conf import conf
from lib.tools import is_pi

if is_pi():
    import aubio
    import pyaudio


class FourierTransformer:
    """Scales colours with the music."""

    def __init__(self, normaliser):
        """Construct."""
        self.normaliser = normaliser
        self.normaliser.factor = Value("f", self.normaliser.default_brightness)
        self.step_size = 0.02
        self.conf = conf["fourier"]
        self.buffer_size = self.conf["sound"]["buffer-size"]
        self.decay_interval = 0.05

    def reduce(self):
        """Constantly reducing the brightness."""
        while True:
            if (
                self.normaliser.factor.value
                > self.normaliser.default_brightness
            ):
                self.normaliser.factor.value -= 0.05
                sleep(self.decay_interval)

    def run(self):
        """Do the work."""
        stream = self.get_stream()
        onset_detector = self.get_onset_detector()

        process = Process(target=self.reduce)
        process.start()
        while True:
            audiobuffer = stream.read(
                self.buffer_size, exception_on_overflow=False
            )
            signal = np.frombuffer(audiobuffer, dtype=np.float32)

            if onset_detector(signal):
                self.normaliser.factor.value = self.normaliser.max_brightness

    def get_stream(self):
        """Get a pyaudio stream."""
        audio = pyaudio.PyAudio()
        pyaudio_format = pyaudio.paFloat32
        n_channels = 1

        return audio.open(
            input_device_index=self.conf["sound"]["device-index"],
            format=pyaudio_format,
            channels=n_channels,
            rate=self.conf["sound"]["sample-rate"],
            input=True,
            frames_per_buffer=self.buffer_size,
        )

    def get_onset_detector(self):
        """Get an aubio onset-detector."""
        win_s = self.conf["onset"]["fft-size"]
        hop_s = self.buffer_size

        detector = aubio.onset(
            self.conf["onset"]["algorithm"],
            win_s,
            hop_s,
            self.conf["sound"]["sample-rate"],
        )
        detector.set_threshold(self.conf["onset"]["threshold"])

        return detector
