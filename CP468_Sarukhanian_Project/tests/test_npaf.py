import numpy as np

from src.npaf import npaf, npaf_all_shifts, npaf_sum_four


def test_npaf_all_ones():
    seq = np.ones(5, dtype=np.int8)
    expected = [5, 4, 3, 2, 1]
    for shift in range(5):
        assert npaf(seq, shift) == expected[shift]


def test_npaf_alternating():
    seq = np.array([1, -1, 1, -1, 1, -1], dtype=np.int8)
    values = npaf_all_shifts(seq)
    assert values.tolist() == [-5, 4, -3, 2, -1]


def test_npaf_sum_four_matches_manual_sum():
    seqs = [
        np.array([1, 1, 1, 1], dtype=np.int8),
        np.array([1, 1, -1, -1], dtype=np.int8),
        np.array([1, -1, 1, -1], dtype=np.int8),
        np.array([-1, 1, 1, -1], dtype=np.int8),
    ]
    sum_series = npaf_sum_four(*seqs)
    manual = sum(npaf_all_shifts(seq) for seq in seqs)
    np.testing.assert_array_equal(sum_series, manual)
