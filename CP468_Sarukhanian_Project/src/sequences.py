"""Utilities for base Sarukhanian sequences and small helper ops."""
from __future__ import annotations

from typing import Dict

import numpy as np
from numpy.typing import NDArray

SequenceArray = NDArray[np.int8]

BASE_SEQUENCES: Dict[str, SequenceArray] = {
    "A": np.array([1, 1, 1], dtype=np.int8),
    "B": np.array([1, 1, -1], dtype=np.int8),
    "C": np.array([1, -1], dtype=np.int8),
    "D": np.array([1, -1], dtype=np.int8),
}

PATTERN_COLUMNS: Dict[str, SequenceArray] = {
    "x": np.array([1, 1, 1, 1], dtype=np.int8),
    "y": np.array([1, 1, -1, -1], dtype=np.int8),
    "z": np.array([-1, 1, -1, 1], dtype=np.int8),
    "w": np.array([-1, 1, 1, -1], dtype=np.int8),
}


def rev(vec: SequenceArray) -> SequenceArray:
    """Return a reversed copy of the provided ±1 vector."""
    return vec[::-1].copy()


REVERSED_SEQUENCES: Dict[str, SequenceArray] = {
    "rA": rev(BASE_SEQUENCES["A"]),
    "rB": rev(BASE_SEQUENCES["B"]),
    "rC": rev(BASE_SEQUENCES["C"]),
    "rD": rev(BASE_SEQUENCES["D"]),
}

ALL_SEQUENCES: Dict[str, SequenceArray] = {**BASE_SEQUENCES, **REVERSED_SEQUENCES}


def get_sequence(name: str) -> SequenceArray:
    """Fetch a base or reversed sequence by its token name."""
    if name not in ALL_SEQUENCES:
        raise KeyError(f"Unknown sequence token '{name}'.")
    return ALL_SEQUENCES[name]


def get_pattern(name: str) -> SequenceArray:
    """Return a 4-entry column pattern vector used for block tiling."""
    if name not in PATTERN_COLUMNS:
        raise KeyError(f"Unknown pattern token '{name}'.")
    return PATTERN_COLUMNS[name]


def tile_block(pattern_col: SequenceArray, row_vector: SequenceArray) -> NDArray[np.int8]:
    """Expand a column pattern and row vector into a 4xN block of ±1 values."""
    if pattern_col.shape != (4,):
        raise ValueError("Pattern column must have length 4 (for X,Y,Z,W).")
    if not np.all(np.isin(pattern_col, (-1, 1))):
        raise ValueError("Pattern column must be ±1.")
    if row_vector.ndim != 1:
        raise ValueError("Row vector must be 1-D.")
    if not np.all(np.isin(row_vector, (-1, 1))):
        raise ValueError("Row vector must be ±1.")
    return (pattern_col[:, None] * row_vector[None, :]).astype(np.int8)


__all__ = [
    "SequenceArray",
    "BASE_SEQUENCES",
    "PATTERN_COLUMNS",
    "ALL_SEQUENCES",
    "get_sequence",
    "get_pattern",
    "tile_block",
    "rev",
]
