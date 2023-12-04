import numpy as np

from minmax.estimate import estimate


def test_estimate():
    state = np.zeros((3, 3), dtype=str)
    assert np.all(estimate(state, 'X'), np.array([
        [3, 2, 3],
        [2, 4, 2],
        [3, 2, 3],
    ]))
