"""Maple-to-Python Sarukhanian construction utilities."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

import numpy as np

from .npaf import npaf_sum_four
from .sequences import SequenceArray, get_pattern, get_sequence, tile_block

PlanBlock = Dict[str, object]
PlanType = List[PlanBlock]


@dataclass
class ConstructionResult:
    x: SequenceArray
    y: SequenceArray
    z: SequenceArray
    w: SequenceArray

    def as_tuple(self) -> Tuple[SequenceArray, SequenceArray, SequenceArray, SequenceArray]:
        return self.x, self.y, self.z, self.w


def _build_default_plan() -> PlanType:
    plan: PlanType = []
    pattern_cycle = ["x", "y", "z", "w"]
    for idx in range(11):
        rotated = pattern_cycle[idx % 4 :] + pattern_cycle[: idx % 4]
        seq_entries = [
            {"seq": "A" if idx % 5 else "rA", "sign": 1},
            {"seq": "C" if idx % 2 else "rC", "sign": 1 if idx % 3 else -1},
            {"seq": "B" if idx % 3 == 0 else "rB", "sign": -1},
            {"seq": "D" if idx % 4 else "rD", "sign": 1},
        ]
        for block_idx, base in enumerate(seq_entries):
            plan.append(
                {
                    "pattern": rotated[block_idx],
                    "seq": base["seq"],
                    "sign": base["sign"],
                }
            )
    return plan


DEFAULT_PLAN: PlanType = _build_default_plan()
DEFAULT_CONFIG = {"plan": DEFAULT_PLAN}


def get_default_plan() -> PlanType:
    """Return a deep copy of the default plan."""
    return deepcopy(DEFAULT_PLAN)


def plan_total_length(plan: PlanType) -> int:
    """Compute the resulting sequence length from the block plan."""
    length = 0
    for block in plan:
        seq = get_sequence(str(block["seq"]))
        length += seq.size
    return length


def plan_to_sequences(plan: PlanType) -> ConstructionResult:
    """Expand a plan into concrete X, Y, Z, W sequences."""
    row_blocks = [[] for _ in range(4)]
    for block in plan:
        pattern_name = str(block["pattern"])
        seq_name = str(block["seq"])
        sign = int(block.get("sign", 1))
        if sign not in (-1, 1):
            raise ValueError("Sign must be ±1.")
        pattern = get_pattern(pattern_name)
        seq = get_sequence(seq_name)
        block_values = tile_block(pattern, seq) * sign
        for idx in range(4):
            row_blocks[idx].append(block_values[idx])
    concatenated = tuple(np.concatenate(chunks).astype(np.int8) for chunks in row_blocks)
    return ConstructionResult(*concatenated)  # type: ignore[arg-type]


def build_sarukhanian_110(config: Dict[str, object] | None = None) -> Tuple[SequenceArray, SequenceArray, SequenceArray, SequenceArray]:
    """Build the Sarukhanian sequences (default length 110) from a config."""
    cfg = deepcopy(DEFAULT_CONFIG)
    if config:
        cfg.update(config)
    plan = cfg.get("plan")
    if not isinstance(plan, list):
        raise TypeError("Config must provide a list[dict] plan.")
    sequences = plan_to_sequences(plan).as_tuple()
    lengths = {seq.size for seq in sequences}
    if len(lengths) != 1:
        raise ValueError("Sequences must share a common length.")
    total_length = lengths.pop()
    if total_length != 110:
        raise AssertionError(
            f"Plan produced sequences of length {total_length}, expected 110."
        )
    return sequences


def verify_four_sequences(x: SequenceArray, y: SequenceArray, z: SequenceArray, w: SequenceArray) -> Dict[str, object]:
    """Return diagnostics describing the four-sequence summed NPAF."""
    sum_series = npaf_sum_four(x, y, z, w)
    non_zero = np.nonzero(sum_series)[0]
    nonzero_pairs = [
        (int(shift + 1), int(sum_series[shift]))
        for shift in non_zero[:10]
    ]
    max_abs = int(np.max(np.abs(sum_series))) if sum_series.size else 0
    worst_shift = int(non_zero[np.argmax(np.abs(sum_series[non_zero]))] + 1) if non_zero.size else None
    return {
        "length": int(x.size),
        "num_nonzero_shifts": int(non_zero.size),
        "nonzero_pairs": nonzero_pairs,
        "max_abs_deviation": max_abs,
        "worst_shift": worst_shift,
        "sum_series": sum_series,
    }


__all__ = [
    "PlanBlock",
    "PlanType",
    "ConstructionResult",
    "DEFAULT_PLAN",
    "DEFAULT_CONFIG",
    "get_default_plan",
    "plan_total_length",
    "plan_to_sequences",
    "build_sarukhanian_110",
    "verify_four_sequences",
]
