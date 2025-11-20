
import sys
from pathlib import Path
import numpy as np

# Add current directory to path
sys.path.insert(0, str(Path(".").resolve()))

from src.construction import verify_four_sequences
from src.sequences import get_sequence, get_pattern, tile_block
from src.npaf import npaf_sum_four

def build_latex_sequence():
    # Sequence X from LaTeX file
    blocks = [
        # Line 72
        ("x", "A", 1),
        ("x", "C", 1),
        ("x", "A", -1),
        ("x", "C", -1),
        ("x", "rB", -1),
        
        # Line 73
        ("x", "C", -1),
        ("x", "A", -1),
        ("x", "C", 1),
        ("y", "A", 1),
        ("x", "D", 1),
        
        # Line 74
        ("y", "A", 1),
        ("x", "D", 1),
        ("y", "A", 1),
        ("x", "D", 1),
        ("y", "B", 1),
        ("y", "D", 1),
        
        # Line 75
        ("y", "B", -1),
        ("y", "rC", 1),
        ("y", "B", -1),
        ("y", "D", 1),
        ("y", "B", 1),
        
        # Line 76
        ("y", "D", -1),
        ("z", "A", 1),
        ("z", "C", 1),
        ("z", "A", -1),
        ("z", "rD", 1),
        ("z", "A", -1),
        
        # Line 77
        ("z", "C", 1),
        ("z", "A", 1),
        ("z", "C", -1),
        ("z", "B", -1),
        ("w", "C", -1),
        
        # Line 78
        # (-z b), (-w c), (-z b), (-w c), (w b)
        ("z", "B", -1),
        ("w", "C", -1),
        ("z", "B", -1),
        ("w", "C", -1),
        ("w", "B", 1),
        
        # Line 79
        ("w", "D", 1),
        ("w", "B", -1),
        ("w", "D", -1),
        ("w", "rA", 1),
        
        # Line 80
        ("w", "D", -1),
        ("w", "B", -1),
        ("w", "D", 1),
    ]
    
    row_blocks = [[] for _ in range(4)]
    
    print(f"Total blocks: {len(blocks)}")
    
    for pattern_name, seq_name, sign in blocks:
        pattern = get_pattern(pattern_name)
        seq = get_sequence(seq_name)
        block_values = tile_block(pattern, seq) * sign
        for idx in range(4):
            row_blocks[idx].append(block_values[idx])
            
    concatenated = tuple(np.concatenate(chunks).astype(np.int8) for chunks in row_blocks)
    return concatenated

def main():
    print("Building sequence from LaTeX transcription...")
    x, y, z, w = build_latex_sequence()
    
    print(f"Sequence length: {x.size}")
    
    diag = verify_four_sequences(x, y, z, w)
    print("\nDiagnostics:")
    print(f"Length: {diag['length']}")
    print(f"Non-zero shifts: {diag['num_nonzero_shifts']}")
    print(f"Max abs deviation: {diag['max_abs_deviation']}")
    
    if diag['num_nonzero_shifts'] == 0:
        print("\nSUCCESS! The LaTeX sequence has zero NPAF.")
    else:
        print("\nFAILURE. The LaTeX sequence has non-zero NPAF.")
        print(f"Non-zero pairs: {diag['nonzero_pairs']}")

if __name__ == "__main__":
    main()
