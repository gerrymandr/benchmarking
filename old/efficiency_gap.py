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

def get_enum_freqs(enumeration, sample):
    # initialize dictionary to store frequency with which every enumerated partition appeared in sample
    enum_freqs = {}
    for i, item in enumerate(enumeration):
        if item not in sample.keys():
            # if the partition wasn't in the sample, assign frequency 0
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

#print(canonical_sample)

enum_freqs = get_enum_freqs(full_ensemble, canonical_sample)
#print(enum_freqs)

plt.scatter(enum_freqs.keys(), enum_freqs.values())
plt.ylim(0,8)
plt.show()