import numpy as np


def pwlinear_with_xedges(edges):
    def pwlinear(x):
        igt = np.searchsorted(edges, x)
        igt = np.clip(igt, 1, len(edges) - 1)
        ilt = igt - 1
        out = ilt + (x - edges[ilt]) / (edges[igt] - edges[ilt])
        return np.clip(out, 0, len(edges) - 1)
    return pwlinear


def pwlinear_with_yedges(edges):
    def pwlinear(x):
        out = np.clip(x, 0, len(edges) - 1)
        ilt = np.clip(np.floor(out), 0, len(edges) - 2).astype(np.int)
        igt = ilt + 1
        eilt = edges[ilt]
        eigt = edges[igt]
        return eilt + (eigt - eilt) * (out - ilt)
    return pwlinear


def replicate(fn, x_step=1, y_step=1):
    def out_fn(x):
        return fn(x - np.floor(x / x_step) * x_step) + np.floor(x / x_step) * y_step
    return out_fn


def compose2(f, g):
    return lambda x: f(g(x))


def weighted_sigmoid(weight):
    def sigmoid(x):
        return 1 / (1 + np.exp(-(x - .5) * weight))
    return sigmoid


"""
    # example for pentatonic scale (from real number to snapped 0, 3, 5, 7, 10, 12, 15, 17, ...)
    edges = np.array([0, 3, 5, 7, 10, 12], dtype=np.float)
    nnotes = len(edges) - 1  # number of notes
    nsteps = 12  # octave

    pwly = pwlinear_with_yedges(edges)
    step_fn = replicate(weighted_sigmoid(20))  # between 8 and 20
    my_fn = compose2(pwly, step_fn)  # one octave
    my_fn = replicate(my_fn, nnotes, nsteps)

    x = np.linspace(0, 10, 200)
    plt.plot(x, my_fn(x))
"""
