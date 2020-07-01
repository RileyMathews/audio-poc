"""PyAudio Example: Play a wave file."""

import pyaudio
import wave
import sys
import os

def distort(frames):
    amp_list = list(frames)
    for i in range(len(amp_list)):
        amp = amp_list[i]
        if amp > 127:
            amp_list[i] = 255
        else:
            amp_list[i] = 0
    return bytes(amp_list)

def play_file(name, effect=None):
    wf = wave.open(f"samples/{name}", 'rb')

    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    # open stream (2)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    all_frames = wf.readframes(wf.getnframes())
    if effect != None:
        all_frames = effect(all_frames)
    stream.write(all_frames)

    stream.stop_stream()
    stream.close()

    p.terminate()

    wf.close()



for file in os.listdir("./samples"):
    print(file)
    play_file(file, distort)
