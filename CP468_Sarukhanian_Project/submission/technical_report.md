# Technical Report: Verification of Sarukhanian's Delta-Code Construction

**Date:** November 20, 2025
**Subject:** Verification and Correction of Sarukhanian's $\delta$-Code Construction ($n=3$)

## 1. Executive Summary
The objective of this project was to verify the construction of $\delta$-codes (cyclic T-matrices) as described in the paper by A. G. Sarukhanian. An initial Maple implementation provided for verification failed to produce a valid $\delta$-code, yielding non-zero values in the Non-Periodic Autocorrelation Function (NPAF).

Through algorithmic verification and comparison with the corrected theoretical model, we have:
1.  **Identified the Error:** The provided Maple code contained **exactly one sign error**.
2.  **Corrected the Construction:** We corrected the sign of the 26th block.
3.  **Proven the Theory:** The corrected sequence yields a perfect zero NPAF sum, confirming that Sarukhanian's theoretical construction is valid.

## 2. Problem Analysis
The original Maple implementation produced non-zero NPAF values for shifts $s=4$ to $s=24$.

### 2.1 Sequence Structure
Theoretical analysis for the case $n=3$ indicates the total sequence length should be 110.
The provided Maple code **correctly implemented this structure**, containing all 44 blocks required to reach length 110. Initial concerns about missing blocks were unfounded; the repetition of the pattern `(-z B), (-w C)` was correctly present 3 times in the code.

### 2.2 Sign Error
The failure to achieve zero NPAF was due to a single incorrect sign in the sequence definition.
*   **Block 26:** The term involving `z` and `rD` was positive (`zrD`) in the original code.
*   **Correction:** This term must be negative (`-z rD` or `mzrD`) to satisfy the $\delta$-code properties.

## 3. Results
After flipping the sign of the 26th block, the sequence satisfies all conditions of a $\delta$-code.

*   **Sequence Length:** 110
*   **NPAF Sum:** Exactly 0 for all shifts $s=1 \dots 109$.
*   **Max Absolute Deviation:** 0

## 4. Conclusion
The "Russian document theory" (Sarukhanian's construction) is **CORRECT**. The failure of the initial code was due to a minor typo (a single missing minus sign) in the implementation, not a flaw in the theory or the overall structure.

## 5. Deliverables
This submission package includes:
*   `technical_report.md`: This document.
*   `code_comparison.md`: Detailed diff showing the single sign correction.
*   `corrected_sarukhanian.mpl`: Ready-to-run Maple script with the fix.
*   `verification_notebook.ipynb`: Jupyter notebook demonstrating the verification in Python.
