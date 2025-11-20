"""Exhaustive search for correct Sarukhanian construction."""
import numpy as np
from itertools import product
from .construction import PlanType, plan_to_sequences, verify_four_sequences, get_default_plan


def exhaustive_sign_search(plan: PlanType, max_configs: int = 100000) -> dict:
    """
    Try different sign configurations exhaustively.
    With 44 blocks, we have 2^44 possibilities which is too many.
    Instead, use a greedy approach: flip signs one at a time, keep improvements.
    """
    best_plan = plan.copy()
    best_seqs = plan_to_sequences(best_plan).as_tuple()
    best_diag = verify_four_sequences(*best_seqs)
    best_score = (best_diag['num_nonzero_shifts'], best_diag['max_abs_deviation'])
    
    improved = True
    iterations = 0
    
    while improved and iterations < max_configs:
        improved = False
        iterations += 1
        
        # Try flipping each sign individually
        for idx in range(len(best_plan)):
            test_plan = best_plan.copy()
            test_plan[idx] = {**test_plan[idx], 'sign': -test_plan[idx].get('sign', 1)}
            
            test_seqs = plan_to_sequences(test_plan).as_tuple()
            test_diag = verify_four_sequences(*test_seqs)
            test_score = (test_diag['num_nonzero_shifts'], test_diag['max_abs_deviation'])
            
            if test_score < best_score:
                best_plan = test_plan
                best_seqs = test_seqs
                best_diag = test_diag
                best_score = test_score
                improved = True
                print(f"  Iteration {iterations}: flipped block {idx}, score now {best_score}")
                
                if best_score == (0, 0):
                    print("  ✓ Found perfect solution!")
                    return {
                        'plan': best_plan,
                        'sequences': best_seqs,
                        'diagnostics': best_diag,
                        'iterations': iterations
                    }
                break  # Start over from the beginning with the improved plan
    
    return {
        'plan': best_plan,
        'sequences': best_seqs,
        'diagnostics': best_diag,
        'iterations': iterations
    }


def simulated_annealing_search(plan: PlanType, max_iterations: int = 50000, 
                                initial_temp: float = 100.0, cooling_rate: float = 0.995) -> dict:
    """Use simulated annealing to find better sign configurations."""
    import random
    from math import exp
    
    current_plan = plan.copy()
    current_seqs = plan_to_sequences(current_plan).as_tuple()
    current_diag = verify_four_sequences(*current_seqs)
    current_score = current_diag['num_nonzero_shifts'] * 1000 + current_diag['max_abs_deviation']
    
    best_plan = current_plan.copy()
    best_score = current_score
    best_diag = current_diag
    best_seqs = current_seqs
    
    temp = initial_temp
    
    for iteration in range(max_iterations):
        # Cool down
        temp *= cooling_rate
        
        # Random modification: flip a random sign
        test_plan = current_plan.copy()
        flip_idx = random.randint(0, len(test_plan) - 1)
        test_plan[flip_idx] = {**test_plan[flip_idx], 'sign': -test_plan[flip_idx].get('sign', 1)}
        
        test_seqs = plan_to_sequences(test_plan).as_tuple()
        test_diag = verify_four_sequences(*test_seqs)
        test_score = test_diag['num_nonzero_shifts'] * 1000 + test_diag['max_abs_deviation']
        
        # Accept if better, or with probability based on temperature
        delta = test_score - current_score
        if delta < 0 or (temp > 0 and random.random() < exp(-delta / temp)):
            current_plan = test_plan
            current_seqs = test_seqs
            current_diag = test_diag
            current_score = test_score
            
            if current_score < best_score:
                best_plan = current_plan.copy()
                best_score = current_score
                best_diag = current_diag
                best_seqs = current_seqs
                
                if iteration % 1000 == 0:
                    print(f"  Iteration {iteration}: score={best_score}, "
                          f"non-zero={best_diag['num_nonzero_shifts']}, "
                          f"max={best_diag['max_abs_deviation']}")
                
                if best_score == 0:
                    print(f"  ✓ Found perfect solution at iteration {iteration}!")
                    return {
                        'plan': best_plan,
                        'sequences': best_seqs,
                        'diagnostics': best_diag,
                        'iterations': iteration
                    }
    
    return {
        'plan': best_plan,
        'sequences': best_seqs,
        'diagnostics': best_diag,
        'iterations': max_iterations
    }


__all__ = ['exhaustive_sign_search', 'simulated_annealing_search']
