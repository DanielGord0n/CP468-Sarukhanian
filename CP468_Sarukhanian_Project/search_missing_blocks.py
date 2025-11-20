
import sys
from pathlib import Path
import numpy as np
from copy import deepcopy

# Add current directory to path
sys.path.insert(0, str(Path(".").resolve()))

from src.construction import plan_to_sequences, verify_four_sequences
from src.sequences import get_sequence, get_pattern

def get_transcribed_plan():
    # Transcription of X from Image 2
    return [
        # Line 1
        {"pattern": "x", "seq": "A", "sign": 1},
        {"pattern": "x", "seq": "C", "sign": 1},
        {"pattern": "x", "seq": "A", "sign": -1},
        {"pattern": "x", "seq": "C", "sign": -1},
        {"pattern": "x", "seq": "rB", "sign": -1},
        
        # Line 2
        {"pattern": "x", "seq": "C", "sign": -1},
        {"pattern": "x", "seq": "A", "sign": -1},
        {"pattern": "x", "seq": "C", "sign": 1},
        {"pattern": "y", "seq": "A", "sign": 1},
        {"pattern": "x", "seq": "D", "sign": 1},
        
        # Line 3
        {"pattern": "y", "seq": "A", "sign": 1},
        {"pattern": "x", "seq": "D", "sign": 1},
        {"pattern": "y", "seq": "A", "sign": 1},
        {"pattern": "x", "seq": "D", "sign": 1},
        {"pattern": "y", "seq": "B", "sign": 1},
        {"pattern": "y", "seq": "D", "sign": 1},
        
        # Line 4
        {"pattern": "y", "seq": "B", "sign": -1},
        {"pattern": "y", "seq": "rC", "sign": 1},
        {"pattern": "y", "seq": "B", "sign": -1},
        {"pattern": "y", "seq": "D", "sign": 1},
        {"pattern": "y", "seq": "B", "sign": 1},
        
        # Line 5
        {"pattern": "y", "seq": "D", "sign": -1},
        {"pattern": "z", "seq": "A", "sign": 1},
        {"pattern": "z", "seq": "C", "sign": 1},
        {"pattern": "z", "seq": "A", "sign": -1},
        {"pattern": "z", "seq": "rD", "sign": 1},
        {"pattern": "z", "seq": "A", "sign": -1},
        
        # Line 6
        {"pattern": "z", "seq": "C", "sign": 1},
        {"pattern": "z", "seq": "A", "sign": 1},
        {"pattern": "z", "seq": "C", "sign": -1},
        {"pattern": "z", "seq": "B", "sign": -1},
        {"pattern": "w", "seq": "C", "sign": -1},
        
        # Line 7
        {"pattern": "z", "seq": "B", "sign": -1},
        {"pattern": "w", "seq": "C", "sign": -1},
        {"pattern": "w", "seq": "B", "sign": 1},
        
        # Line 8
        {"pattern": "w", "seq": "D", "sign": 1},
        {"pattern": "w", "seq": "B", "sign": -1},
        {"pattern": "w", "seq": "D", "sign": -1},
        {"pattern": "w", "seq": "rA", "sign": 1},
        
        # Line 9
        {"pattern": "w", "seq": "D", "sign": -1},
        {"pattern": "w", "seq": "B", "sign": -1},
        {"pattern": "w", "seq": "D", "sign": 1},
    ]

def main():
    base_plan = get_transcribed_plan()
    print(f"Base plan length: {len(base_plan)}")
    
    patterns = ["x", "y", "z", "w"]
    l_seqs = ["A", "B", "rA", "rB"]
    s_seqs = ["C", "D", "rC", "rD"]
    signs = [1, -1]
    
    best_score = float('inf')
    best_plan = None
    
    # Try inserting L then S
    print("Searching for missing L, S blocks...")
    
    # Optimization: Only check positions where L/S alternation is preserved?
    # The base plan has L, S, L, S... perfect alternation.
    # So we must insert (L, S) at an odd index (after an S) or (S, L) at an even index?
    # Wait, if we insert (L, S) anywhere, we shift everything by 2, so parity is preserved.
    # But we want to preserve the local alternation L, S, L, S.
    # So we should insert (L, S) after an S (or at start).
    # Or insert (S, L) after an L.
    
    # Let's just try all positions and check alternation.
    
    count = 0
    for i in range(len(base_plan) + 1):
        # Try inserting L, S
        for p1 in patterns:
            for s1 in l_seqs:
                for sn1 in signs:
                    block1 = {"pattern": p1, "seq": s1, "sign": sn1}
                    
                    for p2 in patterns:
                        for s2 in s_seqs:
                            for sn2 in signs:
                                block2 = {"pattern": p2, "seq": s2, "sign": sn2}
                                
                                # Try L, S
                                new_plan = base_plan[:i] + [block1, block2] + base_plan[i:]
                                
                                # Check score
                                x, y, z, w = plan_to_sequences(new_plan).as_tuple()
                                diag = verify_four_sequences(x, y, z, w)
                                score = diag['num_nonzero_shifts']
                                
                                if score < best_score:
                                    best_score = score
                                    best_plan = new_plan
                                    print(f"New best: {score} at pos {i} with {block1}, {block2}")
                                    if score == 0:
                                        print("FOUND PERFECT SOLUTION!")
                                        return

        # Try inserting S, L
        for p1 in patterns:
            for s1 in s_seqs:
                for sn1 in signs:
                    block1 = {"pattern": p1, "seq": s1, "sign": sn1}
                    
                    for p2 in patterns:
                        for s2 in l_seqs:
                            for sn2 in signs:
                                block2 = {"pattern": p2, "seq": s2, "sign": sn2}
                                
                                # Try S, L
                                new_plan = base_plan[:i] + [block1, block2] + base_plan[i:]
                                
                                # Check score
                                x, y, z, w = plan_to_sequences(new_plan).as_tuple()
                                diag = verify_four_sequences(x, y, z, w)
                                score = diag['num_nonzero_shifts']
                                
                                if score < best_score:
                                    best_score = score
                                    best_plan = new_plan
                                    print(f"New best: {score} at pos {i} with {block1}, {block2}")
                                    if score == 0:
                                        print("FOUND PERFECT SOLUTION!")
                                        return
        
        if i % 5 == 0:
            print(f"Processed position {i}/{len(base_plan)}")

if __name__ == "__main__":
    main()
