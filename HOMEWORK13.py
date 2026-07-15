import numpy as np
import librosa

def lpc(speech, frame_length, frame_skip, order):
    nframes = 1 + (len(speech) - frame_length) // frame_skip

    A = np.zeros((nframes, order + 1))
    excitation = np.zeros((nframes, frame_length))

    for m in range(nframes):
        start = m * frame_skip
        frame = speech[start:start + frame_length]

        A[m] = librosa.lpc(frame, order=order)

        for n in range(frame_length):
            excitation[m, n] = frame[n]

            for k in range(1, min(order, n) + 1):
                excitation[m, n] += A[m, k] * frame[n - k]

    return A, excitation


def synthesize(e, A, frame_skip):
    order = A.shape[1] - 1
    synthesis = np.zeros(len(e))

    for n in range(len(e)):
        frame = min(n // frame_skip, A.shape[0] - 1)
        synthesis[n] = e[n]

        for k in range(1, min(order, n) + 1):
            synthesis[n] -= A[frame, k] * synthesis[n - k]

    return synthesis


def robot_voice(excitation, T0, frame_skip):
    nframes = excitation.shape[0]
    gain = np.zeros(nframes)
    e_robot = np.zeros(nframes * frame_skip)

    for m in range(nframes):
        valid = excitation[m, -frame_skip:]
        gain[m] = np.sqrt(np.mean(valid ** 2))

    for n in range(0, len(e_robot), T0):
        frame = min(n // frame_skip, nframes - 1)
        e_robot[n] = gain[frame] * np.sqrt(T0)

    return gain, e_robot