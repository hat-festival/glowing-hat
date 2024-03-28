import numpy as np

from lib.conf import conf
from lib.tools import is_pi

if is_pi():
    import aubio
    import pyaudio
    import sounddevice  # noqa: F401


class Fourier:
    """Fourier transformer."""

    def __init__(self, owner):
        """Construct."""
        self.owner = owner

    def transform(self):
        """Do the work."""
        stream = get_stream()

        detector = aubio.onset(
            "default",
            conf["fourier"]["buffer-size"],
            conf["fourier"]["buffer-size"],
            conf["fourier"]["sample-rate"],
        )
        detector.set_silence(conf["fourier"]["silence-threshold"])

        while True:
            audiobuffer = stream.read(
                conf["fourier"]["buffer-size"],
                exception_on_overflow=False,
            )

            signal = np.frombuffer(audiobuffer, dtype=np.float32)

            new_note = detector(signal)

            if new_note[0]:
                self.owner.trigger()


def get_stream():
    """Get a pyaudio stream."""
    audio = pyaudio.PyAudio()
    pyaudio_format = pyaudio.paFloat32
    n_channels = 1

    return audio.open(
        input_device_index=conf["fourier"]["device-index"],
        format=pyaudio_format,
        channels=n_channels,
        rate=conf["fourier"]["sample-rate"],
        input=True,
        frames_per_buffer=conf["fourier"]["buffer-size"],
    )
