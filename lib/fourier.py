import numpy as np

from lib.conf import conf
from lib.tools import is_pi

if is_pi():
    import aubio
    import pyaudio
    import sounddevice  # noqa: F401


class Fourier:
    """Fourier transformer."""

    def __init__(self, normaliser):
        """Construct."""
        self.owner = normaliser

    def transform(self):
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
                self.owner.trigger()


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
