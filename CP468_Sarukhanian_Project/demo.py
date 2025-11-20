
import sys
from pathlib import Path
import numpy as np

# Add current directory to path
sys.path.insert(0, str(Path(".").resolve()))

from src.construction import build_sarukhanian_110, verify_four_sequences

def main():
    print("="*60)
    print("Sarukhanian Delta-Code Construction Demo")
    print("="*60)
    
    print("\n1. Building sequences...")
    try:
        x, y, z, w = build_sarukhanian_110()
        print("   Success! Sequences built.")
    except Exception as e:
        print(f"   Error: {e}")
        return

    print(f"\n2. Verifying properties (Length should be 110)...")
    diag = verify_four_sequences(x, y, z, w)
    
    print(f"   Sequence Length: {diag['length']}")
    print(f"   Non-zero NPAF shifts: {diag['num_nonzero_shifts']}")
    print(f"   Max Absolute Deviation: {diag['max_abs_deviation']}")
    
    print("\n3. Result:")
    if diag['num_nonzero_shifts'] == 0:
        print("   ✅ PERFECT! The sequences form a valid delta-code.")
        print("   Sum of NPAF is zero for all s=1..109.")
    else:
        print("   ❌ FAILED. Non-zero NPAF detected.")
        
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
