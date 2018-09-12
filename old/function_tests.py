
#Disclaimer:
#This file is within the Old folder, and changes could have been made to these functions before integration with other programs.  
#The more recent versions of these functions are in use within larger programs.  
#Use these separate test versions at your own risk.

#Functions written and tested in this file include:
#1. canonical_form
#This function intakes a districting partition in a form produced by a separate enumeration function, and translates it into a standardized form, which the function returns.
#This is important because we often need the computer to  be able to compare two districting plans and evaluate whether they are the same, but each plan has many possible relabelings.  
#Canonical form ensures that any two relabelings of the same districting plan are not mistaken for unique plans in future functions.  
#For more on canonical form, see the top-level ReadMe. 
#For more on using pickles in python, see the top-level ReadMe.

#2. get_enum_freqs
#This function runs a sample of districting plans against the full enumeration of possible districting plans, 
#with the goal of comparing the two sets.  
#For a fixed map, input a .csv of all possible enumerated districting plans under some constraints.  
#Input a sample of districting plans.  
#The function outputs a dictionary which stores how often each possible partition appeared in the sample.  
#For example, 80 of the possible enumerated partitions could have appeared 0 times, 
#while 5 of them appeared 4 times.
#In order to evaluate the randomness of a sampling algorithm, 
#we may be interested in understanding why certain partitions appear many times before others appear at all.
#This function is only functional as long as full enumeration is feasible (not long at all).




import pickle
#For more on our use of python pickles, see the top-level ReadMe.
import numpy as np
import matplotlib.pyplot as plt

def canonical_form(vector):
#For more on the concept of canonical form, see the top-level ReadMe. 
    wrong = list(vector)
    seen = set()
    wrong_order = [d for d in wrong if not (d in seen or seen.add(d))]
    correct_order = list(range(1, len(wrong_order) + 1))
    correction_table = dict(zip(wrong_order, correct_order))
    right = [correction_table[d] for d in wrong]
    return right

def get_enum_freqs(enumeration, sample):
    # initialize dictionary to store frequency with which every enumerated partition appeared in sample
    enum_freqs = {}
    for i, item in enumerate(enumeration):
        if item not in sample.keys():
            # if the partition wasn't in the sample, assign frequency zero
            enum_freqs[i]= 0
        else:
            # if the partition was in the sample, assign the frequency with which it appeared (from dictionary input)
            enum_freqs[i]=sample[item]
    return enum_freqs

full_ensemble = np.loadtxt(open('enumerated_ensemble_full.csv', 'rb'), delimiter=',')
full_ensemble = np.transpose(full_ensemble)
full_ensemble = [tuple([int(d) for d in plan]) for plan in full_ensemble]

sample_freq = pickle.load(open('single_flip_1000_steps.p', 'rb'))

canonical_sample = {}
for key in sample_freq.keys():
    canonical_sample[tuple(canonical_form(key))] = sample_freq[key]

enum_freqs = get_enum_freqs(full_ensemble, canonical_sample)

#The code at the end of this file plots the enum_freq output dictionary, 
#to visualize whether there are any spikes in the graph which would show us possible patterns in
# which types of partitions a certain algorithm prefers to choose.

plt.scatter(enum_freqs.keys(), enum_freqs.values())
plt.ylim(0,8)
plt.show()
