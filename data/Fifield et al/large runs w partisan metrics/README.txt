Each file contains 100,00 steps in RunDMCMC. Each step is a 3 district partition of the graph 
from the Fifield et al dataset. Each run starts from a random partition generated using code 
from Gerrymandr/spanning-trees.

The only constraints are that districts must be contiguous and they can't be destroyed.

The data is stored as a list of 3-tuples, with each tuple holding data on a single step : 
(partition, # of seats won by democrats out of 3, efficiency gap)

Partition is a record of district assignments stored in a tuple, with index representing the 
precinct # and the value being the assigned district. District numbers are numbered in 
canonical form.

For details on importing files, proposal methods, or a description of canonical form, 
see the main data file README. 