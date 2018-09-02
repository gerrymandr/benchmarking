# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 14:56:26 2018
@author: Sloan

This is the main script for producing benchmark plots, divided into labeled sections. Several sampled ensembles are compared to a fully enumerated ensemble according to a chosen feature.
"""
import numpy as np
import pickle
from processing import load_plans, get_benchmark_data
from plots import plot_exploration_benchmarks, plot_mixing_benchmarks
from utils import entropy, get_dem_seat_share
    
#%% settings
graph_name = '25 Node Florida Precinct Graph'
demographic_data_path = 'data/demographic_data.csv'
full_ensemble_path = 'data/full_ensemble.p'
sampled_ensemble_paths = {
    'not lazy': 'data/sampled_ensembles/single_flip/not_lazy_1mill.p',
    'wes lazy': 'data/sampled_ensembles/single_flip/wes_lazy_1mill.p',
    'real degree lazy': 'data/sampled_ensembles/single_flip/real_degree_1mill.p'
}
feature = entropy
feature_name = 'Partition Entropy'
feature_axis_label = 'Entropy'
# the following settings are really the only manual part of the plotting process
# feature_hist_bins is the bins argument for the histogram function, fiddle around with this
# iterations_step is the number of iterations skipped between points plotted on running error and exploration charts
# (computing at each iteration is unnecessary and slow)
feature_hist_bins = np.linspace(-75,-50,15)
iterations_step = 100000

#%% load full ensemble and demographic data
with open(full_ensemble_path, 'rb') as f:
    all_plans = pickle.load(f)

with open(demographic_data_path, 'rb') as f:
    demographic_data = np.loadtxt(f, delimiter=',', skiprows=1)
dems = demographic_data[:,1]
reps = demographic_data[:,2]

#%% load sampled ensemble plans
plans_by_ensemble = load_plans(sampled_ensemble_paths)

#%% compute feature for all plans
feature_table = dict([(plan, feature(plan, dems, reps)) for plan in all_plans])

#%% compute data to plot
benchmark_data = get_benchmark_data(plans_by_ensemble,
                                    feature_table,
                                    feature_hist_bins,
                                    iterations_step, verbose=True)

#%% create exploration plots
plot_exploration_benchmarks(benchmark_data, graph_name,
                            feature_name, feature_axis_label)
plot_mixing_benchmarks(benchmark_data, graph_name,
                       feature_name, feature_axis_label)