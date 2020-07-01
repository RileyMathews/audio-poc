"""PyAudio Example: Play a wave file."""

import pyaudio
import wave
import sys
import os

DISTORTION_RATE = 1
ZERO_VOLTAGE_AMPLITUDE = 32768
MAXIMUM_AMPLITUDE = 65535

def distort_amplitude(amplitude):
    new_amplitude = amplitude
    if new_amplitude > ZERO_VOLTAGE_AMPLITUDE:
        new_amplitude += DISTORTION_RATE
        if new_amplitude > MAXIMUM_AMPLITUDE:
            new_amplitude = MAXIMUM_AMPLITUDE
    else:
        new_amplitude -= DISTORTION_RATE
        if new_amplitude < 0:
            new_amplitude = 0
    print(f"{amplitude} -> {new_amplitude}")
    return new_amplitude

def frames_matrix_to_bytes(matrix):
    flat_array = lambda matrix: [item for sublist in matrix for item in sublist]
    return bytes(flat_array(matrix))


def distort(frames):
    new_frames = []
    for i in range(len(frames)):
        frame = frames[i]
        left_channel_frame = [frame[0], frame[1]]
        right_channel_frame = [frame[2], frame[3]]

        left_channel_amplitude = list(distort_amplitude(int.from_bytes(bytes(left_channel_frame), byteorder="big")).to_bytes(2, "big"))
        right_channel_amplitude = list(distort_amplitude(int.from_bytes(bytes(right_channel_frame), byteorder="big")).to_bytes(2, "big"))

        new_frames.append([left_channel_amplitude[0], left_channel_amplitude[1], right_channel_amplitude[0], right_channel_amplitude[1]])
    
    return new_frames

        


def play_file(name):
    wf = wave.open(f"samples/{name}", 'rb')

    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    # open stream (2)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    frames_matrix = []
    for i in range(wf.getnframes()):
        frames_matrix.append(list(wf.readframes(1)))

    frames_matrix = distort(frames_matrix)
    new_bytes = frames_matrix_to_bytes(frames_matrix)
    stream.write(new_bytes)

    stream.stop_stream()
    stream.close()

    p.terminate()

    wf.close()



for file in os.listdir("./samples"):
    print(file)
    play_file(file)
