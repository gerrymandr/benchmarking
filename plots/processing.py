# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 11:56:01 2018

@author: Sloan
"""
import numpy as np
import pickle
from utils import canonical_form

def load_plans(ensemble_paths):
    plans_by_ensemble = dict()
    
    for (ensemble, path) in ensemble_paths.items():
        # load sampled ensemble, collect unique plans
        with open(path, 'rb') as f:
            raw_plans = pickle.load(f)
        plans = [canonical_form(plan) for plan in raw_plans]
        plans_by_ensemble[ensemble] = plans
    
    return plans_by_ensemble
    
def get_benchmark_data(plans_by_ensemble,
                       feature_table,
                       feature_hist_bins,
                       iterations_step,
                       verbose=False):
    true_hist, bin_edges = np.histogram(list(feature_table.values()),
                                        bins=feature_hist_bins,
                                        density=True)
    total_num_plans = len(feature_table)
        
    benchmarks_by_ensemble = {}
    for (ensemble, plans) in plans_by_ensemble.items():
        if verbose:
            print('computing benchmark data for ' + ensemble)
            
        features = [feature_table[plan] for plan in plans]
        hist = np.histogram(features, bins=bin_edges, density=True)[0]
        
        unique_plans = set(plans)
        set_features = [feature_table[plan] for plan in unique_plans]
        set_hist = np.histogram(set_features, bins=bin_edges, density=True)[0]
        
        hist_errors = []
        set_hist_errors = []
        exploration_counts = []
        for i in range(1, len(plans), iterations_step):
            curr_features = features[:i]
            curr_hist = np.histogram(curr_features, bins=bin_edges, density=True)[0]
            
            curr_unique_plans = set(plans[:i])
            exploration_count = len(curr_unique_plans)
            curr_set_features = set_features[:exploration_count]
            curr_set_hist = np.histogram(curr_set_features, bins=bin_edges, density=True)[0]
            
            hist_error = np.sum(np.abs(curr_hist - true_hist))
            set_hist_error = np.sum(np.abs(curr_set_hist - true_hist))
            
            hist_errors.append(hist_error)
            set_hist_errors.append(set_hist_error)
            exploration_counts.append(exploration_count)
        
        plan_freqs = {}
        for plan in plans:
            if plan in plan_freqs:
                plan_freqs[plan] += 1
            else: plan_freqs[plan] = 1
        unseen = total_num_plans - len(unique_plans)
        sorted_plan_freqs = ([0] * unseen) + sorted(plan_freqs.values())
        
        benchmarks_by_ensemble[ensemble] = {
            'hist': hist,
            'set_hist': set_hist,
            'hist_errors': hist_errors,
            'set_hist_errors': set_hist_errors,
            'sorted_plan_freqs': sorted_plan_freqs,
            'exploration_counts': exploration_counts
        }
        
    return {
        'true_hist': true_hist,
        'bin_edges': bin_edges,
        'total_num_plans': total_num_plans,
        'benchmarks_by_ensemble': benchmarks_by_ensemble,
        'iterations_step': iterations_step
    }