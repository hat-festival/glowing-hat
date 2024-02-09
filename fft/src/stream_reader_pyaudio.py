import math  # noqa: F401
import sys  # noqa: F401
import time
from collections import deque

import numpy as np
import pyaudio
from src.utils import *  # noqa: F403


class Stream_Reader:  # noqa: N801
    """
    The Stream_Reader continuously reads data from a selected sound source using PyAudio

    Arguments:

        device: int or None:    Select which audio stream to read .
        rate: float or None:    Sample rate to use. Defaults to something supported.
        updatesPerSecond: int:  How often to record new data.

    """  # noqa: E501, D212, D400, D407, D412, D415

    def __init__(self, rate=None, updates_per_second=1000, verbose=False):  # noqa: FBT002, D107
        self.rate = rate
        self.verbose = verbose
        self.pa = pyaudio.PyAudio()

        # Temporary variables #hacks!
        self.update_window_n_frames = (
            1024  # Don't remove this, needed for device testing!
        )
        self.data_buffer = None

        self.device = 0
        if self.rate is None:
            self.rate = self.valid_low_rate(self.device)

        self.update_window_n_frames = round_up_to_even(  # noqa: F405
            self.rate / updates_per_second
        )
        self.updates_per_second = self.rate / self.update_window_n_frames
        self.info = self.pa.get_device_info_by_index(self.device)
        self.data_capture_delays = deque(maxlen=20)
        self.new_data = False
        if self.verbose:
            self.data_capture_delays = deque(maxlen=20)
            self.num_data_captures = 0

        self.stream = self.pa.open(
            input_device_index=self.device,
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.update_window_n_frames,
            stream_callback=self.non_blocking_stream_read,
        )

        print(
            "\n##################################################################################################"
        )
        print("\nDefaulted to using first working mic, Running on:")
        self.print_mic_info(self.device)
        print(
            "\n##################################################################################################"
        )
        print(
            "Recording from %s at %d Hz\nUsing (non-overlapping) data-windows of %d samples (updating at %.2ffps)"  # noqa: E501
            % (
                self.info["name"],
                self.rate,
                self.update_window_n_frames,
                self.updates_per_second,
            )
        )

    def non_blocking_stream_read(self, in_data, frame_count, time_info, status):  # noqa: ARG002, D102
        if self.verbose:
            start = time.time()

        if self.data_buffer is not None:
            self.data_buffer.append_data(np.frombuffer(in_data, dtype=np.int16))
            self.new_data = True

        if self.verbose:
            self.num_data_captures += 1
            self.data_capture_delays.append(time.time() - start)

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

        print("\n-- Starting live audio stream...\n")
        self.stream.start_stream()
        self.stream_start_time = time.time()

    def terminate(self):  # noqa: D102
        print("Sending stream termination command...")
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()

    def valid_low_rate(self, device, test_rates=[44100, 22050]):  # noqa: B006
        """Set the rate to the lowest supported audio rate."""
        for testrate in test_rates:
            if self.test_device(device, rate=testrate):
                return testrate

        # If none of the test_rates worked, try the default rate:
        self.info = self.pa.get_device_info_by_index(device)
        default_rate = int(self.info["defaultSampleRate"])

        if self.test_device(device, rate=default_rate):
            return default_rate

        print(
            "SOMETHING'S WRONG! I can't figure out a good sample-rate for DEVICE =>",  # noqa: E501
            device,
        )
        return default_rate

    def test_device(self, device, rate=None):
        """given a device ID and a rate, return True/False if it's valid."""  # noqa: D403
        try:
            self.info = self.pa.get_device_info_by_index(device)
            if not self.info["maxInputChannels"] > 0:
                return False

            if rate is None:
                rate = int(self.info["defaultSampleRate"])

            stream = self.pa.open(
                format=pyaudio.paInt16,
                channels=1,
                input_device_index=device,
                frames_per_buffer=self.update_window_n_frames,
                rate=rate,
                input=True,
            )
            stream.close()
            return True  # noqa: TRY300
        except Exception as e:  # noqa: BLE001, F841
            # print(e)
            return False

    def print_mic_info(self, mic):  # noqa: D102
        mic_info = self.pa.get_device_info_by_index(mic)
        print("\nMIC %s:" % (str(mic)))
        for k, v in sorted(mic_info.items()):
            print("%s: %s" % (k, v))  # noqa: UP031
