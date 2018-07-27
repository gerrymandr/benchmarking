# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 11:59:07 2018

@author: Sloan
"""

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import matplotlib._color_data as mcd
import numpy as np

plot_colors = mcd.TABLEAU_COLORS.keys()

def plot_hist_outline(ax, hist, bin_edges, color, label):
    ax.plot([bin_edges[0], bin_edges[0]], [0, hist[0]],
            color, label=label)
    for i in range(len(hist)):
        bin_count = hist[i]
        ax.plot([bin_edges[i], bin_edges[i+1]],
                [bin_count, bin_count], color)
        if i > 0: 
            prev_bin_count = hist[i-1]
            ax.plot([bin_edges[i], bin_edges[i]],
                    [prev_bin_count, bin_count], color)
    ax.plot([bin_edges[-1], bin_edges[-1]],
            [hist[-1], 0], color)

def configure_exploration_axes(graph_name,
                               feature_name,
                               feature_axis_label,
                               iterations_step):
    grid = gridspec.GridSpec(2, 2)
    fig = plt.figure()
    exploration_counts_ax = plt.subplot(grid[0,0])
    hist_error_ax = plt.subplot(grid[0,1])
    feature_hist_ax = plt.subplot(grid[1,:])
    fig.suptitle('Exploration Benchmarks for ' + graph_name)
    
    # label unique plan counts axes
    exploration_counts_ax.set_title('Exploration Counts')
    exploration_counts_ax.set_xlabel('# iterations (x' + str(iterations_step) + ')')
    exploration_counts_ax.set_ylabel('# uniquej plans visited')
    
    # label histogram error axes
    hist_error_ax.set_title('Running ' + feature_name + ' Histogram Error')
    hist_error_ax.set_xlabel('# iterations (x' + str(iterations_step) + ')')
    hist_error_ax.set_ylabel('L1 distance to true distribution')
    
    # label feature histogram axes
    feature_hist_ax.set_title(feature_name + ' Histogram for Unique Plans Visited')
    feature_hist_ax.set_xlabel(feature_axis_label)
    feature_hist_ax.set_ylabel('Relative Frequency')
    
    return exploration_counts_ax, hist_error_ax, feature_hist_ax

def plot_exploration_benchmarks(benchmark_data, graph_name,
                                feature_name, feature_axis_label):
    bin_edges = benchmark_data['bin_edges']
    bin_widths = [t - s for s, t in zip(bin_edges, bin_edges[1:])]
    total_num_plans = benchmark_data['total_num_plans']
    benchmarks_by_ensemble = benchmark_data['benchmarks_by_ensemble']
    iterations_step = benchmark_data['iterations_step']
    
    exploration_counts_ax, hist_error_ax, feature_hist_ax =\
        configure_exploration_axes(graph_name, feature_name,
                                   feature_axis_label, iterations_step)
        
    exploration_counts_ax.axhline(y=total_num_plans,
                                  color=(0,0,0,0.3), linestyle='dashed',
                                  label='total # distinct plans')
    centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    feature_hist_ax.bar(centers, benchmark_data['true_hist'], width=bin_widths,
                        color=(0,0,0,0.3), label='true distribution')
    
    
    ensembles = list(benchmarks_by_ensemble.keys())
    color_by_ensemble = dict(zip(ensembles, plot_colors))
    max_error = 0
    
    for ensemble in ensembles:
        color = color_by_ensemble[ensemble]
        benchmarks = benchmarks_by_ensemble[ensemble]
        
        # plot exploration counts
        exploration_counts = benchmarks['exploration_counts']
        exploration_counts_ax.plot(exploration_counts, color, label=ensemble)
        
        # plot set histogram
        set_hist = benchmarks['set_hist']
        plot_hist_outline(feature_hist_ax, set_hist, bin_edges, color, ensemble)
        
        # plot histogram errors
        set_hist_errors = benchmarks['set_hist_errors']
        hist_error_ax.plot(set_hist_errors, color, label=ensemble)
        max_error = max(max_error, np.max(set_hist_errors[1:]))
    
    # adjust scaling and limits
    exploration_counts_ax.autoscale(axis='x', tight=True)
    hist_error_ax.autoscale(axis='x', tight=True)
    hist_error_ax.set_ylim([0, max_error])
    
    # add legends
    exploration_counts_ax.legend()
    hist_error_ax.legend()
    feature_hist_ax.legend()
      
def configure_mixing_axes(graph_name,
                          feature_name,
                          feature_axis_label,
                          iterations_step):
    grid = gridspec.GridSpec(2, 2)
    fig = plt.figure()
    plan_freqs_ax = plt.subplot(grid[0,0])
    hist_error_ax = plt.subplot(grid[0,1])
    feature_hist_ax = plt.subplot(grid[1,:])
    fig.suptitle('Mixing Benchmarks for ' + graph_name)
    
    # label plan counts axes
    plan_freqs_ax.set_title('Sorted Plan Frequencies')
    plan_freqs_ax.set_xlabel('plan')
    plan_freqs_ax.set_ylabel('log(1 + # occurences)')
    
    # label histogram error axes
    hist_error_ax.set_title('Running ' + feature_name + ' Histogram Error')
    hist_error_ax.set_xlabel('# iterations (x' + str(iterations_step) + ')')
    hist_error_ax.set_ylabel('L1 distance to true distribution')
    
    # label feature histogram axes
    feature_hist_ax.set_title(feature_name + ' Histogram for All Plans Visited')
    feature_hist_ax.set_xlabel(feature_axis_label)
    feature_hist_ax.set_ylabel('Relative Frequency')
    
    return plan_freqs_ax, hist_error_ax, feature_hist_ax
    
def plot_mixing_benchmarks(benchmark_data, graph_name,
                           feature_name, feature_axis_label):
    bin_edges = benchmark_data['bin_edges']
    bin_widths = [t - s for s, t in zip(bin_edges, bin_edges[1:])]
    benchmarks_by_ensemble = benchmark_data['benchmarks_by_ensemble']
    iterations_step = benchmark_data['iterations_step']
    
    plan_freqs_ax, hist_error_ax, feature_hist_ax =\
        configure_mixing_axes(graph_name, feature_name,
                                   feature_axis_label, iterations_step)

    centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    feature_hist_ax.bar(centers, benchmark_data['true_hist'], width=bin_widths,
                        color=(0,0,0,0.3), label='true distribution')
    
    
    ensembles = list(benchmarks_by_ensemble.keys())
    color_by_ensemble = dict(zip(ensembles, plot_colors))
    max_error = 0
    
    for ensemble in ensembles:
        color = color_by_ensemble[ensemble]
        benchmarks = benchmarks_by_ensemble[ensemble]
        
        # plot sorted plan frequencies
        plan_freqs = np.array(benchmarks['sorted_plan_freqs'])
        plan_freqs_ax.plot(np.log(1 + plan_freqs), color, label=ensemble)
        
        # plot set histogram
        hist = benchmarks['hist']
        plot_hist_outline(feature_hist_ax, hist, bin_edges, color, ensemble)
        
        # plot histogram errors
        hist_errors = benchmarks['hist_errors']
        hist_error_ax.plot(hist_errors, color, label=ensemble)
        max_error = max(max_error, np.max(hist_errors[1:]))
    
    # adjust scaling and limits
    plan_freqs_ax.autoscale(axis='x', tight=True)
    hist_error_ax.autoscale(axis='x', tight=True)
    hist_error_ax.set_ylim([0, max_error])
    
    # add legends
    plan_freqs_ax.legend()
    hist_error_ax.legend()
    feature_hist_ax.legend()