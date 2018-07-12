This file measures the movement of different proposal methods in RunDMCMC across the metagraph.

The only constraints are that districts must be contiguous and they can't be destroyed, and
each step in RunDMCMC is a 3 district partition of the graph from the Fifield et al dataset.

First, 500 random seeds(partitions) were generated using code from gerrymandr/spanning-trees. 
From these 500, 25 seeds with approximately maximal hammingdistance between them were chosen in 
an attempt to obtain seeds from all corners of the metagraph.

Information on these seeds is stored in seeds.p, which contains a 3-tuple. 
The first element of the tuple is a list of all the seeds, each seed being represented by a 
tuple, with index representing the vtd # and the value being the assigned district. Districts 
are numbered in canonical form.
The second element is a list 2-tuples, with each tuple holding the indeces of 2 seeds.
The third element is a list of inter-seed distances, with the ith index being the distance
between the ith pair in the second element.
Ex: If seeds[1][0] equals (0,3), then seeds[2][0] contains the hamming distance between 
seeds[0][0] and seeds[0][3].

The other files hold information on 100,000 step RunDMCMC runs, represented as lists of 2-tuples.
The first element is the partition, a record of district assignments stored in a tuple, with index 
representing the precinct # and the value being the assigned district. District numbers are 
numbered in canonical form.
The second element is a list of distances, with the ith index being the hamming or entropy distance
between the current partition and ith seed in seeds.p.

For details on importing files,proposal methods, or a description of canonical form, 
see the main data file README. 