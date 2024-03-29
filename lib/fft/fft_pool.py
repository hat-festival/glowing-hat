import concurrent.futures

from lib.fft.fourier import Fourier


class FFTPool:
    """Manage FFT for modes."""

    def __init__(self, parent):
        """Construct."""
        self.parent = parent

        self.pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        self.fft = Fourier(self.parent)
        self.pool.submit(self.parent.reduce)  # TODO rename this?
        self.pool.submit(self.fft.transform)
