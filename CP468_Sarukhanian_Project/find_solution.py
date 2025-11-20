"""Find the corrected sign configuration for the Sarukhanian construction."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.construction import get_default_plan, plan_to_sequences, verify_four_sequences
from src.exhaustive_search import simulated_annealing_search
import json

def save_working_plan(plan, filename="working_plan.json"):
    """Save a working plan to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(plan, f, indent=2)
    print(f"Saved working plan to {filename}")

def main():
    print("Starting exhaustive search for correct Sarukhanian construction...")
    print("This may take several minutes...")
    
    best_result = None
    best_score = float('inf')
    
    # Try multiple runs with different seeds and parameters
    for seed in range(20):
        print(f"\n=== Run {seed + 1}/20 (seed={seed}) ===")
        result = simulated_annealing_search(
            get_default_plan(), 
            max_iterations=100000,
            initial_temp=500.0,
            cooling_rate=0.99995
        )
        
        diag = result['diagnostics']
        score = diag['num_nonzero_shifts'] * 1000 + diag['max_abs_deviation']
        
        print(f"Result: non-zero={diag['num_nonzero_shifts']}, max_dev={diag['max_abs_deviation']}, score={score}")
        
        if score < best_score:
            best_score = score
            best_result = result
            print(f"  *** New best! ***")
            
            if diag['num_nonzero_shifts'] == 0:
                print("\n" + "="*60)
                print("✓✓✓ PERFECT SOLUTION FOUND! ✓✓✓")
                print("="*60)
                save_working_plan(best_result['plan'], "perfect_plan.json")
                print_plan_as_code(best_result['plan'])
                return best_result
    
    print("\n" + "="*60)
    print(f"Best result after all runs:")
    print(f"  Non-zero shifts: {best_result['diagnostics']['num_nonzero_shifts']}")
    print(f"  Max deviation: {best_result['diagnostics']['max_abs_deviation']}")
    print("="*60)
    
    if best_result:
        save_working_plan(best_result['plan'], "best_plan.json")
        print_plan_as_code(best_result['plan'])
    
    return best_result

def print_plan_as_code(plan):
    """Print the plan as Python code that can be copied into construction.py"""
    print("\n# Python code for the plan:")
    print("plan: PlanType = [")
    for block in plan:
        print(f'    {{"pattern": "{block["pattern"]}", "seq": "{block["seq"]}", "sign": {block["sign"]}}},')
    print("]")

if __name__ == "__main__":
    main()
