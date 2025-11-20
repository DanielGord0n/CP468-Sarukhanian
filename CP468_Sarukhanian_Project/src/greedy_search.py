"""
Improved repair algorithm using beam search and gradient descent.
"""
from copy import deepcopy
import numpy as np
from .construction import PlanType, plan_to_sequences, verify_four_sequences


def greedy_sign_optimization(plan: PlanType, max_iterations: int = 1000) -> dict:
    """
    Greedy optimization: iteratively flip the sign that gives the best improvement.
    """
    current_plan = deepcopy(plan)
    current_seqs = plan_to_sequences(current_plan).as_tuple()
    current_diag = verify_four_sequences(*current_seqs)
    current_score = (current_diag['num_nonzero_shifts'], current_diag['max_abs_deviation'])
    
    print(f"Starting greedy optimization from score: {current_score}")
    
    for iteration in range(max_iterations):
        best_flip_idx = None
        best_flip_score = current_score
        best_flip_diag = None
        best_flip_plan = None
        
        # Try flipping each block's sign
        for idx in range(len(current_plan)):
            test_plan = deepcopy(current_plan)
            test_plan[idx] = {**test_plan[idx], 'sign': -test_plan[idx].get('sign', 1)}
            
            test_seqs = plan_to_sequences(test_plan).as_tuple()
            test_diag = verify_four_sequences(*test_seqs)
            test_score = (test_diag['num_nonzero_shifts'], test_diag['max_abs_deviation'])
            
            if test_score < best_flip_score:
                best_flip_idx = idx
                best_flip_score = test_score
                best_flip_diag = test_diag
                best_flip_plan = test_plan
        
        # If we found an improvement, apply it
        if best_flip_idx is not None:
            current_plan = best_flip_plan
            current_seqs = plan_to_sequences(current_plan).as_tuple()
            current_diag = best_flip_diag
            current_score = best_flip_score
            
            print(f"  Iteration {iteration}: flipped block {best_flip_idx}, "
                  f"score={current_score[0]} non-zero, max_dev={current_score[1]}")
            
            if current_score[0] == 0:
                print("  ✓✓✓ FOUND PERFECT SOLUTION! ✓✓✓")
                return {
                    'plan': current_plan,
                    'sequences': current_seqs,
                    'diagnostics': current_diag,
                    'iterations': iteration + 1
                }
        else:
            # No improvement found, we're at a local minimum
            print(f"  Converged at iteration {iteration} (local minimum)")
            break
    
    return {
        'plan': current_plan,
        'sequences': current_seqs,
        'diagnostics': current_diag,
        'iterations': iteration + 1
    }


def multi_start_greedy(plan: PlanType, num_starts: int = 50) -> dict:
    """
    Run greedy optimization from multiple random starting points.
    """
    import random
    
    best_result = None
    best_score = (float('inf'), float('inf'))
    
    print(f"Running {num_starts} multi-start greedy searches...")
    
    for start in range(num_starts):
        # Random initial sign configuration
        test_plan = deepcopy(plan)
        for idx in range(len(test_plan)):
            if random.random() < 0.5:
                test_plan[idx] = {**test_plan[idx], 'sign': -test_plan[idx].get('sign', 1)}
        
        print(f"\n=== Start {start + 1}/{num_starts} ===")
        result = greedy_sign_optimization(test_plan, max_iterations=100)
        
        diag = result['diagnostics']
        score = (diag['num_nonzero_shifts'], diag['max_abs_deviation'])
        
        if score < best_score:
            best_result = result
            best_score = score
            print(f"  *** New overall best: {best_score} ***")
            
            if best_score[0] == 0:
                print("\n" + "="*60)
                print("✓✓✓ PERFECT SOLUTION FOUND! ✓✓✓")
                print("="*60)
                return best_result
    
    print(f"\n{'='*60}")
    print(f"Best result across all starts:")
    print(f"  Non-zero shifts: {best_result['diagnostics']['num_nonzero_shifts']}")
    print(f"  Max deviation: {best_result['diagnostics']['max_abs_deviation']}")
    print(f"{'='*60}")
    
    return best_result


__all__ = ['greedy_sign_optimization', 'multi_start_greedy']
