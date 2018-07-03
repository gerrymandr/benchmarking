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
ax2.hist([seat_shares_sampled[0]], bins=bins, density=True)
ax2.set_title('sampled ensemble')
ax2.set_xticks(bins)
'''
# define animation function which updates the plot
def animate(i):
    # define animation function which updates the plot
    def animate(i):
        # determine which points are in current t-axis cross section
        current_t = t_range[i]
        displayed_indices = [j for j in range(len(t)) \
             if (t[j] >= current_t) and (t[j] <= current_t + width)]
        x_disp = [x[j] for j in displayed_indices]
        y_disp = [y[j] for j in displayed_indices]
        
        # update points on scatter plot
        pts = np.array(list(zip(x_disp, y_disp)))
        if len(pts) == 0:
            pts = np.zeros((0,2))
        scat.set_offsets(pts)
        
        # update comparison line and best fit line, if present
        if comparison_line_info != None:
            comparison_line.set_data(get_comparison_line_points(current_t))
        if best_fit_line_info != None:
            best_fit_line.set_data(get_best_fit_line_points(x_disp, y_disp))
        
        # update text describing current state in time
        if width == 0:
            txt = '%s = %0.2f' % (t_info['label'], current_t)
        else:
            txt = '%s between %0.2f and %0.2f' % (t_info['label'],
                                                  current_t, current_t + width)
        t_text.set_text(txt)
        
        return scat, comparison_line, best_fit_line, t_text, legend

    # determine time b/t frames and create animation, saving if necessary
    interval = duration * 1000 / (len(t_range) - 1)
    anim = animation.FuncAnimation(fig, animate,
                                   frames=len(t_range),
                                   interval=interval, blit=True)
    
    return scat, comparison_line, best_fit_line, t_text, legend

# determine time b/t frames and create animation, saving if necessary
anim = animation.FuncAnimation(fig, animate,
                               frames=len(t_range),
                               interval=100, blit=True) 
'''