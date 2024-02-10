import math
import time
from collections import deque

import numpy as np
from scipy.signal import savgol_filter  # noqa: F401
from src.fft import getFFT
from src.stream_reader_pyaudio import Stream_Reader
from src.utils import *  # noqa: F403


class Stream_Analyzer:  # noqa: N801
    """
    The Audio_Analyzer class provides access to continuously recorded
    (and mathematically processed) audio data.

    Arguments:

        device: int or None:      Select which audio stream to read .
        rate: float or None:      Sample rate to use. Defaults to something supported.
        FFT_window_size_ms: int:  Time window size (in ms) to use for the FFT transform
        updatesPerSecond: int:    How often to record new data.

    """  # noqa: E501, D205, D212, D407, D412

    def __init__(  # noqa: D107
        self,
        rate=None,
        FFT_window_size_ms=50,  # noqa: N803
        updates_per_second=100,
        n_frequency_bins=51,
    ):
        self.n_frequency_bins = n_frequency_bins
        self.rate = rate
        self.verbose = False
        verbose = self.verbose

        self.stream_reader = Stream_Reader(
            rate=rate,
            updates_per_second=updates_per_second,
            verbose=verbose,
        )

        self.rate = self.stream_reader.rate

        # Custom settings:
        self.rolling_stats_window_s = 20  # The axis range of the FFT features will adapt dynamically using a window of N seconds  # noqa: E501
        self.equalizer_strength = 0.20  # [0-1] --> gradually rescales all FFT features to have the same mean  # noqa: E501

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
        self.data_windows_to_buffer = max(1, self.data_windows_to_buffer)

        # This can probably be done more elegantly...
        self.fftx_bin_indices = (
            np.logspace(
                np.log2(len(self.fftx)),
                0,
                len(self.fftx),
                endpoint=True,
                base=2,
                dtype=None,
            )
            - 1
        )
        self.fftx_bin_indices = np.round(
            ((self.fftx_bin_indices - np.max(self.fftx_bin_indices)) * -1)
            / (len(self.fftx) / self.n_frequency_bins),
            0,
        ).astype(int)
        self.fftx_bin_indices = np.minimum(
            np.arange(len(self.fftx_bin_indices)),
            self.fftx_bin_indices - np.min(self.fftx_bin_indices),
        )

        self.frequency_bin_energies = np.zeros(self.n_frequency_bins)
        self.frequency_bin_centres = np.zeros(self.n_frequency_bins)
        self.fftx_indices_per_bin = []
        for bin_index in range(self.n_frequency_bins):
            bin_frequency_indices = np.where(self.fftx_bin_indices == bin_index)
            self.fftx_indices_per_bin.append(bin_frequency_indices)
            fftx_frequencies_this_bin = self.fftx[bin_frequency_indices]
            self.frequency_bin_centres[bin_index] = np.mean(
                fftx_frequencies_this_bin
            )

        # Hardcoded parameters:
        self.fft_fps = 30
        # self.log_features = False  # Plot log(FFT features) instead of FFT features --> usually pretty bad  # noqa: E501
        self.delays = deque(maxlen=20)
        self.num_ffts = 0
        self.strongest_frequency = 0

        # Assume the incoming sound follows a pink noise spectrum:
        self.power_normalization_coefficients = np.logspace(
            np.log2(1),
            np.log2(np.log2(self.rate / 2)),
            len(self.fftx),
            endpoint=True,
            base=2,
            dtype=None,
        )
        self.rolling_stats_window_n = (
            self.rolling_stats_window_s * self.fft_fps
        )  # Assumes ~30 FFT features per second
        self.rolling_bin_values = numpy_data_buffer(  # noqa: F405
            self.rolling_stats_window_n,
            self.n_frequency_bins,
            start_value=25000,
        )
        self.bin_mean_values = np.ones(self.n_frequency_bins)

        print(
            "Using FFT_window_size length of %d for FFT ---> window_size = %dms"
            % (self.FFT_window_size, self.FFT_window_size_ms)
        )
        print(
            "##################################################################################################"
        )

        # Let's get started:
        self.stream_reader.stream_start(self.data_windows_to_buffer)

    def update_rolling_stats(self):  # noqa: D102
        self.rolling_bin_values.append_data(self.frequency_bin_energies)
        self.bin_mean_values = np.mean(
            self.rolling_bin_values.get_buffer_data(), axis=0
        )
        self.bin_mean_values = np.maximum(
            (1 - self.equalizer_strength) * np.mean(self.bin_mean_values),
            self.bin_mean_values,
        )

    def update_features(self, n_bins=3):  # noqa: ARG002, D102
        latest_data_window = self.stream_reader.data_buffer.get_most_recent(
            self.FFT_window_size
        )

        self.fft = getFFT(
            latest_data_window,
        )

        # Equalize pink noise spectrum falloff:
        self.fft = self.fft * self.power_normalization_coefficients
        self.num_ffts += 1
        self.fft_fps = self.num_ffts / (
            time.time() - self.stream_reader.stream_start_time
        )

        import ipdb; ipdb.set_trace()
        print(1)
        self.strongest_frequency = self.fftx[np.argmax(self.fft)]
        # pump this into Redis
        print(self.strongest_frequency)

        # ToDo: replace this for-loop with pure numpy code
        for bin_index in range(self.n_frequency_bins):
            self.frequency_bin_energies[bin_index] = np.mean(
                self.fft[self.fftx_indices_per_bin[bin_index]]
            )

        # Beat detection ToDo:
        # https://www.parallelcube.com/2018/03/30/beat-detection-algorithm/
        # https://github.com/shunfu/python-beat-detector
        # https://pypi.org/project/vamp/

        return  # noqa: PLR1711

    def get_audio_features(self):  # noqa: D102
        if (
            self.stream_reader.new_data
        ):  # Check if the stream_reader has new audio data we need to process
            self.update_features()
            self.stream_reader.new_data = False

        return (
            self.fftx,
            self.fft,
            self.frequency_bin_centres,
            self.frequency_bin_energies,
        )
