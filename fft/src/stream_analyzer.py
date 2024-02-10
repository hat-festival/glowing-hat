import math

import numpy as np
from scipy.signal import savgol_filter  # noqa: F401
from src.fft import getFFT
from src.stream_reader_pyaudio import Stream_Reader
from src.utils import *  # noqa: F403


class Stream_Analyzer:  # noqa: N801
    """Analyse a stream, I guess."""

    def __init__(  # noqa: D107
        self,
        rate=None,
        FFT_window_size_ms=50,  # noqa: N803
        updates_per_second=100,
        n_frequency_bins=51,
    ):
        self.n_frequency_bins = n_frequency_bins
        self.rate = rate

        self.stream_reader = Stream_Reader(
            updates_per_second=updates_per_second,
        )

        self.rate = self.stream_reader.rate

        self.FFT_window_size = round_up_to_even(  # noqa: F405
            self.rate * FFT_window_size_ms / 1000
        )
        self.FFT_window_size_ms = 1000 * self.FFT_window_size / self.rate
        self.fft = np.ones(int(self.FFT_window_size / 2), dtype=float)
        self.fftx = (
            np.arange(int(self.FFT_window_size / 2), dtype=float)
            * self.rate
            / self.FFT_window_size
        )

        self.data_windows_to_buffer = math.ceil(
            self.FFT_window_size / self.stream_reader.update_window_n_frames
        )

        self.stream_reader.stream_start(self.data_windows_to_buffer)

    # this is where stuff happens
    def update_features(self, n_bins=3):  # noqa: ARG002, D102
        latest_data_window = self.stream_reader.data_buffer.get_most_recent(
            self.FFT_window_size
        )

        self.fft = getFFT(
            latest_data_window,
        )

        self.strongest_frequency = self.fftx[np.argmax(self.fft)]
        # pump this into Redis
        print(self.strongest_frequency)

        return  # noqa: PLR1711

    # this is what the client calls
    def get_audio_features(self):  # noqa: D102
        if (
            self.stream_reader.new_data
        ):  # Check if the stream_reader has new audio data we need to process
            self.update_features()
            self.stream_reader.new_data = False
