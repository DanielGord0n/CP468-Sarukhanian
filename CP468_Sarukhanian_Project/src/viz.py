"""Plotting helpers for Sarukhanian experiments."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

REPORT_FIG_DIR = Path(__file__).resolve().parents[1] / "report" / "figures"
REPORT_FIG_DIR.mkdir(parents=True, exist_ok=True)


def _default_save_path(basename: str, ext: str = "png") -> Path:
    slug = basename.lower().replace(" ", "_")
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    return REPORT_FIG_DIR / f"{slug}_{timestamp}.{ext}"


def plot_npaf_series(a: NDArray[np.int8], title: str, save_path: Optional[Path] = None) -> Path:
    """Plot the NPAF(a,s) curve for s>=1 and save it."""
    n = a.size
    shifts = np.arange(1, n)
    values = np.empty_like(shifts, dtype=np.int32)
    for idx, shift in enumerate(shifts):
        values[idx] = int(np.dot(a[:-shift], a[shift:]))
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(shifts, values, marker="o", linestyle="-", linewidth=1)
    ax.set_xlabel("Shift s")
    ax.set_ylabel("NPAF")
    ax.set_title(title)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.grid(True, linewidth=0.4, linestyle=":")
    path = save_path or _default_save_path(title)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path


def plot_sum_series(sum_series: NDArray[np.int32], title: str, save_path: Optional[Path] = None) -> Path:
    """Plot the sum of four NPAFs across shifts."""
    shifts = np.arange(1, sum_series.size + 1)
    fig, ax = plt.subplots(figsize=(8, 3))
    markerline, stemlines, baseline = ax.stem(shifts, sum_series)
    plt.setp(stemlines, linewidth=1.5)
    plt.setp(markerline, markersize=4)
    ax.set_xlabel("Shift s")
    ax.set_ylabel("Σ NPAF")
    ax.set_title(title)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.grid(True, linewidth=0.4, linestyle=":")
    path = save_path or _default_save_path(title)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path


__all__ = ["plot_npaf_series", "plot_sum_series", "REPORT_FIG_DIR"]
