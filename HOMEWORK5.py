import numpy as np


def center_of_gravity(x):

    indices = np.arange(len(x))
    c = np.dot(indices, x) / np.sum(x)
    return c


def matched_identity(x):

    I = np.eye(len(x))
    return I


def sine_and_cosine(t_start, t_end, t_steps):

    t = np.linspace(t_start, t_end, t_steps)
    x = np.cos(t)
    y = np.sin(t)

    return t, x, y