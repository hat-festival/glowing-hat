import aubio
import numpy as np
import pyaudio

# initialise pyaudio
p = pyaudio.PyAudio()

# open stream
buffer_size = 512
pyaudio_format = pyaudio.paFloat32
n_channels = 1
samplerate = 48000
stream = p.open(
    format=pyaudio_format,
    channels=n_channels,
    rate=samplerate,
    input=True,
    frames_per_buffer=buffer_size,
)

win_s = 4096  # fft size
hop_s = buffer_size  # hop size
o = aubio.onset("default", win_s, hop_s, samplerate)

while True:
    # try:
    audiobuffer = stream.read(buffer_size)
    signal = np.fromstring(audiobuffer, dtype=np.float32)

    if o(signal):
        print("%f" % o.get_last_s())

    # except KeyboardInterrupt:
    #     print("*** Ctrl+C pressed, exiting")
    #     break

stream.stop_stream()
stream.close()
p.terminate()
