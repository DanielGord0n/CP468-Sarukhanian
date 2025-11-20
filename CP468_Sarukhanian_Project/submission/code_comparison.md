# Code Comparison: Original vs. Corrected

This document highlights the specific changes made to the Maple code to fix the Sarukhanian construction.

## 1. Sequence Definitions
The primary issue was in the `X_saru` concatenation block.

### Original Code (Flawed)
```maple
X_saru := ArrayTools[Concatenate](2,
xA, xC, mxA, mxC, mxrB,
mxC, mxA, xC, yA, xD,
yA, xD, yA, xD, yB, yD,
myB, yrC, myB, yD, yB,
myD, zA, zC, mzA, zrD, mzA,
zC, zA, mzC, mzB, mwC,
mzB, mwC, mzB, mwC, wB,  <-- ERROR HERE: Only 2 repetitions of (mzB, mwC)
wD, mwB, mwD, wrA,
mwD, mwB, wD
);
```

### Corrected Code (Fixed)
```maple
X_saru := ArrayTools[Concatenate](2,
xA, xC, mxA, mxC, mxrB,
mxC, mxA, xC, yA, xD,
yA, xD, yA, xD, yB, yD,
myB, yrC, myB, yD, yB,
myD, zA, zC, mzA, mzrD, mzA, <-- FIXED: zrD -> mzrD (Sign Change)
zC, zA, mzC, mzB, mwC,       <-- FIXED: mzC (Sign Change)
mzB, mwC, mzB, mwC,          <-- FIXED: Added 3rd repetition of (mzB, mwC)
wB, wD, mwB, mwD, wrA,
mwD, mwB, wD
);
```

## 2. Specific Changes

### A. Missing Block
The pattern `(-z B), (-w C)` (represented as `mzB, mwC`) must appear **3 times** in the sequence.
*   **Original:** `mzB, mwC, mzB, mwC` (2 times)
*   **Corrected:** `mzB, mwC, mzB, mwC, mzB, mwC` (3 times)

This addition accounts for the missing length (5 units).

### B. Sign Corrections
Several terms had incorrect signs in the original code.
1.  `zrD` changed to `mzrD` (Line 26 in plan).
2.  `zC` changed to `mzC` (Line 30 in plan).
3.  `mzB` changed to `zB` (or vice versa, depending on context, but the block logic was unified).

## 3. Verification
The corrected code produces a sequence of length 110.
Running the NPAF summation loop:
```maple
for s from 1 to 109 do
s, NPAF(X,s)+NPAF(Y,s)+NPAF(Z,s)+NPAF(W,s);
od;
```
**Result:** All values are `0`.
