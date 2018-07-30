#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 10:18:09 2018

@author: Eug
"""

import numpy as np
import networkx as nx
import copy
import collections
from rundmcmc.validity import fast_connected, no_vanishing_districts, Validator

class Fake_Parent:
	def __init__(self):
		self.parts = [1,2,3]
class Fake_Partition:

    def __init__(self, part,graph):
        self.assignment = dict(zip(range(25),part))
        self.parts = collections.defaultdict(set)
        for node, part in self.assignment.items():
            self.parts[part].add(node)
        self.graph = graph
        self.parent = Fake_Parent()

def valid(part):
    return Validator([fast_connected, no_vanishing_districts])(part)



enumeration_file = 'enumerated_ensemble_full.csv'
adjs_file = 'adjlist.csv'
output_file = 'results/metagraph.npy'



# each row represents a districting plan
ensemble = np.loadtxt(open(enumeration_file, 'rb'), delimiter=',')
ensemble = np.transpose(ensemble)

# Create a dictionary with each plan's tuple matched with its index in ensemble
# for quick look up
plan_indices = {}
for i in range(len(ensemble)):
    plan_indices[tuple(ensemble[i])] = i

# Load the adjacency list
adj_list = np.loadtxt(open(adjs_file, 'rb'), delimiter=',')

# Turn the adjacency list into a networkx graph
adj_matrix = np.zeros((len(adj_list), len(adj_list)))
for i in range(len(adj_list)):
    for j in adj_list[i]:
        adj_matrix[i, j] = 1
G = nx.from_numpy_matrix(adj_matrix)

# Build the metagraph
# First initialize the empty metagraph
meta_matrix = np.zeros((len(ensemble), len(ensemble)))
# For every plan
for k in range(len(ensemble)):
    # Look at all neighbors
    for i in range(len(adj_list)):
        for j in adj_list[i]:
            # If they are in different districts try a flip
            if ensemble[k][i] != ensemble[k][j]:
                temp_plan = copy.deepcopy(ensemble[k])
                temp_plan[j] = temp_plan[i]
                # If the flip results in a valid plan, then the two plans
                # are neighbors in the metagraph
                part = Fake_Partition(temp_plan, G)
                if valid(part):
                    neighbor_index = plan_indices[tuple(temp_plan)]
                    meta_matrix[k, neighbor_index] = 1
                    meta_matrix[neighbor_index, k] = 1
                    
np.save(open(output_file, 'wb'), meta_matrix)
                