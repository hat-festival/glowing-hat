import numpy as np


def getFFT(data, rate, chunk_size, log_scale=False):  # noqa: FBT002, ARG001, N802, D103
    data = data * np.hamming(len(data))
    try:
        FFT = np.abs(np.fft.rfft(data)[1:])  # noqa: N806
    except:  # noqa: E722
        FFT = np.fft.fft(data)  # noqa: N806
        left, right = np.split(np.abs(FFT), 2)
        FFT = np.add(left, right[::-1])  # noqa: N806

    if log_scale:
        try:
            FFT = np.multiply(20, np.log10(FFT))  # noqa: N806
        except Exception as e:  # noqa: BLE001
            print("Log(FFT) failed: %s" % str(e))

    return FFT
