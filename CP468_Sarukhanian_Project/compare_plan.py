
import sys
from pathlib import Path
sys.path.insert(0, str(Path(".").resolve()))

from src.construction import get_default_plan, plan_to_sequences, verify_four_sequences
from src.sequences import get_sequence

def format_block(block):
    sign = "+" if block["sign"] == 1 else "-"
    return f"{sign}{block['pattern']}{block['seq']}"

def main():
    plan = get_default_plan()
    print(f"Total blocks in plan: {len(plan)}")
    
    print("\nPlan blocks:")
    for i, block in enumerate(plan):
        seq = block['seq']
        is_long = seq in ['A', 'B', 'rA', 'rB']
        ls = "L" if is_long else "S"
        print(f"{i+1}: {format_block(block)} ({ls})")
        
    # Verify sequences
    x, y, z, w = plan_to_sequences(plan).as_tuple()
    diag = verify_four_sequences(x, y, z, w)
    print("\nDiagnostics:")
    print(f"Length: {diag['length']}")
    print(f"Non-zero shifts: {diag['num_nonzero_shifts']}")
    print(f"Non-zero pairs (first 10): {diag['nonzero_pairs']}")
    
    # Check specific range 4-24
    sum_series = diag['sum_series']
    print("\nChecking shifts 4-24:")
    for s in range(4, 25):
        if s <= len(sum_series):
            val = sum_series[s-1] # shift s is index s-1
            if val != 0:
                print(f"Shift {s}: {val}")
        else:
            print(f"Shift {s}: out of bounds")

if __name__ == "__main__":
    main()
