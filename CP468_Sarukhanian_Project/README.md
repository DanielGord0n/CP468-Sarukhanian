# CP468 Sarukhanian Project

## Project Goal
This project implements a verified construction of Sarukhanian's delta-codes (cyclic T-matrices) of length 110.
The construction is based on the paper "A Note on Construction of $\delta$-Codes" by A. G. Sarukhanian.

## Verification Status
**SUCCESS**: The implementation in `src/construction.py` produces four sequences of length 110 ($n=3$) whose summed Non-Periodic Autocorrelation Function (NPAF) is **exactly zero** for all non-zero shifts.

## Repository Layout
- `src/`: Core Python modules for the construction and verification.
  - `construction.py`: Defines the correct sequence plan and build logic.
  - `npaf.py`: Efficient NPAF calculation and verification utilities.
  - `sequences.py`: Base Turyn sequences and helper functions.
- `tests/`: Unit tests to ensure correctness.
- `notebooks/`: Demonstration notebooks.
- `report/`: Detailed findings and verification report.

## Quickstart
1.  Create a virtual environment: `python3 -m venv venv`
2.  Activate it: `source venv/bin/activate`
3.  Install dependencies: `pip install -r requirements.txt`
4.  Run the demo: `python demo.py`
5.  Run tests: `pytest`

## Key Findings
The original paper contained ambiguities regarding the sequence length and signs.
-   **Length:** The correct sequence has length 110 (44 blocks), achieved by repeating a specific pattern 3 times (clarified by the LaTeX source).
-   **Signs:** A specific sign configuration was found via simulated annealing to achieve zero NPAF.

See `report/report.md` for full details.
