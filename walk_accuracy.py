#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 11:34:01 2018

@author: Eug
"""

import pickle
import numpy as np
import matplotlib.pyplot as plt

def canonical_form(vector):
    wrong = list(vector)
    seen = set()
    wrong_order = [d for d in wrong if not (d in seen or seen.add(d))]
    correct_order = list(range(1, len(wrong_order) + 1))
    correction_table = dict(zip(wrong_order, correct_order))
    right = [correction_table[d] for d in wrong]
    return right

efficiency_gap_file = 'data/full_enum_efficiency_gap_paired_with_partitions.p'
walk_files = [
'data/many_single_flip_1million.p'
        ]
output_folder = 'results/many_single_flip_1million/'

# Load the efficiency gap of every plan
all_gap = pickle.load(open(efficiency_gap_file, 'rb'))
# Convert the plans from using numerals to numbers
for i in range(len(all_gap)):
    dist = list(all_gap[i][0])
    for j in range(len(dist)):
        dist[j] = int(dist[j])
    dist = tuple(dist)
    all_gap[i] = (dist, all_gap[i][1])

# Load the walks
walks = []
for i in walk_files:
    walks.append(pickle.load(open(i, 'rb')))
    
# Put the walks into canonical_form
for i in walks:
    for j in range(len(i)):
        i[j] = tuple(canonical_form(i[j]))
        
# Create a dictionary to reference the efficiency gap of each plan
gaps = {}
for i in all_gap:
    gaps[i[0]] = i[1]

# Create a list of all the efficiency gaps of the full enumeration    
full_gaps = gaps.values()

# Create lists of the efficiency gaps at all the steps in each walk
walks_gaps = []
for i in range(len(walks)):
    walks_gaps.append([])
    for dist in walks[i]:
        walks_gaps[i].append(gaps[dist])
        
#Make histogram 
fig = plt.figure()
x = [list(gaps.values())] + walks_gaps
for i in range(len(x)):
    x[i] = np.asarray(x[i])
num_bins = 40


n, bins, patches = plt.hist(x, num_bins)
plt.title('Efficiency Gap Distributions')
plt.xlabel('Efficiency Gap')
plt.ylabel('Number of Appearences')
print("n = ")
print(n)
plt.show()
#fig.savefig(output_folder + "histogram.png")


# Make plot showing relations of histogram
fig2 = plt.figure()

# normalize n
for i in range(len(n)):
    for j in range(len(n[i])):
        n[i][j] = n[i][j] / len(x[i])
    
# For every bin, average the walks numbers and divide by enumeration number
x = []
for i in range(len(n[0])):
    total_found = 0
    for j in range(1, len(n)):
        total_found += n[j][i]
    ave_found = total_found / (len(n) - 1)
    x.append(ave_found / n[0][i])
x = np.asarray(x)

plt.plot(x)
plt.title('Averaged # of appearences found over # in enumeration')
plt.xlabel('bin number')
plt.ylabel('average # appearences found / # in enumeration')
print('normalization: ')
print(x)
plt.show()
#fig2.savefig(output_folder + 'normalization.png')
        
        
    

    
            
        