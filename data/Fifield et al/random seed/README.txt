Each file contains 100,000 steps in RunDMCMC, starting from an arbitrary partition.
Each step is a 3 district partition of the graph from the Fifield et al dataset. 

The only constraints are that districts must be contiguous and they can't be destroyed.

The data is stored as a list of 3-tuples, with each tuple holding data on a single step : 
(partition, # of seats won by democrats out of 3, efficiency gap)

Partition is a record of district assignments stored in a tuple, with index representing the 
precinct # and the value being the assigned district. District numbers are numbered in 
canonical form.

For details on importing files, proposal methods, or a description of canonical form, 
see the main data file README. 
