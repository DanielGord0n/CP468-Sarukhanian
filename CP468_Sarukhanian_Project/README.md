# CP468 Sarukhanian Project

## Project Goal
Replicate the Sarukhanian Maple construction that produces four ±1 sequences of length 110 whose summed nonperiodic autocorrelations should cancel, diagnose the current non-zero-shift bug, and provide tooling to repair it via configuration-driven tweaks.

## Quickstart
1. Create a virtual environment for Python 3.11+ and activate it.
2. Install dependencies: `pip install -r requirements.txt`.
3. Explore the interactive walkthrough: `jupyter notebook notebooks/sarukhanian.ipynb`.
4. Regenerate sequences or plots via the Python modules under `src/`.

## Repository Layout
- `src/`: reusable modules for sequences, NPAFs, construction, repair, and visualization.
- `notebooks/`: the end-to-end demonstration notebook.
- `tests/`: pytest-based verification of NPAFs, the baseline plan, and repair utilities.
- `report/`: outline plus generated figures saved by the notebook or scripts.

## Editing the Block Plan
`src/construction.py` defines a configuration-driven block plan for the Maple translation. Adjust the list of block dictionaries or use helpers from `src/repair.py` to flip signs, swap blocks, or kick off a stochastic local search. Whenever you change the plan, rerun the notebook or `pytest -q` to ensure diagnostics and tests stay green.

## Running Tests
From the repository root (`CP468_Sarukhanian_Project/`):
```
pytest -q
```
This validates NPAF math, ensures the baseline sequences exhibit the known bug, and smoke-tests the repair API.
