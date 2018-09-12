# benchmarking
Welcome to the benchmarking repo!

Much of our data is stored as .p files using the pickle import. Each file represents a single python
data structure which be perfectly maintained when imported into python. The following code snippet
will import a .p file and assign its information to a variable 'data'.


import pickle

import bz2

data = pickle.load(bz2.BZ2File(new_file_name,'rb'))



Partitions of a graph into districts follow this canonical form:
The partition is given as a tuple, with each element representing a node/precinct. The index of the 
element is its ID in the graph, and the value is its district. District labels are not maintained
across multiple partitions, but rather are assigned by order of appearance. So if part is a partition,
part[0] will always be 1 bc it appears first, and every node in the same district will also have a value 
of 1. This form doesn't maintain consistent labeling of districts intentionally because district 
labels aren't considered important, only the district shapes. Because of this, even if two districts
swap labels they will be relabeled as though nothing had changed, so (1,1,2,2) and (2,2,1,1) are 
equivalent because (2,2,1,1) will be relabeled as (1,1,2,2).
ex: (1,2,3,4), (1,1,2,2), and (1,2,1,2) are all in canonical form.
(4,3,2,1), (2,2,1,1), and (2,1,1,2) are not.
If (1,1,2,2) is inputted in RunDMCMC and the first node is reassigned to the second district
it won't be outputted as (2,1,2,2) but rather it will become (1,2,1,1). 


RunDMCMC takes in a graph representing a set of adjacent precincts and an initial partition of those
precincts into k-many districts. It then 'proposes' an alternate partition, and accepts that partition
if it passes certain validity checks (such as requiring that disctricts be continguous or equally
populated). If a proposal is accepted it becomes the new input and more proposals are made from it,
with each accepted proposal being a 'step'. The following are methods of creating proposals from
a base partition:

Single flip:A random edge between two districts is chosen and one of its nodes is randomly flipped
	into the other's district.
	Laziness:Because different partitions have a higher or lower degree in the metagraph,
	some are more likely to appear. The single flip method can be made 'lazy' by making it
	stay longer at a given partition with probability inversely proportional to its metagraph
	degree. This is effect creates self loops in the metagraph which are intended to give all
	nodes equal degree. Files which start with real_degree_lazy perform a costly calculation
	to measure the exact metagraph degree and weight accordingly. Files starting with 
	approx_lazy use a much faster approximation of degree and weight using that. Files starting
	with not_lazy don't use laziness at all. Given infinite steps, the real_degree_lazy proposals
	will sample uniformly from all valid partitions, however it is extremely costly and 
	explores the metagraph much slower than the not lazy proposal method, so for most 
	practical purposes not_lazy is best. Approx_degree is fast enough to run even on large 
	graphs, but it still explores slowly.

Reversible chunk flip: A random edge between two districts is chosen and one of its nodes is randomly
	flipped into the other's district. Furthermore, other nodes which share an edge and district
	with the flipped node can be flipped, and their neighobors and so on. Though the probability
	of flipping decreases exponentially so large flips are unlikely (and are unlikely to result in
	valid partitions).
