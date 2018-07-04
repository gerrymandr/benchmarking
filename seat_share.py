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

# each row represents a districting plan
full_ensemble = np.loadtxt(open('enumerated_ensemble_full.csv', 'rb'), delimiter=',')
full_ensemble = np.transpose(full_ensemble)
# use same data until a sample is provided

with open('single_flip_1000000_steps_w_repeats.p','rb') as f:
    sampled_ensemble = pickle.load(f)
sampled_ensemble = np.array([np.array(plan) for plan in sampled_ensemble])
sampled_ensemble = sampled_ensemble[20000:]

# each row represents a precinct
demographic_data = np.loadtxt(open('demographic_data.csv', 'rb'), delimiter=',', skiprows=1)
dems = demographic_data[:,1]
reps = demographic_data[:,2]

seat_shares_full = [get_dem_seat_share(dems, reps, plan) for plan in full_ensemble]
seat_shares_sampled = [get_dem_seat_share(dems, reps, plan) for plan in sampled_ensemble]

fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3)
bins = [0,1,2,3]
full_bin_counts = ax1.hist(seat_shares_full, bins=bins, density=True)[0]
full_bin_relative_frequencies = full_bin_counts / np.sum(full_bin_counts)
ax1.set_title('full ensemble')
ax1.set_xticks(bins)
ax1.set_ylim([0, 1])

# second plot unanimated, comment this out and uncomment the next part for animation
sampled_bin_counts = ax2.hist(seat_shares_sampled, bins=bins, density=True)[0]
ax2.set_title('sampled ensemble - lazy, minus start')
ax2.set_xticks(bins)
ax2.set_ylim([0, 1])

'''
errors = []

# define animation function which updates the plot
def animate(i):
    for ax in (ax2, ax3):
        ax.clear()
    sampled_bin_counts = ax2.hist([seat_shares_sampled[:(i*100+1)]], bins=bins, density=True)[0]
    sampled_bin_relative_frequencies = sampled_bin_counts / np.sum(sampled_bin_counts)
    error = np.sum(np.abs(sampled_bin_relative_frequencies - \
                          full_bin_relative_frequencies))
    errors.append(error)
    ax2.set_title('sampled ensemble')
    ax2.set_xticks(bins)
    ax2.set_ylim([0, 1])
    ax3.plot(errors)
    ax3.set_title('L1 dist to uniform')

num_frames = int(len(sampled_ensemble)/100)
anim = animation.FuncAnimation(fig, animate,
                               frames=num_frames,
                               interval=100) 
'''
