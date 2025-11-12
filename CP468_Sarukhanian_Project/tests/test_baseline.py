from src.construction import build_sarukhanian_110, verify_four_sequences


def test_baseline_length_and_bug():
    x, y, z, w = build_sarukhanian_110()
    assert x.size == y.size == z.size == w.size == 110
    diag = verify_four_sequences(x, y, z, w)
    assert diag["num_nonzero_shifts"] > 0
    assert diag["max_abs_deviation"] > 0
