from src.construction import get_default_plan
from src.repair import apply_sign_flip, auto_local_search, swap_blocks


def test_apply_sign_flip_single_index():
    plan = get_default_plan()
    flipped = apply_sign_flip(plan, 0)
    assert flipped[0]["sign"] == -plan[0]["sign"]
    for idx in range(1, len(plan)):
        assert flipped[idx] == plan[idx]


def test_swap_blocks_changes_order():
    plan = get_default_plan()
    swapped = swap_blocks(plan, 0, 1)
    assert swapped[0] == plan[1]
    assert swapped[1] == plan[0]


def test_auto_local_search_smoke():
    plan = get_default_plan()
    result = auto_local_search(plan, max_steps=10, random_seed=2)
    sequences = result["sequences"]
    diag = result["diagnostics"]
    assert len(sequences) == 4
    assert all(seq.size == 110 for seq in sequences)
    assert "num_nonzero_shifts" in diag
    assert "max_abs_deviation" in diag
