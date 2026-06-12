import numpy as np

def major_chord(f, Fs):
    t = np.arange(0, 0.5, 1/Fs)

    f1 = f
    f2 = f * (2 ** (4/12))
    f3 = f * (2 ** (7/12))

    x = (np.sin(2*np.pi*f1*t) +
         np.sin(2*np.pi*f2*t) +
         np.sin(2*np.pi*f3*t))

    return x

def dft_matrix(N):
    k = np.arange(N).reshape(N, 1)
    n = np.arange(N).reshape(1, N)

    W = np.cos(2*np.pi*k*n/N) - 1j*np.sin(2*np.pi*k*n/N)

    return W

def spectral_analysis(x, Fs):
    N = len(x)

    W = dft_matrix(N)
    X = W @ x

    magnitude = np.abs(X)

    half = N // 2
    magnitude = magnitude[:half]

    freqs = np.arange(half) * Fs / N

    indices = np.argsort(magnitude)[-3:]
    loudest_freqs = np.sort(freqs[indices])

    return loudest_freqs[0], loudest_freqs[1], loudest_freqs[2]