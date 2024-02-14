import datetime

import aubio
import numpy as np
import pyaudio

from lib.custodian import Custodian

cust = Custodian(namespace="hat")
audio = pyaudio.PyAudio()

buffer_size = 512
win_s = 4096  # fft size
hop_s = buffer_size  # hop size
pyaudio_format = pyaudio.paFloat32
n_channels = 1
samplerate = 48000

stream = audio.open(
    format=pyaudio_format,
    channels=n_channels,
    rate=samplerate,
    input=True,
    frames_per_buffer=buffer_size,
)

onset_detector = aubio.onset("hfc", win_s, hop_s, samplerate)
onset_detector.set_threshold(0.8)

while True:
    audiobuffer = stream.read(buffer_size)
    signal = np.frombuffer(audiobuffer, dtype=np.float32)

    if onset_detector(signal):
        cust.set("low", datetime.datetime.now().timestamp())

stream.stop_stream()
stream.close()
audio.terminate()
