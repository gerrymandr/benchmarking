# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 14:57:55 2018

@author: Sloan
"""
import numpy as np

# each row represents a districting plan
ensemble = np.loadtxt(open('enumerated_ensemble_full.csv', 'rb'), delimiter=',')
ensemble = np.transpose(ensemble)

# each row represents a precinct
demographic_data = np.loadtxt(open('demographic_data.csv', 'rb'), delimiter=',', skiprows=1)