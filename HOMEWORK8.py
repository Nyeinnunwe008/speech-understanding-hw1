import numpy as np

def waveform_to_frames(waveform, frame_length, step):
    num_frames = 1 + (len(waveform) - frame_length) // step
    frames = np.zeros((num_frames, frame_length))

    for i in range(num_frames):
        start = i * step
        frames[i, :] = waveform[start:start + frame_length]

    return frames

def frames_to_mstft(frames):
    mstft = np.abs(np.fft.fft(frames, axis=1))
    return mstft

def mstft_to_spectrogram(mstft):
    threshold = 0.001 * np.amax(mstft)
    mstft = np.maximum(threshold, mstft)
    spectrogram = 20 * np.log10(mstft)
    return spectrogram