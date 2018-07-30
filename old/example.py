# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 14:57:55 2018

@author: Sloan
"""
import numpy as np

# each row represents a districting plan
ensemble = np.loadtxt(open('enumerated_ensemble_full.csv', 'rb'), delimiter=',')
ensemble = np.transpose(ensemble)

# get first districting plan
plan = ensemble[0,:]

# each row represents a precinct
demographic_data = np.loadtxt(open('demographic_data.csv', 'rb'), delimiter=',', skiprows=1)
populations = demographic_data[:,0]
dems = demographic_data[:,1]
reps = demographic_data[:,2]

# get population in first district
pop = np.sum(populations[plan == 1])
dem_count = np.sum(dems[plan == 1])
rep_count = np.sum(reps[plan == 1])