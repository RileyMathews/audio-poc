from os.path import dirname, join as pjoin
from scipy.io import wavfile
import scipy.io
import matplotlib.pyplot as plt
import numpy as np

def distort(data):
    data_copy = data
    for i in range(len(data_copy)):
        if data_copy[i][0] > 0.6:
            data_copy[i][0] = 0.6
            data_copy[i][1] = 0.6
        if data_copy[i][0] < -0.6:
            data_copy[i][0] = -0.6
            data_copy[i][1] = -0.6
    return data_copy

data_dir = pjoin(dirname(scipy.io.__file__), 'tests', 'data')
wav_fname = pjoin(data_dir, 'test-44100Hz-2ch-32bit-float-be.wav')
samplerate, data = wavfile.read(wav_fname)
print(f"number of channels = {data.shape[1]}")
length = data.shape[0] / samplerate
print(f"length = {length}s")
time = np.linspace(0., length, data.shape[0])
distorted_data = distort(data)
plt.plot(time, data[:, 0], label="Left channel")
plt.plot(time, data[:, 1], label="Right channel")
plt.plot(time, distorted_data[:, 0], label="Left Channel dist")
plt.plot(time, distorted_data[:, 1], label="Right Channel dist")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()
