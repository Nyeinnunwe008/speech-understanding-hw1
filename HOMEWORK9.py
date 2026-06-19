import numpy as np

def VAD(waveform, Fs):
    frame_length = int(0.025 * Fs)
    step = int(0.010 * Fs)

    energies = []
    starts = []

    for start in range(0, len(waveform) - frame_length + 1, step):
        frame = waveform[start:start + frame_length]
        energy = np.sum(frame ** 2)
        energies.append(energy)
        starts.append(start)

    energies = np.array(energies)

    if len(energies) == 0:
        return []

    threshold = 0.10 * np.max(energies)
    speech_frames = energies > threshold

    segments = []
    in_segment = False
    seg_start = 0

    for i, is_speech in enumerate(speech_frames):
        if is_speech and not in_segment:
            in_segment = True
            seg_start = starts[i]

        elif not is_speech and in_segment:
            in_segment = False
            seg_end = starts[i - 1] + frame_length
            segments.append(waveform[seg_start:seg_end])

    if in_segment:
        seg_end = starts[-1] + frame_length
        segments.append(waveform[seg_start:seg_end])

    return segments


def segments_to_models(segments, Fs):
    models = []

    frame_length = int(0.004 * Fs)
    step = int(0.002 * Fs)

    for segment in segments:
        emphasized = np.append(segment[0], segment[1:] - 0.97 * segment[:-1])

        frames = []
        for start in range(0, len(emphasized) - frame_length + 1, step):
            frames.append(emphasized[start:start + frame_length])

        if len(frames) == 0:
            continue

        frames = np.array(frames)
        spectra = np.abs(np.fft.fft(frames, axis=1))

        half = frame_length // 2
        spectra = spectra[:, :half]

        spectra = np.maximum(spectra, 1e-10)
        log_spectra = 20 * np.log10(spectra)

        model = np.mean(log_spectra, axis=0)
        models.append(model)

    return models


def recognize_speech(testspeech, Fs, models, labels):
    segments = VAD(testspeech, Fs)
    test_models = segments_to_models(segments, Fs)

    sims = np.zeros((len(models), len(test_models)))
    test_outputs = []

    for k, test_model in enumerate(test_models):
        best_score = -1
        best_label = None

        for y, model in enumerate(models):
            min_len = min(len(model), len(test_model))

            m = model[:min_len]
            t = test_model[:min_len]

            similarity = np.dot(m, t) / (np.linalg.norm(m) * np.linalg.norm(t))
            sims[y, k] = similarity

            if similarity > best_score:
                best_score = similarity
                best_label = labels[y]

        test_outputs.append(best_label)

    return sims, test_outputs