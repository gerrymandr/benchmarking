import networkx as nx
import numpy as np
import operator
import types
import sys


#This file contains various functions for calculating benchmarking data on different partitions
#of a graph. It can be used to analyze various partition formats, including chain and paritition
#objects from gerrymandr/RunDMCMC and assignment dictionaries
#
#Functions:
#
#canonical_form : converts district assignment list into canonical form partition
#dict_to_canon : converts assignment dictionary into canonical form partition
#partition_to_canon : converts partition object into canonical form partition
#chain_to_canon : converts chain object into canonical form list of partitions 
#							which most other functions accept as input
#
#eff_gap : calculates efficiency gap for a list of canonical form partitions
#dem_seats : calculates democrat majority districts for a list of canonical form partitions
#rep_seats : calculates republican majority districts for a list of canonical form partitions
#mean_med : calculates mean_median for a list of canonical form partitions
#mean_thi : calculates mean_thirdian for a list of canonical form partitions
#
#hamming_dist : calculates hamming distances between inputted list of 'towers' (partitions) and 
# 			a list of canonical form partitions
#entropy_dist : same as hamming but for entropy distance
#create_towers : generates a number of randomly generated co-distance maximizing partitions
#					intended to be used as input for hamming and entropy


#----------------------- Canonical form conversion -------------------------------------

#Takes in a vector, list, tuple etc of integers where each index maps to a node (VTD/precinct) and  the value is
#its district assignment. Changes labeling of districts such that district 1 is the first district in the input,
#district 2 is the second, etc. This doesn't change the index to unit mapping only the label of districts.
#Ex: canonical_form([3,1,2,1]) = (1,2,3,2)
#Note: index to node mapping is standardized as a least to greatest ASCII ordering by node label (usually GEOID)
def canonical_form(vector):
	wrong = list(vector)
	seen = set()
	wrong_order = [d for d in wrong if not (d in seen or seen.add(d))]
	correct_order = list(range(1, len(wrong_order) + 1))
	correction_table = dict(zip(wrong_order, correct_order))
	right = [correction_table[d] for d in wrong]
	return tuple(right)


#Converts assignment dictionary in the form {node : district} to canonical form
#assumes nodes are integer indexed from 0 to 1-num_nodes
def dict_to_canon(dict):
	return canonical_form([dict[node] for node in range(len(dict))])


#Given a partition object from gerrymandr/RunDMCMC, outputs a tuple representing the district assignments
#in canonical form
def partition_to_canon(part):
	G = nx.convert_node_labels_to_integers(part.graph, ordering = 'sorted', label_attribute = 'key')
	ordered_assign = [part.assignment[G.nodes[node]['key']] for node in range(nx.number_of_nodes(G))]
	return canonical_form(ordered_assign)


#Given a chain object from gerrymandr/RunDMCMC, outputs a list of tuples, with the ith tuple being the district
#assignments in canonical form at the ith step of that chain
def chain_to_canon(chain):
	out = list()
	G = nx.convert_node_labels_to_integers(chain.state.graph, ordering = 'sorted', label_attribute = 'key')
	for part in chain:
		ordered_assign = [part.assignment[G.nodes[node]['key']] for node in range(nx.number_of_nodes(G))]
		out.append(canonical_form(ordered_assign))
	return out


#------------------------Partisan benchmarks -------------------------------
'''
Note: all of these will accept a networkx graph  and a list of tuples
	  they will output a list of scores index-paired with the input
The tuples should hold district assignments in canonical form
The graph should have relevant attributes for population, votes, etc depending on what's necessary for 
that benchmark, and nodes should be labeled according to their correspoding index in the assignments tuple
If the graph needs to be relabeled, using nx.convert_node_lables_to_integers is advised
Ex: G = nx.convert_node_labels_to_integers(graph, ordering = 'sorted', label_attribute = 'old_label')

Attribute names are assumed to be the following, but there are optional inputs for different names:
Democrat votes: DV
Republican votes: RV
'''

#efficiency gap calculator
#requires votes by vtd for each party
#Note: wastage is calculated as democratic waste - republican waste, so a republican favoring plan
#results in a positive efficiency gap, and a democratic favoring plan results in a negative
def eff_gap(graph, partitions, dv_name = 'DV', rv_name = 'RV'):
	output = list()
	for part in partitions:
		num_dists = len(set(part))
		wasted_sum = 0
		dem_votes = [0]*num_dists
		rep_votes = [0]*num_dists
		for node in graph.nodes:
			dem_votes[part[node]-1] += graph.nodes[node][dv_name]
			rep_votes[part[node]-1] += graph.nodes[node][rv_name]
		for dist in range(num_dists):
			dv_wasted, rv_wasted = wasted_votes(dem_votes[dist], rep_votes[dist])
			wasted_sum += dv_wasted - rv_wasted
		total_votes = sum(dem_votes) + sum(rep_votes)
		output.append(wasted_sum / total_votes)
	return output


def wasted_votes(party1_votes, party2_votes):
	total_votes = party1_votes + party2_votes
	if party1_votes > party2_votes:
		party1_waste = party1_votes - total_votes / 2
		party2_waste = party2_votes
	else:
		party2_waste = party2_votes - total_votes / 2
		party1_waste = party1_votes
	return party1_waste, party2_waste


#seats won by democrats
#ties are counted as half a seat
#requires votes by vtd for each party
def dem_seats(graph, partitions, dv_name = 'DV', rv_name = 'RV'):
	output = list()
	for part in partitions:
		num_dists = len(set(part))
		dem_votes = [0]*num_dists
		rep_votes = [0]*num_dists
		for node in graph.nodes:
			dem_votes[part[node]-1] += graph.nodes[node][dv_name]
			rep_votes[part[node]-1] += graph.nodes[node][rv_name]
		output.append(sum([1 if dem_votes[dist] > rep_votes[dist] else 0 if 
			rep_votes[dist] > dem_votes[dist] else .5 for dist in range(num_dists)]))
	return output


def rep_seats(graph, partitions, dv_name = 'DV', rv_name = 'RV'):
	dem_seats_list = dem_seats(graph, partitions, dv_name, rv_name)
	return [len(set(partitions[x])) - dem_seats_list[x] for x in range(len(partitions))]


#mean median score for democrats
#requires votes by vtd for each party
#Note: a republican favoring plan results in a positive score, and a democratic favoring plan 
#results in a negative
#if you want to calculate the mean median score for republicans just put your republican
#voter attribute as dv_name and the democrat one as rv_name
#This measure is less robust in cases where one party is heavily favored
def mean_median(graph, partitions, dv_name = 'DV', rv_name = 'RV'):
	output = list()
	for part in partitions:
		num_dists = len(set(part))
		dem_totals = [0]*num_dists
		rep_totals = [0]*num_dists
		for node in graph.nodes:
			dem_totals[part[node]-1] += graph.nodes[node][dv_name]
			rep_totals[part[node]-1] += graph.nodes[node][rv_name]
		dem_vote_percents = [1.0 * dem_totals[x] / (dem_totals[x] + rep_totals[x]) for x in range(num_dists)]
		output.append(np.mean(dem_vote_percents) - np.median(dem_vote_percents))
	return output


#mean thirdian score for democrats
#requires votes by vtd for each party
def mean_thirdian(graph, partitions, dv_name = 'DV', rv_name = 'RV'):
	output = list()
	for part in partitions:
		num_dists = len(set(part))
		dem_totals = [0]*num_dists
		rep_totals = [0]*num_dists
		for node in graph.nodes:
			dem_totals[part[node]-1] += graph.nodes[node][dv_name]
			rep_totals[part[node]-1] += graph.nodes[node][rv_name]
		dem_vote_percents = [1.0 * dem_totals[x] / (dem_totals[x] + rep_totals[x]) for x in range(num_dists)]
		thirdian_index = round((len(dem_vote_percents)) / 3)
		thirdian = sorted(dem_vote_percents)[thirdian_index]
		output.append(np.mean(dem_vote_percents) - thirdian)
	return output


#----------------------------Distance calculations--------------------------------------
#These functions are designed to track movement of an MCMC method across the metagraph of all possible
#partitions. This is done by generating random partitions ('towers'), choosing a subset of them to maximize
#co-distance (so they well represent different parts of the metagraph), and tracking the distance of the 
#MCMC method to each of these towers at each step. This is similar to how cell phone towers triangulate
#position by tracking position relative to several towers, hence calling the stable partitions towers.


#calculates hamming distance between inputted towers and list of canonical form partitions
#outputs as a list of tuples. Elements of the list of index-paired to the inputted partitions,
#and elements of the tuples are index-paired to the towers.
#ex: hamming_dist(graph, partitions, towers)[5][4] = the distance between the 6th element of
#partitions and the 5th element of towers. 
def hamming_dist(graph, partitions, towers):
	output = list()
	towers = [{node : towers[x][node] for node in graph.nodes} for x in range(len(towers))]
	for part in partitions:
		part = {node : part[node] for node in graph.nodes}
		output.append(tuple([unlabeled_hamming_distance(graph, part, towers[x]) for x in range(len(towers))]))
	return output


#same as hamming_dist but for entropy distances
def entropy_dist(graph, partitions, towers):
	output = list()
	towers = [{node : towers[x][node] for node in graph.nodes} for x in range(len(towers))]
	for part in partitions:
		part = {node : part[node] for node in graph.nodes}
		output.append(tuple([entropy_distance(graph, part, towers[x]) for x in range(len(towers))]))
	return output


#This function uses code from the gerrymandr/spanning_trees repository. Uncomment and put a 
#file path to your local copy of the repository to use
'''
sys.path.append('file_path_to/spanning_trees')
from spanning_trees.main import explore_random


#generates num_towers-many partitions of graph into num_dists-many districts. Chooses
#partitions from a larger pool to avoid having close together towers. This is calculated
#using either hamming distance (when hamming == True) or entropy distance (when hamming == False)
#Districts must be contiguous, but can also have population constraints. Pop constraint is the
#percentage that outputted district populations may vary from the ideal district population 
#size (total population / num_dists). Default of 100 is equivalent to no population constraint
#Population constraint algorithm:
#	allowed population minimum = ideal_pop - ideal_pop * pop_constraint
#	allowed population maximum = ideal_pop + ideal_pop * pop_constraint
#Ex: total_pop = 10, num_dists = 2, pop_constraint = .2
#ideal population = 10/2 = 5
#allowed range of district populations = 5 - .2*5 - 5 + .2*5 = 4-6
#so only partitions for which both districts have population 4, 5, or 6 are outputted
def create_towers(graph, num_dists, num_towers = 3, hamming = True, pop_constraint = 100):
	if hamming:
		distance_measure = unlabeled_hamming_distance
	else:
		distance_measure = partition_entropy

	num_options = num_towers*5
	tower_options = explore_random(graph, num_options, num_dists, pictures = False, 
					divide_and_conquer = False, equi = False, delta = pop_constraint)
	for t in range(num_options):
		assignments = dict()
		for dist in range(num_dists):
			tower_options[t][dist] = {x : dist for x in tower_options[t][dist].nodes}
			assignments.update(tower_options[t][dist])
		tower_options[t] = assignments

	distances = dict()
	for o2 in range(num_options):
		for o1 in range(o2):
			if (o1,o2) not in distances:
				distances[(o1,o2)] = distance_measure(graph,tower_options[o1], tower_options[o2])

	if num_towers == 1:
		towers = [1]
	else:
		(t1,t2) = max(distances.items(), key=operator.itemgetter(1))[0]
		towers = [t1,t2]

	while len(towers) < num_towers:
		dists = dict()
		for o in range(num_options):
			if o in towers:
				continue
			total = list()
			for t in towers:
				total.append(tuple(sorted([o,t])))
			dists[o] = min(total)
		towers.append(max(dists.items(), key=operator.itemgetter(1))[0])

	pairs = list()
	tower_distances = list()
	for t1 in range(num_towers):
		for t2 in range(t1):
			pair = [towers[t1],towers[t2]]
			pair.sort()
			pair = tuple(pair)
			pairs.append((t2,t1))
			tower_distances.append(distances[pair])

	canon_towers = list()
	for t in towers:
		assign_dict = tower_options[t]
		assign_list = [assign_dict[node] for node in range(len(assign_dict))]
		canon_towers.append(canonical_form(assign_list))
	return (canon_towers, tower_distances)
'''

#===========================================================================================
#Distance calculation algorithms written by Robert Dougherty-Bliss
#Original can be found here: https://gist.github.com/rwbogl/0eadcdf28dd07afa0c9db8ad073e5ce4

import scipy.optimize as optimize
import numpy as np
import itertools


def build_inverse_dictionaries(graph, initial_assignment, current_assignment):
	# Build "inverse" dictionaries; i.e., the actual partitions.
	initial_inverse = dict()
	current_inverse = dict()

	for node in graph.nodes:
		initial = initial_assignment[node]
		current = current_assignment[node]

		if initial not in initial_inverse:
			initial_inverse[initial] = set()
		if current not in current_inverse:
			current_inverse[current] = set()

		initial_inverse[initial].update([node])
		current_inverse[current].update([node])

	return initial_inverse, current_inverse


def partition_entropy(graph, initial_assignment, current_assignment):
	"""Compute the entropy between two partitions of the graph.
	:graph: Underlying graph.
	:returns: Entropy.
	"""
	initial_inverse, current_inverse = build_inverse_dictionaries(graph, initial_assignment, current_assignment)

	terms = itertools.product(initial_inverse.values(), current_inverse.values())

	entropy_sum = 0

	for initial_nodes, current_nodes in terms:
		shared = initial_nodes.intersection(current_nodes)

		shared_count = len(shared)
		initial_count = len(initial_nodes)
		current_count = len(current_nodes)
		proportion = shared_count / current_count

		if proportion != 0:
			entropy_sum -= initial_count * proportion * np.log(proportion)

	total_val = len(graph.nodes)

	return entropy_sum / total_val


def unlabeled_hamming_distance(graph, initial_assignment, current_assignment):
	"""Determine the permutation that yields the unlabeled Hamming distance.
	This method relies on the Hungarian algorithm.
	Here's a rough explanation:
		Consider the complete bipartite graph with sets of vertices
		corresponding to the cells of the respective partitions of the graph.
		Weight the edge (i, j) as the number of matching nodes between cell i
		and cell j if i were relabeled as j. Every perfect matching on this
		graph induces a permutation on the partition cells, and "N - the sum of
		the edge weights" is the hamming distance after relabeling by this
		permutation. Therefore the permutation that yields the unlabeled
		hamming distance is the perfect matching that maximizes the sum of edge
		weights. If we negate the edge weights, then we seek the minimum sum.
		This is equivalent to the assignment problem, which the Hungarian
		algorithm solves in O(n^3) time.
	"""
	initial_inverse, current_inverse = build_inverse_dictionaries(graph, initial_assignment, current_assignment)

	# This matrix should be square.
	cost_matrix = np.zeros((len(initial_inverse), len(current_inverse)))

	for i, initial_cell in enumerate(initial_inverse.values()):
		for j, current_cell in enumerate(current_inverse.values()):
			# Compute the overlap between the two cells.
			intersection = initial_cell.intersection(current_cell)
			cost_matrix[i, j] = -len(intersection)

	row, col = optimize.linear_sum_assignment(cost_matrix)

	# We negated the entries of the matrix, so we add here.
	best_distance = len(graph) + cost_matrix[row, col].sum()

	return best_distance
