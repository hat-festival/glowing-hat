from multiprocessing import Process
from time import sleep

import aubio
import numpy as np
import pyaudio

from lib.mode import Mode
from lib.tools.utils import scale_colour


class MusicBounce(Mode):
    """Dance to the music."""

    def reconfigure(self):
        """Configure ourself."""
        # self.custodian.set("axis", "none")  # FIXME get this from the prefs
        self.buffer_size = self.prefs["sound"]["buffer-size"]

    def run(self):
        """Do the stuff."""
        self.reconfigure()

        self.drums = {
            "high": {"colour": (255, 0, 0), "value": 0, "new_value": 0},
            "mid": {"colour": (0, 255, 0), "value": 0, "new_value": 0},
            "low": {"colour": (0, 0, 255), "value": 0, "new_value": 0},
        }

        self.analyse_sound()

    def punch(self):
        """Illuminate the hat."""
        colour = self.get_colour()
        # all these lookups might have a performance hit, maybe?
        for i in range(
            self.prefs["decay"]["max"],
            self.prefs["decay"]["min"],
            self.prefs["decay"]["step"],
        ):
            colour = scale_colour(colour, i / 100)
            self.hat.fill(colour)
            sleep(self.prefs["decay"]["rate"])

    def analyse_sound(self):
        """Directly analyse the audio stream."""
        stream = self.get_stream()
        onset_detector = self.get_onset_detector()

        process = None
        while True:
            audiobuffer = stream.read(self.buffer_size, exception_on_overflow=False)
            signal = np.frombuffer(audiobuffer, dtype=np.float32)

            if onset_detector(signal):
                if process and process.is_alive():
                    process.terminate()

                process = Process(target=self.punch)
                process.start()

    def get_stream(self):
        """Get a pyaudio stream."""
        audio = pyaudio.PyAudio()
        pyaudio_format = pyaudio.paFloat32
        n_channels = 1

        return audio.open(
            input_device_index=self.prefs["sound"]["device-index"],
            format=pyaudio_format,
            channels=n_channels,
            rate=self.prefs["sound"]["sample-rate"],
            input=True,
            frames_per_buffer=self.buffer_size,
        )

    def get_onset_detector(self):
        """Get an aubio onset-detector."""
        win_s = self.prefs["onset"]["fft-size"]
        hop_s = self.buffer_size

        detector = aubio.onset(
            self.prefs["onset"]["algorithm"],
            win_s,
            hop_s,
            self.prefs["sound"]["sample-rate"],
        )
        detector.set_threshold(self.prefs["onset"]["threshold"])

        return detector

    ###

    def from_redis(self):
        """Get triggers from Redis."""
        process = None
        while True:
            for pitch, data in self.drums.items():
                data["new_value"] = self.custodian.get(pitch)
                if data["value"] != data["new_value"]:
                    if process and process.is_alive():
                        process.terminate()

                    process = Process(target=self.punch)  # ), args=(data["colour"],))
                    process.start()
                    data["value"] = data["new_value"]
