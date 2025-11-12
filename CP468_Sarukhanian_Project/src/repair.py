"""Repair utilities for tweaking the Sarukhanian block plan."""
from __future__ import annotations

from copy import deepcopy
from random import Random
from typing import Callable, Dict, Iterable, List, Tuple

from .construction import PlanBlock, PlanType, plan_to_sequences, verify_four_sequences


def _clone_plan(plan: PlanType) -> PlanType:
    return deepcopy(plan)


def apply_sign_flip(plan: PlanType, where: int | Iterable[int] | Callable[[PlanBlock, int], bool] | None = None) -> PlanType:
    """Flip the sign on selected blocks and return a new plan."""
    updated = _clone_plan(plan)
    indices: List[int]
    if where is None:
        indices = list(range(len(updated)))
    elif isinstance(where, int):
        indices = [where]
    elif callable(where):
        indices = [idx for idx, block in enumerate(updated) if where(block, idx)]
    else:
        indices = list(where)
    for idx in indices:
        updated[idx] = {**updated[idx], "sign": -int(updated[idx].get("sign", 1))}
    return updated


def swap_blocks(plan: PlanType, i: int, j: int) -> PlanType:
    """Swap two block positions in the plan."""
    if not (0 <= i < len(plan) and 0 <= j < len(plan)):
        raise IndexError("Swap indices out of range.")
    updated = _clone_plan(plan)
    updated[i], updated[j] = updated[j], updated[i]
    return updated


def auto_local_search(
    plan: PlanType,
    max_steps: int = 500,
    random_seed: int = 0,
) -> Dict[str, object]:
    """Stochastic local search over the plan using sign flips and swaps."""
    rng = Random(random_seed)
    current_plan = _clone_plan(plan)
    current_sequences = plan_to_sequences(current_plan).as_tuple()
    current_diag = verify_four_sequences(*current_sequences)
    best_plan = _clone_plan(current_plan)
    best_sequences = current_sequences
    best_diag = current_diag

    def score(diag: Dict[str, object]) -> Tuple[int, int]:
        return diag["num_nonzero_shifts"], diag["max_abs_deviation"]

    best_score = score(best_diag)
    current_score = best_score

    for _ in range(max_steps):
        candidate_plan = _clone_plan(current_plan)
        if rng.random() < 0.6:
            idx = rng.randrange(len(candidate_plan))
            candidate_plan[idx] = {
                **candidate_plan[idx],
                "sign": -int(candidate_plan[idx].get("sign", 1)),
            }
        else:
            i, j = rng.sample(range(len(candidate_plan)), 2)
            candidate_plan[i], candidate_plan[j] = candidate_plan[j], candidate_plan[i]
        sequences = plan_to_sequences(candidate_plan).as_tuple()
        diag = verify_four_sequences(*sequences)
        cand_score = score(diag)
        if cand_score <= current_score:
            current_plan = candidate_plan
            current_sequences = sequences
            current_diag = diag
            current_score = cand_score
        if cand_score < best_score:
            best_plan = _clone_plan(candidate_plan)
            best_sequences = sequences
            best_diag = diag
            best_score = cand_score
        if best_score == (0, 0):
            break

    return {
        "plan": best_plan,
        "sequences": best_sequences,
        "diagnostics": best_diag,
    }


__all__ = ["apply_sign_flip", "swap_blocks", "auto_local_search"]
