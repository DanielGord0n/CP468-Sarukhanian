
import sys
from pathlib import Path
import numpy as np

# Add current directory to path
sys.path.insert(0, str(Path(".").resolve()))

from src.sequences import get_sequence
from src.npaf import npaf_all_shifts

def check_turyn():
    A = get_sequence("A")
    B = get_sequence("B")
    C = get_sequence("C")
    D = get_sequence("D")
    
    print(f"A: {A}")
    print(f"B: {B}")
    print(f"C: {C}")
    print(f"D: {D}")
    
    # Check lengths
    print(f"Lengths: A={A.size}, B={B.size}, C={C.size}, D={D.size}")
    
    # Calculate NPAFs
    nA = npaf_all_shifts(A)
    nB = npaf_all_shifts(B)
    nC = npaf_all_shifts(C)
    nD = npaf_all_shifts(D)
    
    print(f"NPAF(A): {nA}")
    print(f"NPAF(B): {nB}")
    print(f"NPAF(C): {nC}")
    print(f"NPAF(D): {nD}")
    
    # Turyn sequences definition varies.
    # Definition 1: A, B, C, D are complementary, i.e., sum of NPAFs is 0.
    # But C, D have different lengths?
    # If lengths differ, we can only sum up to min length.
    
    min_len = min(A.size, B.size, C.size, D.size)
    sum_npaf = np.zeros(min_len - 1, dtype=np.int32)
    
    for s in range(min_len - 1):
        sum_npaf[s] = nA[s] + nB[s] + nC[s] + nD[s]
        
    print(f"Sum NPAF (up to shift {min_len-1}): {sum_npaf}")
    
    if np.all(sum_npaf == 0):
        print("Base sequences are complementary (sum NPAF = 0).")
    else:
        print("Base sequences are NOT complementary.")

if __name__ == "__main__":
    check_turyn()
