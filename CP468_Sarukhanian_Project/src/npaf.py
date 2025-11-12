"""Nonperiodic autocorrelation helpers."""
from __future__ import annotations

from typing import Tuple

import numpy as np
from numpy.typing import NDArray

SequenceArray = NDArray[np.int8]


def _validate_sequence(a: SequenceArray) -> None:
    if a.ndim != 1:
        raise ValueError("Sequence must be 1-D.")
    if not np.issubdtype(a.dtype, np.integer):
        raise TypeError("Sequence must have integer dtype.")
    if not np.all((a == 1) | (a == -1)):
        raise ValueError("Sequence entries must be ±1.")


def npaf(a: SequenceArray, s: int) -> int:
    """Compute the nonperiodic autocorrelation of *a* at shift *s*."""
    _validate_sequence(a)
    n = a.size
    if not 0 <= s < n:
        raise ValueError(f"Shift s must be in [0, {n - 1}].")
    if s == 0:
        return int(np.dot(a, a))
    return int(np.dot(a[:-s], a[s:]))


def npaf_all_shifts(a: SequenceArray) -> NDArray[np.int32]:
    """Return the NPAF for shifts 1..n-1 as a vector."""
    _validate_sequence(a)
    n = a.size
    if n <= 1:
        return np.zeros(0, dtype=np.int32)
    result = np.empty(n - 1, dtype=np.int32)
    for shift in range(1, n):
        result[shift - 1] = npaf(a, shift)
    return result


def npaf_sum_four(x: SequenceArray, y: SequenceArray, z: SequenceArray, w: SequenceArray) -> NDArray[np.int32]:
    """Sum the NPAFs of four equal-length sequences over shifts 1..n-1."""
    lengths = {seq.size for seq in (x, y, z, w)}
    if len(lengths) != 1:
        raise ValueError("All sequences must have the same length.")
    return npaf_all_shifts(x) + npaf_all_shifts(y) + npaf_all_shifts(z) + npaf_all_shifts(w)


def summarized_diagnostics(x: SequenceArray, y: SequenceArray, z: SequenceArray, w: SequenceArray) -> Tuple[int, int]:
    """Return (num_nonzero_shifts, max_abs_deviation) for the four-sequence sum."""
    sum_series = npaf_sum_four(x, y, z, w)
    non_zero = np.count_nonzero(sum_series)
    max_abs = int(np.max(np.abs(sum_series))) if sum_series.size else 0
    return non_zero, max_abs


__all__ = [
    "npaf",
    "npaf_all_shifts",
    "npaf_sum_four",
    "summarized_diagnostics",
]
