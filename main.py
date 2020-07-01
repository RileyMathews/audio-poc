
import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

def distort(amplitudes):
    amplitude_stages = list(data)
    for i in range(len(amplitude_stages)):
        if amplitude_stages[i] > 127:
            amplitude_stages[i] += 20
            if amplitude_stages[i] > 255:
                amplitude_stages[i] = 255
        else:
            amplitude_stages[i] -= 20
            if amplitude_stages[i] < 0:
                amplitude_stages[i] = 0
    print(amplitude_stages)
    return bytes(amplitude_stages)

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    data = distort(data)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
