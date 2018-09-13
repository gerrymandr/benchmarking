# See main.py in the plots folder for an updated example of producing benchmarking plots.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import pickle

def get_dem_seat_share(dems, reps, districting):
    num_districts = int(max(districting))
    seats = 0
    for d in range(1, num_districts):
        dem_count = np.sum(dems[districting == d])
        rep_count = np.sum(reps[districting == d])
        if dem_count > rep_count:
            seats += 1
        # add half a seat in the case of a tie
        elif dem_count == rep_count == 0:
            seats += 0.5
    return seats

with open('data/full_ensemble.p', 'rb') as f:
    full_ensemble_tuples = pickle.load(f)
full_ensemble = [np.array(plan) for plan in full_ensemble_tuples]

path = 'data/sampled_ensembles/single_flip/with_degrees/'
chain = 'wes_lazy_500000'
with open(path + chain + '.p','rb') as f:
    sampled_ensemble = pickle.load(f)
with open(path + chain + '_freq.p','rb') as f:
    sampled_ensemble_freqs = pickle.load(f).values()
    
sampled_ensemble_tuples = [plan for (plan, degree) in sampled_ensemble]
unique_ensemble_tuples = set(sampled_ensemble_tuples)
unique_ensemble = [np.array(plan) for plan in set(sampled_ensemble_tuples)]
sampled_ensemble = [np.array(plan) for plan in sampled_ensemble_tuples]

demographic_data = np.loadtxt(open('data/demographic_data.csv', 'rb'), delimiter=',', skiprows=1)
dems = demographic_data[:,1]
reps = demographic_data[:,2]

seat_shares_dict = dict([(p, get_dem_seat_share(dems, reps, np.array(p)))
                         for p in full_ensemble_tuples])
seat_shares_full = list(seat_shares_dict.values())
seat_shares_sampled = [seat_shares_dict[plan] for plan in sampled_ensemble_tuples]
seat_shares_unique = [seat_shares_dict[plan] for plan in unique_ensemble_tuples]

bins = [0,1,2,3]
full_bin_relative_freqs = np.histogram(seat_shares_full, bins=bins, density=True)[0]
sampled_bin_relative_freqs = np.histogram(seat_shares_sampled, bins=bins, density=True)[0]
unique_bin_relative_freqs = np.histogram(seat_shares_unique, bins=bins, density=True)[0]

sampled_errors = []
unique_errors = []
num_unique = []
for i in range(1, len(sampled_ensemble), 10000):
    sampled_bin_relative_freqs = np.histogram(seat_shares_sampled[:i], bins=bins, density=True)[0]
    unique_samples = set(sampled_ensemble_tuples[:i])
    num_unique.append(len(unique_samples))
    urf = np.histogram(seat_shares_unique[:len(unique_samples)], bins=bins, density=True)[0]
    sampled_error = np.sum(np.abs(sampled_bin_relative_freqs - full_bin_relative_freqs))
    sampled_errors.append(sampled_error)
    unique_error = np.sum(np.abs(urf - full_bin_relative_freqs))
    unique_errors.append(unique_error)


fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
x = np.array(bins[:-1]) + 0.5
zero = [0] * (len(bins) - 1)

unseen = len(full_ensemble) - len(unique_ensemble)
ax1.plot(([0] * unseen) + sorted(sampled_ensemble_freqs))
ax1.axvline(x=unseen, color='g')
ax1.set_title('Plan Counts')
ax1.set_xlabel('plan')
ax1.set_ylabel('# occurences')

p1 = ax2.fill_between(x, full_bin_relative_freqs, zero)
p2, = ax2.plot(x, sampled_bin_relative_freqs, 'r')
p3, = ax2.plot(x, unique_bin_relative_freqs, 'g')
ax2.set_xticks(bins)
ax2.fill()
ax2.set_ylim([0, 1])
ax2.set_title('Seat Share')
ax2.set_xlabel('# Dem Seats Won')
ax2.set_ylabel('Relative Frequency')
ax2.legend([p1, p2, p3], ['fully enumerated', 'sampled', 'unique sampled'])

p1, = ax3.plot(sampled_errors)
p2, = ax3.plot(unique_errors)
ax3.set_title('L1 dist to uniform')
ax3.set_xlabel('# iterations')
ax3.set_ylabel('L1')
ax3.legend([p1, p2], ['sampled', 'unique sampled'])
ax4.plot(num_unique)
ax4.set_title('Exploration')
ax4.set_xlabel('# iterations')
ax4.set_ylabel('# unique plans seen')
