from os.path import dirname, join as pjoin
from scipy.io import wavfile
import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import pyaudio

def distort(data):
    return data.clip(-2000, 2000)

DELAY_FRAMES=20000
def delay(data):
    delayed_frames = []
    final_frames = []
    for i in range(len(data)):
        delayed_frames.insert(0, data[i])
        if i > DELAY_FRAMES:
            frame = data[i] + delayed_frames.pop()
            final_frames.append(frame)
        else:
            final_frames.append(data[i])
    return np.array(final_frames, dtype="int16")

samplerate, data = wavfile.read("samples/chord.wav")
print(f"number of channels = {data.shape[1]}")
length = data.shape[0] / samplerate
print(f"length = {length}s")
time = np.linspace(0., length, data.shape[0])
distorted_data = distort(data)
distorted_data = delay(distorted_data)
plt.plot(time, data[:, 0], label="Left channel")
plt.plot(time, data[:, 1], label="Right channel")
plt.plot(time, distorted_data[:, 0], label="Left Channel dist")
plt.plot(time, distorted_data[:, 1], label="Right Channel dist")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")

plt.show()

wavfile.write("output.wav", samplerate, distorted_data)
