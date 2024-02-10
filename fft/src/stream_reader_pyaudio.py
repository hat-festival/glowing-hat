import numpy as np
import pyaudio
from src.utils import *  # noqa: F403


class Stream_Reader:  # noqa: N801
    """Read a stream."""

    def __init__(self, updates_per_second=1000):  # noqa: D107
        self.pa = pyaudio.PyAudio()
        self.data_buffer = None
        self.device = 0
        self.rate = 48000

        self.update_window_n_frames = round_up_to_even(  # noqa: F405
            self.rate / updates_per_second
        )
        self.updates_per_second = self.rate / self.update_window_n_frames
        self.new_data = False

        self.stream = self.pa.open(
            input_device_index=self.device,
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.update_window_n_frames,
            stream_callback=self.non_blocking_stream_read,
        )

    def non_blocking_stream_read(self, in_data, frame_count, time_info, status):  # noqa: ARG002, D102
        if self.data_buffer is not None:
            self.data_buffer.append_data(np.frombuffer(in_data, dtype=np.int16))
            self.new_data = True

        return in_data, pyaudio.paContinue

    def stream_start(self, data_windows_to_buffer=None):  # noqa: D102
        self.data_windows_to_buffer = data_windows_to_buffer

        if data_windows_to_buffer is None:
            self.data_windows_to_buffer = int(
                self.updates_per_second / 2
            )  # By default, buffer 0.5 second of audio
        else:
            self.data_windows_to_buffer = data_windows_to_buffer

        self.data_buffer = numpy_data_buffer(  # noqa: F405
            self.data_windows_to_buffer, self.update_window_n_frames
        )

        self.stream.start_stream()

    def terminate(self):  # noqa: D102
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()
