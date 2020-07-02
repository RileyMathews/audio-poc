from os.path import dirname, join as pjoin
from scipy.io import wavfile
import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import pyaudio

def distort(data):
    return data.clip(-2000, 2000)
    # data_copy.setflags(write=1)
    # for i in range(len(data_copy)):
    #     if data_copy[i][0] > 0.6:
    #         data_copy[i][0] = 0.6
    #         data_copy[i][1] = 0.6
    #     if data_copy[i][0] < -0.6:
    #         data_copy[i][0] = -0.6
    #         data_copy[i][1] = -0.6
    # return data_copy

samplerate, data = wavfile.read("samples/chord.wav")
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


wavfile.write("output.wav", samplerate, distorted_data)
# p = pyaudio.PyAudio()
# stream = p.open(format=pyaudio.paInt16,
#                 channels=2,
#                 rate=samplerate,
#                 output=True)


# stream.write(distorted_data)

# stream.stop_stream()
# stream.close()

# # close PyAudio (5)
# p.terminate()
