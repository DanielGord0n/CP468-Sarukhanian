
import sys
from pathlib import Path
import numpy as np

# Add current directory to path to import src modules
sys.path.insert(0, str(Path(".").resolve()))

from src.sequences import get_sequence, get_pattern, tile_block
from src.construction import verify_four_sequences
from src.npaf import npaf_sum_four

def build_paper_sequence():
    # Transcription of X from Image 2
    # Format: (pattern, sequence_name, sign)
    # Note: 
    # a_i -> A
    # b_i -> B
    # c_i -> C
    # d_i -> D
    # a_{n-i+1} -> rA (reverse A)
    # b_{n-i+1} -> rB
    # c_{n-i} -> rC (Note: c is length n-1, indices 1..n-1. i=1->n-1, i=n-1->1. So reverse)
    # d_{n-i} -> rD
    
    # The list of blocks from transcription
    blocks = [
        # Line 1
        ("x", "A", 1),
        ("x", "C", 1),
        ("x", "A", -1),
        ("x", "C", -1),
        ("x", "rB", -1), # -x b_{n-i+1}
        
        # Line 2
        ("x", "C", -1),
        ("x", "A", -1),
        ("x", "C", 1),
        ("y", "A", 1),
        ("x", "D", 1),
        
        # Line 3
        ("y", "A", 1),
        ("x", "D", 1),
        ("y", "A", 1),
        ("x", "D", 1),
        ("y", "B", 1),
        ("y", "D", 1),
        
        # Line 4
        ("y", "B", -1),
        ("y", "rC", 1), # y c_{n-i}
        ("y", "B", -1),
        ("y", "D", 1),
        ("y", "B", 1),
        
        # Line 5
        ("y", "D", -1),
        ("z", "A", 1),
        ("z", "C", 1),
        ("z", "A", -1),
        ("z", "rD", 1), # z d_{n-i}
        ("z", "A", -1),
        
        # Line 6
        ("z", "C", 1),
        ("z", "A", 1),
        ("z", "C", -1),
        ("z", "B", -1),
        ("w", "C", -1),
        
        # Line 7
        ("z", "B", -1),
        ("w", "C", -1),
        ("w", "B", 1),
        
        # Line 8
        ("w", "D", 1),
        ("w", "B", -1),
        ("w", "D", -1),
        ("w", "rA", 1), # w a_{n-i+1}
        
        # Line 9
        ("w", "D", -1),
        ("w", "B", -1),
        ("w", "D", 1),
    ]
    
    row_blocks = [[] for _ in range(4)]
    
    print(f"Total blocks: {len(blocks)}")
    
    for pattern_name, seq_name, sign in blocks:
        pattern = get_pattern(pattern_name)
        seq = get_sequence(seq_name)
        
        # Tile and apply sign
        block_values = tile_block(pattern, seq) * sign
        
        for idx in range(4):
            row_blocks[idx].append(block_values[idx])
            
    concatenated = tuple(np.concatenate(chunks).astype(np.int8) for chunks in row_blocks)
    return concatenated

def main():
    print("Building sequence from paper transcription...")
    x, y, z, w = build_paper_sequence()
    
    print(f"Sequence length: {x.size}")
    
    # Expected length: 44n - 22. For n=3 (default in sequences.py? No, sequences.py has fixed arrays)
    # sequences.py: A,B len 3. C,D len 2.
    # n=3.
    # Expected: 44*3 - 22 = 132 - 22 = 110.
    
    diag = verify_four_sequences(x, y, z, w)
    print("\nDiagnostics:")
    print(f"Length: {diag['length']}")
    print(f"Non-zero shifts: {diag['num_nonzero_shifts']}")
    print(f"Max abs deviation: {diag['max_abs_deviation']}")
    
    if diag['num_nonzero_shifts'] == 0:
        print("\nSUCCESS! The paper's sequence has zero NPAF.")
    else:
        print("\nFAILURE. The paper's sequence has non-zero NPAF.")
        print(f"Non-zero pairs: {diag['nonzero_pairs']}")

if __name__ == "__main__":
    main()
