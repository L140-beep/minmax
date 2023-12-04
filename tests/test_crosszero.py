import numpy as np

from minmax.estimate import estimate


def test_estimate():
    state = np.zeros((3, 3), dtype=str)
    assert np.array_equal(estimate(state, 'X'), (np.array([
        [3, 2, 3],
        [2, 4, 2],
        [3, 2, 3],
    ]).astype(int)))
    state[1, 1] = 'X'
    assert np.array_equal(estimate(state, 'O'), (np.array(
        [
            [4, 3, 4],
            [3, 0, 3],
            [4, 3, 4]
        ]
    )))

    state = np.array([
        ['', '', ''],
        ['X', '', 'O'],
        ['X', '', 'O']])

    assert np.array_equal(estimate(state, 'X'), np.array([
        [12, 4, 10],
        [0, 10, 0],
        [0, 5, 0]
    ]
    ))
