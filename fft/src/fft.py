import numpy as np
import pyfftw


def getFFT(data):  # noqa: N802, D103
    data = data * np.hamming(len(data))
    return abs(pyfftw.interfaces.numpy_fft.rfft(data)[1:])
