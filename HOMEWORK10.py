import numpy as np
import torch, torch.nn

def get_features(waveform, Fs):
    emphasized = np.append(waveform[0], waveform[1:] - 0.97 * waveform[:-1])

    frame_length = int(0.004 * Fs)
    step = int(0.002 * Fs)

    frames = []
    starts = []

    for start in range(0, len(emphasized) - frame_length + 1, step):
        frames.append(emphasized[start:start + frame_length])
        starts.append(start)

    frames = np.array(frames)

    spectra = np.abs(np.fft.fft(frames, axis=1))
    features = spectra[:, :frame_length // 2]

    vad_frame_length = int(0.025 * Fs)
    vad_step = int(0.010 * Fs)

    energies = []
    vad_starts = []

    for start in range(0, len(waveform) - vad_frame_length + 1, vad_step):
        frame = waveform[start:start + vad_frame_length]
        energies.append(np.sum(frame ** 2))
        vad_starts.append(start)

    energies = np.array(energies)

    labels = np.zeros(len(features), dtype=int)

    if len(energies) == 0:
        return features, labels

    threshold = 0.10 * np.max(energies)
    speech_frames = energies > threshold

    label = 1
    in_segment = False
    seg_start = 0

    for i, is_speech in enumerate(speech_frames):
        if is_speech and not in_segment:
            in_segment = True
            seg_start = vad_starts[i]

        elif not is_speech and in_segment:
            in_segment = False
            seg_end = vad_starts[i - 1] + vad_frame_length

            start_index = int(seg_start / step)
            end_index = int(seg_end / step)

            labels[start_index:end_index] = label
            label += 1

    if in_segment:
        seg_end = vad_starts[-1] + vad_frame_length

        start_index = int(seg_start / step)
        end_index = int(seg_end / step)

        labels[start_index:end_index] = label

    labels = labels[:len(features)]

    return features, labels


def train_neuralnet(features, labels, iterations):
    x = torch.tensor(features, dtype=torch.float32)
    y = torch.tensor(labels, dtype=torch.long)

    nfeats = features.shape[1]
    nlabels = int(np.max(labels)) + 1

    model = torch.nn.Sequential(
        torch.nn.LayerNorm(nfeats),
        torch.nn.Linear(nfeats, nlabels)
    )

    loss_fn = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    lossvalues = np.zeros(iterations)

    for i in range(iterations):
        optimizer.zero_grad()
        output = model(x)
        loss = loss_fn(output, y)
        loss.backward()
        optimizer.step()

        lossvalues[i] = loss.item()

    return model, lossvalues


def test_neuralnet(model, features):
    x = torch.tensor(features, dtype=torch.float32)

    with torch.no_grad():
        output = model(x)
        probabilities = torch.nn.functional.softmax(output, dim=1)

    return probabilities.detach().numpy()