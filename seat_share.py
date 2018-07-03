import numpy as np
import matplotlib.pyplot as plt

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

# each row represents a districting plan
full_ensemble = np.loadtxt(open('enumerated_ensemble_full.csv', 'rb'), delimiter=',')
full_ensemble = np.transpose(full_ensemble)
# use same data until a sample is provided
sampled_ensemble = full_ensemble

# each row represents a precinct
demographic_data = np.loadtxt(open('demographic_data.csv', 'rb'), delimiter=',', skiprows=1)
dems = demographic_data[:,1]
reps = demographic_data[:,2]

seat_shares_full = [get_dem_seat_share(dems, reps, plan) for plan in full_ensemble]
seat_shares_sampled = [get_dem_seat_share(dems, reps, plan) for plan in sampled_ensemble]

fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3)
bins = [0,1,2,3]
ax1.hist(seat_shares_full, bins=bins, density=True)
ax1.set_title('full ensemble')
ax1.set_xticks(bins)
ax2.hist(seat_shares_sampled, bins=bins, density=True)
ax2.set_title('sampled ensemble')
ax2.set_xticks(bins)   