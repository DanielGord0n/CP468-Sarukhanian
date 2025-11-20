
import sys
from pathlib import Path
import numpy as np
import json
import random
from copy import deepcopy

# Add current directory to path
sys.path.insert(0, str(Path(".").resolve()))

from src.construction import plan_to_sequences, verify_four_sequences
from src.sequences import get_sequence, get_pattern

def get_base_plan():
    # Transcription of X from Image 2
    plan = [
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
        # INSERTED BLOCKS HERE (Pos 30 in 0-indexed list is after 29 items. 
        # Items 0-29 are the first 30 items. Item 30 is the 31st item.
        # In search_missing_blocks, pos 30 means insert before item 30.
        # Item 29 is "zB" (index 29). Item 30 is "wC" (index 30).
        # So we insert between zB and wC.
        
        # Inserted: zB (-1), wC (-1)
        {"pattern": "z", "seq": "B", "sign": -1},
        {"pattern": "w", "seq": "C", "sign": -1},
        
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
    return plan

def get_score(plan):
    x, y, z, w = plan_to_sequences(plan).as_tuple()
    diag = verify_four_sequences(x, y, z, w)
    return diag['num_nonzero_shifts'] * 1000 + diag['max_abs_deviation']

def solve():
    current_plan = get_base_plan()
    current_score = get_score(current_plan)
    
    print(f"Initial score: {current_score}")
    
    best_plan = deepcopy(current_plan)
    best_score = current_score
    
    temp = 100.0
    cooling_rate = 0.995
    
    for i in range(50000):
        # Mutate: flip a sign
        idx = random.randint(0, len(current_plan) - 1)
        
        # Create neighbor
        neighbor_plan = deepcopy(current_plan)
        neighbor_plan[idx]["sign"] *= -1
        
        neighbor_score = get_score(neighbor_plan)
        
        # Accept?
        delta = neighbor_score - current_score
        if delta < 0 or random.random() < np.exp(-delta / temp):
            current_plan = neighbor_plan
            current_score = neighbor_score
            
            if current_score < best_score:
                best_score = current_score
                best_plan = deepcopy(current_plan)
                print(f"Iter {i}: New best score {best_score}")
                if best_score == 0:
                    print("FOUND PERFECT SOLUTION!")
                    break
        
        temp *= cooling_rate
        if temp < 0.1:
            temp = 100.0 # Restart heating
            
    # Save best plan
    with open("solved_plan.json", "w") as f:
        json.dump(best_plan, f, indent=2)
        
    print("\nBest plan found:")
    for i, block in enumerate(best_plan):
        print(f"{i+1}: {block['sign']} {block['pattern']}{block['seq']}")

if __name__ == "__main__":
    solve()
