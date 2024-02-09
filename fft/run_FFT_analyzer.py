import time

from src.stream_analyzer import Stream_Analyzer


def run_FFT_analyzer():  # noqa: N802, D103
    ear = Stream_Analyzer(
        rate=None,  # Audio samplerate, None uses the default source settings
        FFT_window_size_ms=60,  # Window size used for the FFT transform
        updates_per_second=1000,  # How often to read the audio stream for new data  # noqa: E501
        n_frequency_bins=400,  # The FFT features are grouped in bins
    )

    fps = 1.0 / 60  # How often to update the FFT features + display
    last_update = time.time()
    while True:
        if (time.time() - last_update) > fps:
            last_update = time.time()
            ear.get_audio_features()


if __name__ == "__main__":
    run_FFT_analyzer()
